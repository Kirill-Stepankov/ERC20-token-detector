from abc import abstractmethod
from typing import Protocol

from erc20detector.application.common.dto import ContractSignature


class ContractDetector(Protocol):
    @abstractmethod
    async def is_contract_detected(self, data: list[ContractSignature]) -> bool:
        raise NotImplementedError
