# selfservice-listener

The selfservice listener for handling user invites

- **Version**: 0.1.0
- **Type**: application
- **AppVersion**: 0.0.1
-

## Introduction

This chart does install a the selfservice listener container.

It is intended to listen for newly created users, starting the flow to send the
user an email to set their password.

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://gitregistry.knut.univention.de/univention/customers/dataport/upx/common-helm/helm | common | ^0.2.0 |

## Values

<table>
	<thead>
		<th>Key</th>
		<th>Type</th>
		<th>Default</th>
		<th>Description</th>
	</thead>
	<tbody>
		<tr>
			<td>affinity</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>fullnameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.imagePullSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
"Always"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.registry</td>
			<td>string</td>
			<td><pre lang="json">
"gitregistry.knut.univention.de"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"univention/customers/dataport/upx/selfservice-listener/selfservice-listener"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.sha256</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Define image sha256 as an alternative to `tag`</td>
		</tr>
		<tr>
			<td>image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>nameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>nodeSelector</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>podAnnotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>podSecurityContext</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>replicaCount</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>resources</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>securityContext</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.caCert</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>CA root certificate, base64-encoded. Optional; will be written to "caCertFile" if set.</td>
		</tr>
		<tr>
			<td>selfserviceListener.caCertFile</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Where to search for the CA Certificate file. caCertFile: "/var/secrets/ca_cert"</td>
		</tr>
		<tr>
			<td>selfserviceListener.debugLevel</td>
			<td>string</td>
			<td><pre lang="json">
"4"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.environment</td>
			<td>string</td>
			<td><pre lang="json">
"production"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapBaseDn</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapHost</td>
			<td>string</td>
			<td><pre lang="json">
"ucs-machine"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapHostDn</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapPassword</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>LDAP password for `cn=admin`. Will be written to "ldapPasswordFile" if set.</td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapPasswordFile</td>
			<td>string</td>
			<td><pre lang="json">
"/var/secrets/ldap_secret"
</pre>
</td>
			<td>The path to the "ldapPasswordFile" docker secret or a plain file</td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapPort</td>
			<td>string</td>
			<td><pre lang="json">
"389"
</pre>
</td>
			<td>Will add a mapping from "ldapHost" to "ldapHostIp" into "/etc/hosts" if set</td>
		</tr>
		<tr>
			<td>selfserviceListener.notifierServer</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Defaults to "ldapHost" if not set.</td>
		</tr>
		<tr>
			<td>selfserviceListener.tlsMode</td>
			<td>string</td>
			<td><pre lang="json">
"secure"
</pre>
</td>
			<td>Whether to start encryption and validate certificates. Chose from "off", "unvalidated" and "secure".</td>
		</tr>
		<tr>
			<td>tolerations</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
	</tbody>
</table>

