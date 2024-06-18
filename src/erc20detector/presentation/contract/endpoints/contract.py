from fastapi import APIRouter, Depends, Query
from pydantic import Field

from erc20detector.application.common.dto import Pagination
from erc20detector.application.get_contract import GetContractDTO
from erc20detector.application.get_contracts import (ContractsResultDTO,
                                                     GetContractsDTO)
from erc20detector.application.process_contract import (
    ProcessContractDTO, ProcessContractResultDTO)
from erc20detector.application.upload_contract import UploadContractDTO
from erc20detector.domain.contract.entities.contract import Contract
from erc20detector.domain.contract.value_objects.processing_status import \
    ProcessingStatus
from erc20detector.presentation.interactor_factory import InteractorFactory

from ..schemas.contract import UploadContractSchema

contract_router = APIRouter(
    tags=["contracts"],
    responses={404: {"description": "Not found"}},
)


@contract_router.post("/upload")
async def upload_contract(
    data: UploadContractSchema,
    ioc: InteractorFactory = Depends(),
) -> Contract:
    async with ioc.upload_contract() as interactor:
        response = await interactor(
            UploadContractDTO(contract_address=data.contract_address)
        )

        return response


@contract_router.get("/contracts")
async def get_contracts(
    status: ProcessingStatus | None = Query(
        None, description="Select processing status"
    ),
    limit: int = 20,
    offset: int = 0,
    ioc: InteractorFactory = Depends(),
) -> ContractsResultDTO:
    async with ioc.get_contracts() as interactor:
        response = await interactor(
            GetContractsDTO(
                status=status,
                pagination=Pagination(limit=limit, offset=offset),
            )
        )

    return response


@contract_router.get("/contracts/{contract_address}")
async def get_contract(
    contract_address: str,
    ioc: InteractorFactory = Depends(),
) -> Contract:
    async with ioc.get_contract() as interactor:
        response = await interactor(GetContractDTO(contract_address=contract_address))

    return response


@contract_router.post("/contracts/{contract_address}/process")
async def process_contract(
    contract_address: str,
    ioc: InteractorFactory = Depends(),
) -> ProcessContractResultDTO:
    async with ioc.process_contract() as interactor:
        response = await interactor(
            ProcessContractDTO(contract_address=contract_address)
        )

    return response
