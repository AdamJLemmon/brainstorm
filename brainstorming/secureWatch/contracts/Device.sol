pragma solidity ^0.4.6;

// contract permissioned {
//     /* Define variable owner of the type address*/
//     address owner;
//     string public device_addr;

//     /* this function is executed at initialization and sets the owner of the contract */
//     function permissioned() { owner = msg.sender; }

//     /* Function to recover the funds on the contract */
//     function kill() { if (msg.sender == owner) selfdestruct(owner); }

//     // allow method to be called only by owner of contract
//     modifier onlyOwner {
//         if (msg.sender != owner) throw;
//         _;
//     }

//     // allow method to be called only by the registered device
//     modifier onlyDevice {
//         // if (msg.sender != device_addr) throw;
//         // _;
//     }
// }

contract device {
    // address owner;

    /* this function is executed at initialization and sets the owner of the contract */
    function device() { 
        // owner = msg.sender; 
    }

    // function set_device_address(address addr) {
    //     device_addr = addr;
    // }

    // function device_address() constant returns (address device_addr) {
    //     // return device_addr;
    // }
}



// contract Device is permissioned {
//     // address of manager that tracks status of devices
//     // address public manager_address;
//     uint8[] public data_array;
//     string public test;

//     /* This generates a public event on the blockchain that will notify clients */
//     event DeviceRegistered(address device_address);

//     /* Initializes contract with addresses amount and card number of 0 */
//     function Device(
//         // address manager_address,
//         address device_address
//         ) {

//         // address to update and that maintains collection of devices
//         // manager_address = manager_address; 

//         // address of the devices external account
//         device = device_address;
//         test = "hello";

//         DeviceRegistered(device_address);
//     }

//     function hello() returns (string greeting) {
//         return 'hello';
//     }

//     function push_data(uint8 data) onlyDevice returns(uint256 length){
//         return data_array.push(data);
//     }

//     /* Function to recover the funds on the contract */
//     function kill() onlyOwner { selfdestruct(owner); }

//     /* This unnamed function is called whenever someone tries to send ether to it */
//     function () {
//         throw;     // Prevents accidental sending of ether
//     }
// }