from erc20detector.domain.contract.entities.contract import (Contract,
                                                             ContractId)
from erc20detector.infrastructure.db.models.contract import ContractModel


def contract_model_to_entity(contract: ContractModel) -> Contract:
    return Contract(
        id=ContractId(contract.id),
        contract_address=contract.contract_address,
        is_erc20=contract.is_erc20,
        erc20_version=contract.erc20_version,
        status=contract.status,
        source_code=contract.source_code,
        contract_name=contract.contract_name,
    )


def contract_entity_to_model(contract: Contract) -> ContractModel:
    return ContractModel(
        id=contract.id.value,
        contract_address=contract.contract_address,
        is_erc20=contract.is_erc20,
        erc20_version=contract.erc20_version,
        status=contract.status.name,
        source_code=contract.source_code,
        contract_name=contract.contract_name,
    )
