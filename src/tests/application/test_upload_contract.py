from unittest.mock import AsyncMock

from erc20detector.application.upload_contract import (
    UploadContractDTO, UploadContractInteractor)
from erc20detector.domain.contract.entities.contract import Contract
from tests.conftest import CONTRACT_ID


async def test_upload_contract(
    contract_gateway, request_contract_client, uow, contract_service
):
    contract_gateway.get_contract_by_address = AsyncMock(return_value=None)

    usecase = UploadContractInteractor(
        contract_service=contract_service,
        contract_gateway=contract_gateway,
        uow=uow,
        http_client=request_contract_client,
    )

    res = await usecase(UploadContractDTO("0x1212"))

    assert res.id == CONTRACT_ID
