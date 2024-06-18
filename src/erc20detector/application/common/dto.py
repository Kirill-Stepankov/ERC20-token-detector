from dataclasses import dataclass


@dataclass
class OKResult:
    source_code: str


@dataclass
class ContractResponse:
    status: str
    message: str
    result: OKResult | str
    contract_name: str | None


@dataclass
class Pagination:
    limit: int
    offset: int


@dataclass
class InputOutput:
    name: str
    type: str

    def __eq__(self, value) -> bool:
        if isinstance(value, InputOutput):
            return self.type == value.type
        return False


@dataclass
class ContractSignature:
    method_name: str
    inputs: list[InputOutput]
    outputs: list[InputOutput]

    def __eq__(self, value) -> bool:
        if isinstance(value, ContractSignature):
            if len(self.inputs) != len(value.inputs) and len(self.outputs) != len(
                value.outputs
            ):
                return False

            return (
                self.method_name == value.method_name
                and all([input_output in value.inputs for input_output in self.inputs])
                and all(
                    [input_output in value.outputs for input_output in self.outputs]
                )
            )
        return False
