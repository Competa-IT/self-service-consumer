import logging
import os
import sys
import time
from pathlib import Path

import requests

UMC_SERVER_URL = os.environ.get("UMC_SERVER_URL", "http://umc-server")
UMC_ADMIN_USER = os.environ.get("UMC_ADMIN_USER", "admin")
UMC_ADMIN_PASSWORD = os.environ.get("UMC_ADMIN_PASSWORD")

console_handler = logging.StreamHandler(sys.stdout)
logger = logging.getLogger("selfservice-invitation")
logger.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))
formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d  %(name)-11s ( %(levelname)-7s ) : %(message)s",
    "%d.%m.%y %H:%M:%S",
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def handle_file(path: Path):
    username = path.name[:-5]
    try:
        response = requests.post(
            f"{UMC_SERVER_URL}/command/passwordreset/send_token",
            json={
                "options": {
                    "username": username,
                    "method": "email",
                },
            },
            auth=(UMC_ADMIN_USER, UMC_ADMIN_PASSWORD),
        )
        response_data = response.json()
        if response.status_code != 200:
            logger.error(
                "There was an error requesting a user invitation email: %r"
                % response_data
            )
            return
        logger.info("Email invitation sent to user %s" % username)
        logger.debug(response_data)
        os.remove(path)
        logger.debug("Removing %s to avoid duplicate email invites" % path)
    except requests.exceptions.ConnectionError as e:
        logger.error("Could not reach UMC server: %r" % e)


def main():
    queue_directory = Path("/var/cache/listener")

    logger.info("Starting the filesystem watch to trigger invitation emails via the UMC")
    while True:
        logger.debug("Checking queue directory for new files: %s", queue_directory)
        for filename in queue_directory.glob("*.send"):
            handle_file(filename)

        time.sleep(5)


if __name__ == "__main__":
    main()
