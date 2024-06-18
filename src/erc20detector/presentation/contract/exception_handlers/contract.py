from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from erc20detector.application.common.exceptions import (
    AlreadyProcessedException, ApplicationException,
    CompilationProcessException, ContractDoesNotExistException,
    ContractIsAlreadyUploadedException, InvalidContractAddressException,
    InvalidSourceCodeException)
from erc20detector.infrastructure.common.exceptions import \
    HttpConnectionException


async def application_exception_handler(
    _request: Request, _exc: ApplicationException
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error."},
    )


async def contract_does_not_exist_handler(
    _request: Request, _exc: ContractDoesNotExistException
) -> JSONResponse:
    return JSONResponse(
        status_code=403,
        content={"message": "Contract does not exist."},
    )


async def invalid_contract_address_handler(
    _request: Request, exc: InvalidContractAddressException
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": "Invalid contract address."},
    )


async def contract_is_already_uploaded_handler(
    _request: Request, _exc: ContractIsAlreadyUploadedException
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"message": "Contract is already uploaded."},
    )


async def invalid_source_code_handler(
    _request: Request, exc: InvalidSourceCodeException
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": "Invalid contract address."},
    )


async def http_connection_exception_handler(
    _request: Request, exc: HttpConnectionException
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"message": "Connection timeout. Please try again."},
    )


async def compilation_errors_handler(
    _request: Request, exc: CompilationProcessException
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"message": "Compilation Error."},
    )


async def already_processed_handler(
    _request: Request, exc: AlreadyProcessedException
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"message": "Source code of the contract is already processed."},
    )


def include_exception_handlers(app: FastAPI) -> None:

    # logging.info("Exception handlers was included.")

    app.add_exception_handler(ApplicationException, application_exception_handler)
    app.add_exception_handler(
        ContractDoesNotExistException, contract_does_not_exist_handler
    )
    app.add_exception_handler(
        InvalidContractAddressException, invalid_contract_address_handler
    )
    app.add_exception_handler(
        ContractIsAlreadyUploadedException, contract_is_already_uploaded_handler
    )
    app.add_exception_handler(InvalidSourceCodeException, invalid_source_code_handler)
    app.add_exception_handler(
        HttpConnectionException, http_connection_exception_handler
    )
    app.add_exception_handler(CompilationProcessException, compilation_errors_handler)
    app.add_exception_handler(AlreadyProcessedException, already_processed_handler)
