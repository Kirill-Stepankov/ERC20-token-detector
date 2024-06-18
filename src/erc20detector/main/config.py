import os
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)

ETHERSCAN_API_KEY_ENV = "ETHERSCAN_API_KEY"
HOST_DB_ENV = "POSTGRES_HOST"
DB_NAME_ENV = "POSTGRES_DB"
DB_USER_ENV = "POSTGRES_USER"
DB_PASSWORD_ENV = "POSTGRES_PASSWORD"
DB_PORT = "DB_PORT"


class ConfigParseError(ValueError):
    pass


@dataclass
class EtherscanConfig:
    api_key: str


@dataclass
class DatabaseConfig:
    host: str
    db_name: str
    user: str
    password: str
    port: str

    def get_connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db_name}"


@dataclass
class Config:
    etherscan_config: EtherscanConfig
    db_config: DatabaseConfig


def get_str_env(key) -> str:
    val = os.getenv(key)
    if not val:
        logger.error("%s is not set", key)
        raise ConfigParseError(f"{key} is not set")
    return val


def load_etherscan_config() -> EtherscanConfig:
    api_key = get_str_env(ETHERSCAN_API_KEY_ENV)
    return EtherscanConfig(api_key=api_key)


def load_db_config() -> DatabaseConfig:
    host = get_str_env(HOST_DB_ENV)
    user = get_str_env(DB_USER_ENV)
    name = get_str_env(DB_NAME_ENV)
    password = get_str_env(DB_PASSWORD_ENV)
    port = get_str_env(DB_PORT)

    return DatabaseConfig(
        host=host, user=user, db_name=name, password=password, port=port
    )


def load_config() -> Config:
    etherscan_config = load_etherscan_config()
    db_config = load_db_config()

    return Config(
        etherscan_config=etherscan_config,
        db_config=db_config,
    )
