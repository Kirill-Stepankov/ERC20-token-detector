import aiohttp
from aiohttp import ClientSession
from httpx import AsyncClient

from erc20detector.application.common.dto import ContractResponse, OKResult
from erc20detector.application.common.request_contract_client import \
    RequestContractClient
from erc20detector.infrastructure.common.exceptions import \
    HttpConnectionException


class AioHTTPRequestContractClient(RequestContractClient):

    def __init__(self, api_key: str, http_session: ClientSession):
        self._url = "https://api.etherscan.io/api"
        self._api_key = api_key
        self._http_session = http_session

    async def get_by_address(self, contract_address: str) -> ContractResponse:
        query_params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": contract_address,
            "apikey": self._api_key,
        }
        try:
            async with self._http_session.get(
                self._url, params=query_params
            ) as response:

                contract_json = await response.json()

                contract_name = None
                if isinstance(contract_json["result"], str):
                    result = contract_json["result"]
                else:
                    result = OKResult(
                        source_code=contract_json["result"][0]["SourceCode"]
                    )
                    contract_name = contract_json["result"][0].get("ContractName")

                return ContractResponse(
                    status=contract_json["status"],
                    message=contract_json["message"],
                    result=result,
                    contract_name=contract_name,
                )
        except aiohttp.ClientConnectorError:
            raise HttpConnectionException
