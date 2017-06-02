pragma solidity ^0.4.6;

contract permissioned {
    /* Define variable owner of the type address*/
    address owner;
    address permissioned_device;

    /* this function is executed at initialization and sets the owner of the contract */
    function permissioned() { 
        // the creater of contractor is owner and has permissions
        owner = msg.sender; 
    }

    // allow method to be called only by owner of contract
    modifier onlyOwner {
        if (msg.sender != owner) throw;
        _;
    }

    // allow method to be called only by the registered device
    modifier onlyPermissionedDevice {
        if (msg.sender != permissioned_device) throw;
        _;
    }

    /* Function to recover the funds on the contract */
    function kill() { if (msg.sender == owner) selfdestruct(owner); }
}

contract device is permissioned {
    string[] public transaction_list;

    function set_device_permission(address _device_addr) onlyOwner public {
        permissioned_device = _device_addr;
    }

    // add hash of data upload to contract list of transactions
    function add_transaction(string data_hash) onlyPermissionedDevice {
        transaction_list.push(data_hash);
    }

    // // return complete list of transactions
    // function get_transaction_list() onlyOwner returns (string[]) {
    //     return transaction_list;
    // }
}