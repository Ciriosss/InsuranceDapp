pragma solidity ^0.8.0;

contract HAMSAToken {

    string public  name = "HAMSA";
    string public symbol = "HMS";
    uint256 totalSupply = 100000000000;

    event Transfer(address _from,address _to, uint _value);
    event Repayment(address _insured, uint _value);

    mapping(address => uint)Balance;

    constructor() {
        Balance[msg.sender] = totalSupply;
    }

    function supply() public view returns(uint256){
        return totalSupply - Balance[msg.sender];
    }

    function balanceOf() public view returns(uint256){
        return Balance[msg.sender];
    }

    function transferFrom(address _from,address _to, uint256 _value) public returns (bool success){

        require(Balance[_from] > _value , "not enough");
        Balance[_from] -= _value;
        Balance[_to] += _value;
        emit Transfer(_from,_to, _value);
        return true;
    }

    function repayment(address _insured, uint256 _value) public returns (bool success){

        Balance[msg.sender] -= _value;
        Balance[_insured] += _value;
        emit Repayment(_insured, _value);
        return true;
    }
}