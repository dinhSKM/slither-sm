from typing import List, Optional
from slither.core.cfg.node import NodeType, Node
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Contract
from slither.utils.output import Output


def detect_no_modifier(contract: Contract) -> List[Node]:
    results: List[Node] = []
    for f in contract.functions_entry_points:
        if f.is_empty is not None:
            if f.name not in ["constructor", "initialize", "fallback", "receivce"] and f.visibility in ["public", "external"] and f.modifiers == [] and not f.pure and not f.view:
                results.append(f.entry_point)
    return results


class NoModifier(AbstractDetector):
    """
    Detect the use of delegatecall inside a loop in a payable function
    """

    ARGUMENT = "no-modifier"
    HELP = "Payable functions using `delegatecall` inside a loop"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "Function is public/external but without modifiers"

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
            values = detect_no_modifier(c)
            for node in values:
                func = node.function

                info = ["Function ", func,
                        " is public/external but no modifiers: ", node, "\n"]
                res = self.generate_result(info)
                results.append(res)

        return results
