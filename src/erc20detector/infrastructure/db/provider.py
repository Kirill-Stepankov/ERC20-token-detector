import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from erc20detector.main.config import DatabaseConfig

from ..repositories.contract_gateway import ContractGatewayImpl
from .uow import UnitOfWork


def get_engine(db_config: DatabaseConfig) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        db_config.get_connection_url(),
        pool_size=15,
        max_overflow=15,
    )

    return engine


def get_async_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    logging.info("Session factory was initialized")

    return session_factory


def get_uow(session: AsyncSession) -> UnitOfWork:
    return UnitOfWork(session=session)


def get_contract_gateway(session: AsyncSession) -> ContractGatewayImpl:
    return ContractGatewayImpl(session=session)
