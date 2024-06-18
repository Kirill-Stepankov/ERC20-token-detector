import re

import solcx
import solcx.exceptions

from erc20detector.application.common.dto import ContractSignature, InputOutput
from erc20detector.application.common.exceptions import (
    CompilationProcessException, InvalidSourceCodeException)
from erc20detector.application.common.source_code_compiler import \
    SourceCodeCompiler


class SourceCodeCompilerImpl(SourceCodeCompiler):
    async def get_source_code_signatures(
        self, source_code: str, contract_name: str
    ) -> list[ContractSignature]:
        pragma_index = source_code.find("pragma solidity")
        if pragma_index == -1:
            raise InvalidSourceCodeException

        semicolon_index = source_code.find(";", pragma_index)
        if semicolon_index == -1:
            raise InvalidSourceCodeException

        version_line = source_code[pragma_index : semicolon_index + 1]
        version = self.find_version_pattern(version_line)[0]

        solcx.set_solc_version(version)

        try:
            compiled_sol = solcx.compile_source(source_code)
        except solcx.exceptions.SolcError:
            raise CompilationProcessException
        abi = compiled_sol[f"<stdin>:{contract_name}"]["abi"]

        functions = [item for item in abi if item["type"] == "function"]
        events = [item for item in abi if item["type"] == "event"]

        return [
            ContractSignature(
                method_name=signature["name"],
                inputs=[
                    InputOutput(name=input_output["name"], type=input_output["type"])
                    for input_output in signature.get("inputs", [])
                ],
                outputs=[
                    InputOutput(name=input_output["name"], type=input_output["type"])
                    for input_output in signature.get("outputs", [])
                ],
            )
            for signature in functions + events
        ]

    def find_version_pattern(self, text):
        pattern = r"\b\d+\.\d+\.\d+\b"

        matches = re.findall(pattern, text)

        return matches
