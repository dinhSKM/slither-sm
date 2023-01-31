pragma solidity 0.4.24;

contract MyContract {
    function myfunc() public {
        require(1 == 1, "aaaa");
    }

    function myPrivateFunc() private {}
}
