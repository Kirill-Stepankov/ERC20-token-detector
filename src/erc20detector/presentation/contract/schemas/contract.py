from pydantic import BaseModel


class UploadContractSchema(BaseModel):
    contract_address: str
