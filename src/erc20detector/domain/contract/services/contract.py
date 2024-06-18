from ..entities.contract import Contract, ContractId
from ..value_objects.processing_status import ProcessingStatus


class ContractService:
    async def create_contract(
        self,
        contract_id: ContractId,
        contract_adddress: str,
        source_code: str,
        contract_name: str,
    ) -> Contract:
        return Contract(
            id=contract_id,
            contract_address=contract_adddress,
            source_code=source_code,
            status=ProcessingStatus.WAITS_PROCESSING,
            is_erc20=None,
            erc20_version=None,
            contract_name=contract_name,
        )

    async def update_contract(
        self, contract: Contract, status: ProcessingStatus
    ) -> None:
        contract.status = status
