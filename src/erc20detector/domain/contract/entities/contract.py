from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from ..value_objects.processing_status import ProcessingStatus


@dataclass(frozen=True)
class ContractId:
    value: UUID


@dataclass
class Contract:
    id: ContractId
    contract_address: str
    contract_name: str
    source_code: str
    is_erc20: bool | None
    erc20_version: str | None
    status: ProcessingStatus
