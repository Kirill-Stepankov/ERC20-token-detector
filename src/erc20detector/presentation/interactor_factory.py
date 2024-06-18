from abc import ABC, abstractmethod
from typing import AsyncContextManager

from erc20detector.application.get_contract import GetContractInteractor
from erc20detector.application.get_contracts import GetContractsInteractor
from erc20detector.application.process_contract import \
    ProcessContractInteractor
from erc20detector.application.upload_contract import UploadContractInteractor


class InteractorFactory(ABC):
    @abstractmethod
    def upload_contract(self) -> AsyncContextManager[UploadContractInteractor]:
        raise NotImplementedError

    @abstractmethod
    def get_contracts(self) -> AsyncContextManager[GetContractsInteractor]:
        raise NotImplementedError

    @abstractmethod
    def get_contract(self) -> AsyncContextManager[GetContractInteractor]:
        raise NotImplementedError

    @abstractmethod
    def process_contract(self) -> AsyncContextManager[ProcessContractInteractor]:
        raise NotImplementedError
