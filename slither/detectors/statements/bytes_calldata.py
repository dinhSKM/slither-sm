from typing import List, Optional
from slither.core.cfg.node import NodeType, Node
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import LowLevelCall, InternalCall
from slither.core.declarations import Contract
from slither.core.variables.local_variable import LocalVariable
from slither.utils.output import Output

Byte = [
    "byte",
    "bytes",
    "bytes32[]",
    "bytes1",
    "bytes2",
    "bytes3",
    "bytes4",
    "bytes5",
    "bytes6",
    "bytes7",
    "bytes8",
    "bytes9",
    "bytes10",
    "bytes11",
    "bytes12",
    "bytes13",
    "bytes14",
    "bytes15",
    "bytes16",
    "bytes17",
    "bytes18",
    "bytes19",
    "bytes20",
    "bytes21",
    "bytes22",
    "bytes23",
    "bytes24",
    "bytes25",
    "bytes26",
    "bytes27",
    "bytes28",
    "bytes29",
    "bytes30",
    "bytes31",
    "bytes32",
    "bytes1[]",
    "bytes2[]",
    "bytes3[]",
    "bytes4[]",
    "bytes5[]",
    "bytes6[]",
    "bytes7[]",
    "bytes8[]",
    "bytes9[]",
    "bytes10[]",
    "bytes11[]",
    "bytes12[]",
    "bytes13[]",
    "bytes14[]",
    "bytes15[]",
    "bytes16[]",
    "bytes17[]",
    "bytes18[]",
    "bytes19[]",
    "bytes20[]",
    "bytes21[]",
    "bytes22[]",
    "bytes23[]",
    "bytes24[]",
    "bytes25[]",
    "bytes26[]",
    "bytes27[]",
    "bytes28[]",
    "bytes29[]",
    "bytes30[]",
    "bytes32[]",
    "bytes31[]",
]

def detect_byte_data(contract: Contract) -> List[Node]:
    results: List[Node] = []
    for f in contract.functions_entry_points:
        if f.visibility in ["public", "external"]:
            results += [ p for p in f.parameters if (str(p.type) in Byte) and (p.location in ['calldata', 'memory', 'storage']) ]
            for n in f.all_nodes():
                if n.variable_declaration and str(n.variable_declaration.type) in Byte: 
                    if n.variable_declaration.location in ['calldata', 'memory', 'storage']:
                        results.append(n)

    return results

class BytesCalldata(AbstractDetector):
    """
    Detect the use of delegatecall inside a loop in a payable function
    """

    ARGUMENT = "bytes-calldata"
    HELP = "Payable functions using `delegatecall` inside a loop"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "Public/External function contain bytes declare"

    WIKI_TITLE = "Payable functions using `delegatecall` inside a loop"
    WIKI_DESCRIPTION = "Detect the use of `delegatecall` inside a loop in a payable function."

    # region wiki_exploit_scenario
    WIKI_EXPLOIT_SCENARIO = """
```solidity
contract DelegatecallInLoop{

    mapping (address => uint256) balances;

    function bad(address[] memory receivers) public payable {
        for (uint256 i = 0; i < receivers.length; i++) {
            address(this).delegatecall(abi.encodeWithSignature("addBalance(address)", receivers[i]));
        }
    }

    function addBalance(address a) public payable {
        balances[a] += msg.value;
    } 

}
```
When calling `bad` the same `msg.value` amount will be accredited multiple times."""
    # endregion wiki_exploit_scenario

    WIKI_RECOMMENDATION = """
Carefully check that the function called by `delegatecall` is not payable/doesn't use `msg.value`.
"""

    def _detect(self) -> List[Output]:
        """"""
        results: List[Output] = []
        for c in self.compilation_unit.contracts_derived:
            values = detect_byte_data(c)
            for node in values:
                func = node.function

                info = [func, " has bytes declaration in public/external function: ", node, "\n"]
                res = self.generate_result(info)
                results.append(res)

        return results
