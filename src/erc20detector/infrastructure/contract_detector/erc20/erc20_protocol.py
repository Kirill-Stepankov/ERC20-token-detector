from erc20detector.application.common.dto import ContractSignature, InputOutput

erc20_protocol = [
    ContractSignature(
        method_name="name", inputs=[], outputs=[InputOutput(name="", type="string")]
    ),
    ContractSignature(
        method_name="symbol", inputs=[], outputs=[InputOutput(name="", type="string")]
    ),
    ContractSignature(
        method_name="decimals", inputs=[], outputs=[InputOutput(name="", type="uint8")]
    ),
    ContractSignature(
        method_name="totalSupply",
        inputs=[],
        outputs=[InputOutput(name="", type="uint256")],
    ),
    ContractSignature(
        method_name="balanceOf",
        inputs=[InputOutput(name="_owner", type="address")],
        outputs=[InputOutput(name="balance", type="uint256")],
    ),
    ContractSignature(
        method_name="transfer",
        inputs=[
            InputOutput(name="_to", type="address"),
            InputOutput(name="_value", type="uint256"),
        ],
        outputs=[InputOutput(name="success", type="bool")],
    ),
    ContractSignature(
        method_name="transferFrom",
        inputs=[
            InputOutput(name="_to", type="address"),
            InputOutput(name="_from", type="address"),
            InputOutput(name="_value", type="uint256"),
        ],
        outputs=[InputOutput(name="success", type="bool")],
    ),
    ContractSignature(
        method_name="approve",
        inputs=[
            InputOutput(name="_spender", type="address"),
            InputOutput(name="_value", type="uint256"),
        ],
        outputs=[InputOutput(name="success", type="bool")],
    ),
    ContractSignature(
        method_name="allowance",
        inputs=[
            InputOutput(name="_owner", type="address"),
            InputOutput(name="_spender", type="address"),
        ],
        outputs=[InputOutput(name="remaining", type="uint256")],
    ),
    ContractSignature(
        method_name="Transfer",
        inputs=[
            InputOutput(name="_from", type="address"),
            InputOutput(name="_to", type="address"),
            InputOutput(name="_value", type="uint256"),
        ],
        outputs=[],
    ),
    ContractSignature(
        method_name="Transfer",
        inputs=[
            InputOutput(name="_owner", type="address"),
            InputOutput(name="_spender", type="address"),
            InputOutput(name="_value", type="uint256"),
        ],
        outputs=[],
    ),
]
