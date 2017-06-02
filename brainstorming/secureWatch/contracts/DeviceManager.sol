contract owned {
    address public owner;

    function owned() {
        owner = msg.sender;
    }

    modifier onlyOwner {
        if (msg.sender != owner) throw;
        _;
    }
}

contract DeviceManager is owned {

    mapping (address => string) public deviceStatus;

    function DeviceManager() {
        owner = msg.sender;
    }

    function registerNewDevice(address deviceAddress) onlyOwner {
        deviceStatus[deviceAddress] = "Active";
    }
}