from dataclasses import dataclass

from erc20detector.application.common.contract_detector import ContractDetector
from erc20detector.application.common.contract_gateway import ContractGateway
from erc20detector.application.common.exceptions import (
    AlreadyProcessedException, CompilationProcessException,
    ContractDoesNotExistException, InvalidSourceCodeException)
from erc20detector.application.common.source_code_compiler import \
    SourceCodeCompiler
from erc20detector.application.common.uow import UoW
from erc20detector.domain.contract.value_objects.processing_status import \
    ProcessingStatus

from .common.interactor import Interactor


@dataclass
class ProcessContractDTO:
    contract_address: str


@dataclass
class ProcessContractResultDTO:
    contract_address: str
    is_erc20: bool
    erc20_version: str


class ProcessContractInteractor(
    Interactor[ProcessContractDTO, ProcessContractResultDTO]
):
    def __init__(
        self,
        source_code_compiler: SourceCodeCompiler,
        contract_gateway: ContractGateway,
        contract_detector: ContractDetector,
        uow: UoW,
    ):
        self._contract_gateway = contract_gateway
        self._source_code_compiler = source_code_compiler
        self._contract_detector = contract_detector
        self._uow = uow

    async def __call__(self, data: ProcessContractDTO) -> ProcessContractResultDTO:
        contract = await self._contract_gateway.get_contract_by_address(
            data.contract_address
        )

        if contract.status != ProcessingStatus.WAITS_PROCESSING.value:
            raise AlreadyProcessedException

        if not contract:
            raise ContractDoesNotExistException

        try:
            source_code_signatures = (
                await self._source_code_compiler.get_source_code_signatures(
                    contract.source_code, contract.contract_name
                )
            )
        except (InvalidSourceCodeException, CompilationProcessException) as e:
            await self._contract_gateway.update_contract(
                contract_address=contract.contract_address,
                status=ProcessingStatus.FAILED.value,
            )
            await self._uow.commit()
            raise e.__class__ from e

        is_contract_detected = await self._contract_detector.is_contract_detected(
            source_code_signatures
        )

        await self._contract_gateway.update_contract(
            contract_address=contract.contract_address,
            status=ProcessingStatus.PROCESSED.value,
            is_erc20=is_contract_detected,
        )

        await self._uow.commit()

        return ProcessContractResultDTO(
            contract_address=contract.contract_address,
            is_erc20=is_contract_detected,
            erc20_version=None,
        )
