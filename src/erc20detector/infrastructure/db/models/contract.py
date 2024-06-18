from typing import get_args
from uuid import UUID

from sqlalchemy import Boolean, Enum, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from erc20detector.domain.contract.value_objects.processing_status import \
    ProcessingStatus

from .base import Base


class ContractModel(Base):
    __tablename__ = "contract"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    contract_address: Mapped[str] = mapped_column(
        String[200], unique=True, nullable=False
    )
    contract_name: Mapped[str] = mapped_column(String[200], nullable=True)
    source_code = mapped_column(Text, nullable=False)
    is_erc20: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    erc20_version: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[ProcessingStatus] = mapped_column(
        Enum(ProcessingStatus).values_callable
    )
