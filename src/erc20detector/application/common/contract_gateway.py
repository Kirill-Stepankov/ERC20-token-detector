from abc import abstractmethod
from typing import Protocol

from erc20detector.domain.contract.entities.contract import (Contract,
                                                             ContractId)
from erc20detector.domain.contract.value_objects.processing_status import \
    ProcessingStatus


class ContractGateway(Protocol):
    @abstractmethod
    async def save_contract(self, contract: Contract) -> ContractId:
        raise NotImplementedError

    @abstractmethod
    async def total_contracts(self, status: ProcessingStatus | None) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_contracts(self, status: ProcessingStatus | None) -> list[Contract]:
        raise NotImplementedError

    @abstractmethod
    async def get_contract_by_address(self, contract_address: str) -> Contract | None:
        raise NotImplementedError

    @abstractmethod
    async def update_contract(self, contract_address: str, **kwargs) -> None:
        raise NotImplementedError
