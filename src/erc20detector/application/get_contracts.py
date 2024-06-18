from dataclasses import dataclass

from ..domain.contract.entities.contract import Contract
from ..domain.contract.value_objects.processing_status import ProcessingStatus
from .common.contract_gateway import ContractGateway
from .common.dto import Pagination
from .common.interactor import Interactor


@dataclass
class GetContractsDTO:
    status: ProcessingStatus | None
    pagination: Pagination


@dataclass
class ContractsResultDTO:
    total: int
    contracts: list[Contract]


class GetContractsInteractor(Interactor[GetContractsDTO, ContractsResultDTO]):
    def __init__(self, contract_gateway: ContractGateway):
        self.contract_gateway = contract_gateway

    async def __call__(self, data: GetContractsDTO) -> ContractsResultDTO:
        total = await self.contract_gateway.total_contracts(status=data.status)
        contracts = await self.contract_gateway.find_contracts(
            status=data.status,
            limit=data.pagination.limit,
            offset=data.pagination.offset,
        )
        return ContractsResultDTO(
            total=total,
            contracts=contracts,
        )
