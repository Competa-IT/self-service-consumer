# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from functools import lru_cache
from typing import Literal
from pydantic import conint
from pydantic_settings import BaseSettings

Loglevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class SelfServiceConsumerSettings(BaseSettings):
    log_level: Loglevel
    max_umc_request_retries: conint(ge=0, le=10)
    umc_server_url: str
    umc_admin_user: str
    umc_admin_password: str


@lru_cache
def get_selfservice_consumer_settings() -> SelfServiceConsumerSettings:
    return SelfServiceConsumerSettings()
