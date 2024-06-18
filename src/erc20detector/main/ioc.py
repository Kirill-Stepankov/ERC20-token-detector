from contextlib import asynccontextmanager
from typing import AsyncIterator

from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from erc20detector.application.get_contract import GetContractInteractor
from erc20detector.application.get_contracts import GetContractsInteractor
from erc20detector.application.process_contract import \
    ProcessContractInteractor
from erc20detector.application.upload_contract import UploadContractInteractor
from erc20detector.domain.contract.services.contract import ContractService
from erc20detector.infrastructure.contract_detector.erc20.contract_detector import \
    Erc20ContractDetectorImpl
from erc20detector.infrastructure.db.provider import (get_contract_gateway,
                                                      get_uow)
from erc20detector.infrastructure.http_client.aiohttp_client import \
    AioHTTPRequestContractClient
from erc20detector.infrastructure.source_code_compiler.source_code_compiler import \
    SourceCodeCompilerImpl
from erc20detector.presentation.interactor_factory import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        etherscan_api_key: str,
        http_session_factory: ClientSession,
    ):
        self._session_factory = session_factory
        self._contract_service = ContractService()
        self._etherscan_api_key = etherscan_api_key
        self._http_session_factory = http_session_factory

    @asynccontextmanager
    async def upload_contract(self) -> AsyncIterator[UploadContractInteractor]:
        async with self._session_factory() as session, self._http_session_factory() as http_session:
            interactor = UploadContractInteractor(
                contract_gateway=get_contract_gateway(session),
                http_client=AioHTTPRequestContractClient(
                    api_key=self._etherscan_api_key, http_session=http_session
                ),
                contract_service=self._contract_service,
                uow=get_uow(session),
            )

            yield interactor

    @asynccontextmanager
    async def get_contracts(self) -> AsyncIterator[GetContractsInteractor]:
        async with self._session_factory() as session:
            interactor = GetContractsInteractor(
                contract_gateway=get_contract_gateway(session)
            )

            yield interactor

    @asynccontextmanager
    async def get_contract(self) -> AsyncIterator[GetContractInteractor]:
        async with self._session_factory() as session:
            interactor = GetContractInteractor(
                contract_gateway=get_contract_gateway(session)
            )

            yield interactor

    @asynccontextmanager
    async def process_contract(self) -> AsyncIterator[ProcessContractInteractor]:
        async with self._session_factory() as session:
            interactor = ProcessContractInteractor(
                contract_gateway=get_contract_gateway(session),
                uow=get_uow(session),
                contract_detector=Erc20ContractDetectorImpl(),
                source_code_compiler=SourceCodeCompilerImpl(),
            )

            yield interactor
