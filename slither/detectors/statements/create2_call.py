from typing import List, Optional
from slither.core.cfg.node import NodeType, Node
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import LowLevelCall, InternalCall
from slither.core.declarations import Contract
from slither.core.variables.local_variable import LocalVariable
from slither.utils.output import Output
from slither.core.declarations import SolidityFunction
from slither.slithir.operations import SolidityCall
from slither.slithir.operations import NewContract

deterministic_func = [
    SolidityFunction("create2(uint256,uint256,uint256,uint256)")
    
]
def detect_create_call(contract: Contract) -> List[Node]:
    results: List[Node] = []
    for f in contract.functions_entry_points:
            nodes = f.all_nodes()
            ops = f.all_slithir_operations()
            [
                            results.append(ir._node)
                            for ir in ops
                            if isinstance(ir, SolidityCall) and ir.function in deterministic_func
                        ]
            [
                            results.append(ir._node)
                            for ir in ops
                            if isinstance(ir, NewContract) ]
            [
                            results.append(ir)
                            for ir in nodes
                            if ir.inline_asm and "create" in ir.inline_asm
                        ]
            

    return results

class CreateCall(AbstractDetector):
    """
    Detect the use of delegatecall inside a loop in a payable function
    """

    ARGUMENT = "create"
    HELP = "Payable functions using `delegatecall` inside a loop"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "Function contain create call to deploy contract"

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
            values = detect_create_call(c)
            for node in values:
                func = node.function

                info = [func, " has create call: ", node, "\n"]
                res = self.generate_result(info)
                results.append(res)

        return results
