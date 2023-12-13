[toc]

# Design considerations

## Risks

- We removed a redundant LDAP check
before triggering the notification, the upstream script checks agains LDAP
that the user exists. This is also done by UMC and thus should be redundant.

## Why not use the upstream code?

The upstream code consists of three components,
which are deeply integrated with the UCS Appliance

- listener module
- cli script (executed by systemd)
  - uses UCR
  - systemd watchdog
  - cli arguments not needed
  - ldap call not needed
- UMC RPC client library
  - depends on UCR
  - Hard-Coded HTTPS
  - could not easily get it working

We would have to heavily patch these components to fit our stack
and the result would be much more complex than a reimplementation.

We re-implemented it in ~70 lines of python code.

## Authentication

- We use basic auth against UMC RPC on every request.
This is advantageous, becasuse we don't have to manage a UMC Session
including timeouts and reauthentication.
UMC creates only one session per user
meaning that even with thousands of requests including authentications
there is no risk of overloading the UMC Server with to many sessions.


## Retries

scope:
The selfservice listener is only responsible for calling a `umc-command`.
The UMC ensures that a user actually exists and tries to send the email.
If the user does not exist or the mail address is invalid, it's a success
from the perspective of the selfservice-listener.

Only if the UMC responds with an error,
(because it can't reach it's mail gateway, internal server error, not found,)
It's a failure from the perspective of the selfservice-listener and should be retried.

Ideally the message queue should be configured to coordinate retries
with exponential backoff.
Our "file based queue" obviously has no such functionality.

We implemented a simple but limited alternative client-side.

The `watchdog` library only detects newly created files
and does not take existing files into account.
This is the reason why reverted back to an infinite while loop with a 5-second interval.

If the UMC Command was successful, the file gets deleted.
if not, it gets retried on the next loop iteration.
Internally the python script counts the retries for each user
and when the invitation failed for the 5th time, the process exits with an error.
This means the complete Pod (including the listener container)
will be terminated and re-created.
This is to communicate the failure upstream to the kubernetes controllers.

Unfortunately this does not trigger the kubernetes CrashLoopBackoff
because the pod seems healthy while doing the retries for ~25 seconds.
