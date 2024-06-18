from erc20detector.application.common.contract_detector import ContractDetector
from erc20detector.application.common.dto import ContractSignature
from erc20detector.infrastructure.contract_detector.erc20.erc20_protocol import \
    erc20_protocol


class Erc20ContractDetectorImpl(ContractDetector):
    async def is_contract_detected(self, data: list[ContractSignature]) -> bool:
        return all([signature in data for signature in erc20_protocol])
