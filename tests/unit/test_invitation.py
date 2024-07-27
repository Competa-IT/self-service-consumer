# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from copy import deepcopy
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from client import AsyncClient, MessageHandler, Settings
from shared.models import Message, ProvisioningMessage, PublisherName
from invitation.__main__ import InvalidMessageSchema, SelfServiceConsumer
from invitation.config import SelfServiceConsumerSettings


class MockedResponse(MagicMock):
    def __init__(self, status, json=None, *args):
        super().__init__(*args)
        self.status = status
        self.json = AsyncMock(return_value=json)


USERNAME = "testuser"
MESSAGE = Message(
    publisher_name=PublisherName.udm_listener,
    ts=datetime(2023, 11, 9, 11, 15, 52, 616061),
    realm="udm",
    topic="users/user",
    body={
        "new": {
            "properties": {
                "username": USERNAME,
                "PasswordRecoveryEmail": "example@gmail.com",
                "pwdChangeNextLogin": True,
            }
        },
        "old": None,
    },
)
MESSAGE_OLD_USER = deepcopy(MESSAGE)
MESSAGE_OLD_USER.body["old"] = {"properties": {"username": USERNAME}}

MESSAGE_NO_EMAIL = deepcopy(MESSAGE)
MESSAGE_NO_EMAIL.body["new"]["properties"] = {
    "username": USERNAME,
    "pwdChangeNextLogin": True,
}

MESSAGE_PWD_CHANGE_NEXT_LOGIN_IS_NONE = deepcopy(MESSAGE)
MESSAGE_PWD_CHANGE_NEXT_LOGIN_IS_NONE.body["new"]["properties"] = {
    "username": USERNAME,
    "PasswordRecoveryEmail": "example@gmail.com",
    "pwdChangeNextLogin": None,
}


MESSAGE_NO_USERNAME = deepcopy(MESSAGE)
MESSAGE_NO_USERNAME.body["new"]["properties"] = {
    "PasswordRecoveryEmail": "example@gmail.com",
    "pwdChangeNextLogin": True,
}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def selfservice_consumer_settings() -> SelfServiceConsumerSettings:
    return SelfServiceConsumerSettings(
        log_level="DEBUG",
        max_umc_request_retries=3,
        umc_server_url="http://foo.local",
        umc_admin_user="user",
        umc_admin_password="password",
    )


@pytest.fixture
def selfservice_consumer(selfservice_consumer_settings) -> SelfServiceConsumer:
    return SelfServiceConsumer(settings=selfservice_consumer_settings)


@pytest.fixture
def provisioining_client_settings() -> Settings:
    return Settings(
        provisioning_api_base_url="http://foo.local",
        provisioning_api_username="bar",
        provisioning_api_password="baz",
    )


@pytest.fixture
async def mock_provisioning_client(
    provisioining_client_settings: Settings,
) -> AsyncClient:
    client = AsyncClient(provisioining_client_settings)
    client.get_subscription_message = AsyncMock()
    client.set_message_status = AsyncMock()
    return client


def mock_constructor_factory(instance):
    def mock_constructor():
        return instance

    return mock_constructor


class EscapeLoopException(Exception):
    ...


PROVISIONING_MESSAGE = ProvisioningMessage(
    publisher_name=PublisherName.udm_listener,
    ts=datetime.now(),
    realm="udm",
    topic="users/user",
    body={"old": {}, "new": {}},
    sequence_number=33,
    num_delivered=2,
)


@pytest.mark.anyio
async def test_invalid_requests(
    selfservice_consumer: SelfServiceConsumer,
    mock_provisioning_client: AsyncClient,
):
    mock_provisioning_client.get_subscription_message.side_effect = [
        PROVISIONING_MESSAGE,
        EscapeLoopException("let's exit the loop"),
    ]

    selfservice_consumer.send_email_invitation = AsyncMock()

    with pytest.raises(EscapeLoopException):
        await selfservice_consumer.start_the_process_of_sending_invitations(
            mock_constructor_factory(mock_provisioning_client), MessageHandler, "foobar"
        )

    selfservice_consumer.send_email_invitation.assert_not_awaited()


@pytest.mark.anyio
async def test_valid_provisioning_message(
    selfservice_consumer: SelfServiceConsumer,
    mock_provisioning_client: AsyncClient,
):
    mock_provisioning_client.get_subscription_message.side_effect = [
        PROVISIONING_MESSAGE,
        EscapeLoopException("let's exit the loop"),
    ]

    selfservice_consumer.send_email_invitation = AsyncMock()
    message = PROVISIONING_MESSAGE
    message.body = {
        "new": {
            "properties": {
                "username": "jblob",
                "pwdChangeNextLogin": True,
                "PasswordRecoveryEmail": "lohmer@univention.de",
            }
        },
        "old": None,
    }

    with pytest.raises(EscapeLoopException):
        await selfservice_consumer.start_the_process_of_sending_invitations(
            mock_constructor_factory(mock_provisioning_client), MessageHandler, "foobar"
        )
    selfservice_consumer.send_email_invitation.assert_awaited_once_with("jblob")


# @pytest.mark.anyio
# async def test_send_email(
#     selfservice_consumer: SelfServiceConsumer,
#     mock_provisioning_client: AsyncClient,
# ):
#     mock_post.assert_called_once_with(
#         f"{ENV_DEFAULTS['UMC_SERVER_URL']}/command/passwordreset/send_token",
#         json={"options": {"username": USERNAME, "method": "email"}},
#         auth=BasicAuth(
#             ENV_DEFAULTS["UMC_ADMIN_USER"], ENV_DEFAULTS["UMC_ADMIN_PASSWORD"]
#         ),
#     )
#     selfservice_consumer.send_email()


@pytest.mark.anyio
@pytest.mark.parametrize(
    "message",
    [MESSAGE_OLD_USER, MESSAGE_PWD_CHANGE_NEXT_LOGIN_IS_NONE],
)
async def test_message_filtering(
    message: Message,
    selfservice_consumer: SelfServiceConsumer,
):
    selfservice_consumer.send_email_invitation = AsyncMock()

    await selfservice_consumer.handle_user_event(message)

    selfservice_consumer.send_email_invitation.assert_not_awaited()


@pytest.mark.anyio
@pytest.mark.parametrize(
    "message",
    [MESSAGE_NO_EMAIL, MESSAGE_NO_USERNAME],
)
async def test_invalid_message_schema(
    message: Message,
    selfservice_consumer: SelfServiceConsumer,
):
    selfservice_consumer.send_email_invitation = AsyncMock()

    with pytest.raises(InvalidMessageSchema):
        await selfservice_consumer.handle_user_event(message)

    selfservice_consumer.send_email_invitation.assert_not_awaited()


@pytest.mark.anyio
@patch("asyncio.sleep", return_value=None)
@pytest.mark.parametrize("retries", [0, 3, 9, 10])
async def test_valid_retry_values(
    mock_sleep, retries, selfservice_consumer: SelfServiceConsumer
):
    selfservice_consumer.settings.max_umc_request_retries = retries
    selfservice_consumer.send_email_invitation = AsyncMock(return_value=False)

    with pytest.raises(SystemExit) as excinfo:
        await selfservice_consumer.handle_user_event(MESSAGE)

    assert excinfo.value.code == 1
    assert selfservice_consumer.send_email_invitation.call_count == retries + 1
    assert mock_sleep.call_count == retries

    # @patch("invitation.__main__.asyncio.sleep")
    # @patch("invitation.__main__.sys.exit")
    # async def test_error_during_sending_email(
    #     self,
    #     mock_sys_exit,
    #     mock_sleep,
    #     mock_post,
    #     async_client: AsyncClient,
    #     message_handler: MessageHandler,
    # ):
    #     invitation = SelfServiceConsumer()
    #     mock_sys_exit.side_effect = Exception("SystemExit 1")
    #     mock_post.return_value.__aenter__.return_value = MockedResponse(500, {})
    #     message_handler.run = Mock(return_value=invitation.handle_new_user(MESSAGE))
    #     with pytest.raises(Exception, match="SystemExit 1"):
    #         await invitation.start_the_process_of_sending_invitations()
    #
    #     async_client.assert_called_once_with()
    #     message_handler.run.assert_called_once_with()
    #     assert mock_post.call_count == 3
    #     mock_sleep.assert_has_calls([call(2), call(4)])
    #     mock_sys_exit.assert_called_once_with(1)
