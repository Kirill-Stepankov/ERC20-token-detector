from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from erc20detector.application.common.contract_gateway import ContractGateway
from erc20detector.domain.contract.entities.contract import (Contract,
                                                             ContractId)
from erc20detector.domain.contract.value_objects.processing_status import \
    ProcessingStatus
from erc20detector.infrastructure.repositories.converters.contract import (
    contract_entity_to_model, contract_model_to_entity)

from ..db.models.contract import ContractModel


class ContractGatewayImpl(ContractGateway):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_contract(self, contract: Contract) -> ContractId:
        db_contract = contract_entity_to_model(contract)

        self.session.add(db_contract)

        await self.session.flush(objects=[db_contract])

        return contract.id

    async def find_contracts(
        self, status: ProcessingStatus | None, limit: int, offset: int
    ) -> list[Contract]:
        q = select(ContractModel)
        if status:
            q = q.where(ContractModel.status == status.value)

        q = q.limit(limit).offset(offset)

        res = await self.session.execute(q)
        contracts: list[ContractModel] = res.scalars()

        if not contracts:
            return []

        return [contract_model_to_entity(contract) for contract in contracts]

    async def get_contract_by_address(self, contract_address: str) -> Contract | None:
        q = select(ContractModel).where(
            ContractModel.contract_address == contract_address
        )

        res = await self.session.execute(q)

        contract: ContractModel | None = res.scalar()

        if not contract:
            return None

        return contract_model_to_entity(contract)

    async def total_contracts(self, status: ProcessingStatus | None) -> int:
        q = select(func.count()).select_from(ContractModel)

        if status:
            q = q.where(ContractModel.status == status.value)

        res = await self.session.execute(q)

        return res.scalar()

    async def update_contract(self, contract_address: str, **kwargs) -> None:
        q = (
            update(ContractModel)
            .where(ContractModel.contract_address == contract_address)
            .values(**kwargs)
        )

        await self.session.execute(q)

    # async def update(self, user_id: UserIdentityId, updated_user: UserEntity) -> None:
    #     q = (
    #         update(UserIdentity)
    #         .where(UserIdentity.identity_id == user_id.to_raw())
    #         .values(is_active=updated_user.is_active)
    #     )

    #     await self.session.execute(q)
