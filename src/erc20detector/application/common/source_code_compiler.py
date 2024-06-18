from abc import abstractmethod
from typing import Protocol

from erc20detector.application.common.dto import ContractSignature


class SourceCodeCompiler(Protocol):
    @abstractmethod
    async def get_source_code_signatures(
        self, source_code: str, contract_name: str
    ) -> list[ContractSignature]:
        raise NotImplementedError
