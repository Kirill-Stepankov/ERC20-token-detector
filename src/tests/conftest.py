from unittest.mock import AsyncMock

import pytest

from erc20detector.application.common.contract_detector import ContractDetector
from erc20detector.application.common.contract_gateway import ContractGateway
from erc20detector.application.common.dto import ContractResponse, OKResult
from erc20detector.application.common.request_contract_client import \
    RequestContractClient
from erc20detector.application.common.source_code_compiler import \
    SourceCodeCompiler
from erc20detector.application.common.uow import UoW
from erc20detector.domain.contract.entities.contract import (Contract,
                                                             ContractId)
from erc20detector.domain.contract.services.contract import ContractService
from erc20detector.domain.contract.value_objects.processing_status import \
    ProcessingStatus

CONTRACT_ID = ContractId(100)
CONTRACT_ADDRESS = "0x1212"

NEW_CONTRACT_ID = ContractId(200)
NEW_CONTRACT_ADDRESS = "0x3434"


@pytest.fixture()
def uow() -> UoW:
    uow_mock = AsyncMock()
    uow_mock.commit = AsyncMock()
    uow_mock.rollback = AsyncMock()
    uow_mock.flush = AsyncMock()
    return uow_mock


@pytest.fixture()
def contract_gateway() -> ContractGateway:
    gateway = AsyncMock()
    gateway.save_contract = AsyncMock()
    gateway.total_contracts = AsyncMock(return_value=2)
    gateway.update_contract = AsyncMock()
    gateway.get_contract_by_address = AsyncMock(
        return_value=Contract(
            id=CONTRACT_ID,
            contract_address=CONTRACT_ADDRESS,
            contract_name="",
            source_code="",
            is_erc20=False,
            erc20_version=None,
            status=ProcessingStatus.WAITS_PROCESSING.value,
        )
    )
    gateway.find_contracts = AsyncMock(
        return_value=[
            Contract(
                id=CONTRACT_ID,
                contract_address=CONTRACT_ADDRESS,
                contract_name="",
                source_code="",
                is_erc20=False,
                erc20_version=None,
                status=ProcessingStatus.WAITS_PROCESSING.value,
            ),
            Contract(
                id=NEW_CONTRACT_ID,
                contract_address=NEW_CONTRACT_ADDRESS,
                contract_name="",
                source_code="",
                is_erc20=False,
                erc20_version=None,
                status=ProcessingStatus.WAITS_PROCESSING.value,
            ),
        ]
    )
    return gateway


@pytest.fixture()
def contract_detector() -> ContractDetector:
    contract_detector = AsyncMock()
    contract_detector.is_contract_detected = AsyncMock(return_value=True)

    return contract_detector


@pytest.fixture()
def request_contract_client() -> RequestContractClient:
    request_contract_client = AsyncMock()
    request_contract_client.get_by_address = AsyncMock(
        return_value=ContractResponse(
            status="1", message="OK", contract_name="", result=OKResult(source_code="")
        )
    )

    return request_contract_client


@pytest.fixture()
def source_code_compiler() -> SourceCodeCompiler:
    compiler = AsyncMock()
    compiler.get_source_code_signatures = AsyncMock()

    return compiler


@pytest.fixture()
def contract_service() -> ContractService:
    contract_service = AsyncMock()
    contract_service.create_contract = AsyncMock(
        return_value=Contract(
            id=CONTRACT_ID,
            contract_address=CONTRACT_ADDRESS,
            contract_name="",
            source_code="",
            is_erc20=False,
            erc20_version=None,
            status=ProcessingStatus.WAITS_PROCESSING.value,
        ),
    )
    return contract_service
