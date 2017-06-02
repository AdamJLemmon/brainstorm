pragma solidity ^0.4.6;

// importing lib for string concat
import "github.com/Arachnid/solidity-stringutils/strings.sol";

contract permissionedData {
    /* Define variable owner of the type address*/
    address owner;

    /* define address of device account this contract belongs to */
    address device_addr;

    // List of addresses that may access data
    mapping (address => bool) permissioned_users;

    /* this function is executed at initialization and sets the owner of the contract */
    function permissionedData() { owner = msg.sender; }

    // allow method to be called only by owner of contract
    modifier onlyOwner {
        if (msg.sender != owner) throw;
        _;
    }

    // allow method to be called only by the registered device
    modifier onlyDevice {
        if (msg.sender != device_addr) throw;
        _;
    }

    // allow methods to be called only by addresses that have been given permission
    modifier ifPermissioned {
        // throw error if the address has not been given permission
        if (!permissioned_users[msg.sender]) throw;
        _;
    }
}

contract dataHistory is permissionedData {
    // importing library for string concat
    using strings for *;

    // an array to hold reference to all data uploaded by device
    dataUpload[] uploaded_data;

    // object for each data upload, hold reference to data and timestamp
    struct dataUpload {
        string data_hash;
        uint timestamp;
        uint[] shape;
    }

    event newDataUpload(address device_addr, string data_hash, uint timestamp, uint upload_array_length);
    event userPermissionsRevised(address device_addr, address user_address, bool permission);
    event dataHashesReceived(address device_addr, address user_address, string return_value);

    // *******************
    // *** CONSTRUCTOR ***
    // *******************
    // init with the device address the contract belongs to
    function dataHistory(address _addr) public {
        device_addr = _addr;

        // give the owner permission initially
        permissioned_users[msg.sender] = true;
    }

    // *******************
    // ***** METHODS *****
    // *******************
    // device has uplaoded new data to storage, save hash and timestamp
    // function new_data_upload(string data_hash, uint timestamp, uint[] shape) onlyDevice returns (uint) {
    function new_data_upload(string data_hash, uint timestamp, uint[] shape) returns (uint) {
        uploaded_data.push(dataUpload(data_hash, timestamp, shape));

        // trigger event to monitor all data uploaded by device
        newDataUpload(device_addr, data_hash, timestamp, uploaded_data.length);
    }

    /* return the list of uploaded data within time frame */
    function get_uploads_in_time_interval(uint start_time, uint stop_time) ifPermissioned returns (string data_hash_string) {
    // function get_uploads_in_time_interval(uint start_time, uint stop_time) returns (string data_hash_string) {
        // hold value of hashes to concat
        string new_hash;

        // loop over uploaded data structs and return those that fall within time interval
        for (uint i = 0; i < uploaded_data.length; i++) {

            // if within time intervall aggregate with current string
            if (uploaded_data[i].timestamp > start_time && uploaded_data[i].timestamp < stop_time){

                // add comma then new hash in order to deconstruct on other end
                data_hash_string = data_hash_string.toSlice().concat(",".toSlice());

                // hash of uploaded data to be returned
                new_hash = uploaded_data[i].data_hash;

                // final concat after comma with new data
                data_hash_string = data_hash_string.toSlice().concat(new_hash.toSlice());
            }
        } // for loop end

        // trigger event to notify data has been pulled
        dataHashesReceived(device_addr, msg.sender, data_hash_string);

    } // get upload func end


    // *******************
    // ***** OWNER *******
    // *******************

    // owner may grant access to other addresses in order to view data
    function set_user_permissions(address user_address, bool permission) onlyOwner returns (bool) {
        permissioned_users[user_address] = permission;

        // event to monitor status of permissions
        userPermissionsRevised(device_addr, user_address, permission);

        return permissioned_users[user_address];
    }

    /* return the address of assoicated device */
    function get_device_addr() onlyOwner constant returns (address) {
        return device_addr;
    }

    /* Function to recover the funds on the contract */
    function kill() onlyOwner { if (msg.sender == owner) selfdestruct(owner); }



}