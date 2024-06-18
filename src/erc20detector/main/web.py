import logging
from datetime import timedelta
from typing import Callable, TypeVar

import aiohttp
import solcx
from fastapi import FastAPI
from solcx import install_solc

from erc20detector.infrastructure.db.provider import (get_async_sessionmaker,
                                                      get_engine)
from erc20detector.presentation.contract.endpoints.contract import \
    contract_router
from erc20detector.presentation.contract.exception_handlers.contract import \
    include_exception_handlers
from erc20detector.presentation.interactor_factory import InteractorFactory

from .config import load_config
from .ioc import IoC

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

DependencyT = TypeVar("DependencyT")


def singleton(value: DependencyT) -> Callable[[], DependencyT]:

    def singleton_factory() -> DependencyT:
        return value

    return singleton_factory


def create_app() -> FastAPI:
    app = FastAPI()
    config = load_config()

    versions = solcx.get_installable_solc_versions()
    for v in versions:
        install_solc(v.base_version)

    engine = get_engine(config.db_config)

    session_factory = get_async_sessionmaker(engine)
    ioc = IoC(
        session_factory=session_factory,
        etherscan_api_key=config.etherscan_config.api_key,
        http_session_factory=aiohttp.ClientSession,
    )

    app.dependency_overrides.update(
        {
            InteractorFactory: singleton(ioc),
        }
    )

    app.include_router(contract_router)
    include_exception_handlers(app)
    return app


app = create_app()
