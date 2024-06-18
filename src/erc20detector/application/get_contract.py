from dataclasses import dataclass

from ..domain.contract.entities.contract import Contract
from .common.contract_gateway import ContractGateway
from .common.exceptions import ContractDoesNotExistException
from .common.interactor import Interactor


@dataclass
class GetContractDTO:
    contract_address: str


class GetContractInteractor(Interactor[GetContractDTO, Contract]):
    def __init__(self, contract_gateway: ContractGateway):
        self.contract_gateway = contract_gateway

    async def __call__(self, data: GetContractDTO) -> Contract:
        contract = await self.contract_gateway.get_contract_by_address(
            contract_address=data.contract_address
        )

        if not contract:
            raise ContractDoesNotExistException

        return contract
