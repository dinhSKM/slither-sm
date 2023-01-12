from solc_select import solc_select

from slither import Slither
from slither.core.declarations.function import FunctionType
from slither.core.solidity_types.elementary_type import ElementaryType

def extract():
    solc_select.switch_global_version("0.8.9", always_install=True)
    slither = Slither("/Users/dinh.le/Security/Smart Contract/ronin-dpos-contracts/contracts/ronin/staking/Staking.sol")
    print(slither.contracts)
    # functions = slither.get_contract_from_name("TestFunction")[0].available_functions_as_dict()
    print(slither)

extract()