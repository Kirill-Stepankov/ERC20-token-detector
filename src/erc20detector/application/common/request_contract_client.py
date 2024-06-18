from abc import abstractmethod
from typing import Protocol

from .dto import ContractResponse


class RequestContractClient(Protocol):

    @abstractmethod
    async def get_by_address(self, contract_address: str) -> ContractResponse:
        raise NotImplementedError
