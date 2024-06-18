from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from erc20detector.application.common.exceptions import (
    ContractIsAlreadyUploadedException, InvalidContractAddressException)
from erc20detector.domain.contract.entities.contract import (Contract,
                                                             ContractId)
from erc20detector.domain.contract.services.contract import ContractService

from .common.contract_gateway import ContractGateway
from .common.interactor import Interactor
from .common.request_contract_client import RequestContractClient
from .common.uow import UoW


@dataclass
class UploadContractDTO:
    contract_address: str


class UploadContractInteractor(Interactor[UploadContractDTO, Contract]):
    def __init__(
        self,
        contract_gateway: ContractGateway,
        http_client: RequestContractClient,
        contract_service: ContractService,
        uow: UoW,
    ):
        self.contract_gateway = contract_gateway
        self.http_client = http_client
        self.contract_service = contract_service
        self.uow = uow

    async def __call__(self, data: UploadContractDTO) -> Contract:
        contract = await self.contract_gateway.get_contract_by_address(
            data.contract_address
        )
        if contract:
            raise ContractIsAlreadyUploadedException

        contract_response = await self.http_client.get_by_address(data.contract_address)

        if contract_response.status != "1":
            raise InvalidContractAddressException

        contract_id = ContractId(value=uuid4())

        contract = await self.contract_service.create_contract(
            contract_id=contract_id,
            contract_adddress=data.contract_address,
            source_code=contract_response.result.source_code,
            contract_name=contract_response.contract_name,
        )

        await self.contract_gateway.save_contract(contract)
        await self.uow.commit()

        return contract
