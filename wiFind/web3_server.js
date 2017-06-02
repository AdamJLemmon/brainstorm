// server web3 over rpc to connect with python server
var zerorpc = require("zerorpc");

// connect to eth network, local geth node for testing
var Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

console.log("Web3 is connected: " + web3.isConnected())


var server = new zerorpc.Server({
    executeMethod: function(method, params, reply) {
        console.log("Executing method: " + method + ", params: " + String(params))
        
        // response to return following method call
        var res;

        // if there are params call method with them otherwise call with no params
        if (typeof param != undefined)
          res = eval(method)(params);
        else
          res = eval(method)();

        console.log(method + " response: "+ res)
        reply(null, res);
    },

    sayHello: function(reply){
      console.log('hello!!')
      reply(null, 'hello')
    }
});

var url = "tcp://0.0.0.0:4242"

server.bind(url);
console.log("Zerorpc listening on: " + url)


// **************************
// ******* USER ACCOUNT *****
// **************************
function create_account(password){
  // create new account with given password, do not forget this!
  var address = web3.personal.newAccount(password)

  console.log('New account created: ' + address);
  return address;
}


// **************************
// ******* NODE *************
// **************************
// deploy a new node contract, requires ssid, user addr and password
function deploy_node_contract(params){
    var ssid = params['ssid']
    var account_address = params['eth_account_address']
    var password = params['password']

    console.log('Deply Node!')

    // unlock the user account
    web3.personal.unlockAccount(account_address, password)

    // static interface of contract and data from online compiler
    var interface = 'TBD'
    var data = 'bytes'

    // interface of the contract
    var nodeContract = web3.eth.contract(interface);

    // estimate gas for contract
    var gasEstimate = web3.eth.estimateGas({data: data});

    var node = nodeContract.new(
       {
         from: account_address, 
         data: data,
         gas: gasEstimate*2
       }, function (e, contract){
        return contractDeploymentCallback(e, contract);
     })
}


// ************************
// ****** Helper methods **
// ************************
// callback method for all contract deployments, returns address or error
function contractDeploymentCallback(e, contract){
  if(!e) {
        if(!contract.address) {
          console.log("Contract transaction send: TransactionHash: " + contract.transactionHash + " waiting to be mined...");
          return contract.transactionHash 

        } else {
          console.log("Contract mined! Address: " + contract.address);
          return contract.address
        }

      } // end contract addr if
  else {
    console.log("err: " + e)
    return e
  }
}





























// *********** Device Data Upload **************
// params: data hash, shape
function new_data_upload(params){
  // pull vars out of the params object
  var data_hash = params['data_hash']
  var shape = params['shape']
  var timestamp = params['timestamp']

  // good idea to try call before executing on chain
  // console.log("CALL")
  // console.log(deviceData.new_data_upload.call(data_hash, timestamp, shape))

  console.log("Send transaction")
  var response = deviceData.new_data_upload.sendTransaction(
      data_hash, timestamp, shape, {
                  from:defaultAccount, 
                  data: data,
                  gas: 1000000
                }
      )
  
  return response
}

// ********** Retrieve data hashes ***********
// params: start time, end time
// method requires the user account be permissioned!
function get_uploaded_device_data(params){
  var start_time = params['start_time'] 
  var end_time = params['end_time']

  // good idea to try call before executing on chain
  console.log("CALL")

  var response = deviceData.get_uploads_in_time_interval.call(start_time, end_time)

  // console.log("Send Transaction")
  // var response = deviceData.get_uploads_in_time_interval.sendTransaction(
  //     start_time, end_time, {
  //                 from:defaultAccount, 
  //                 data: data,
  //                 gas: 1000000
  //               }
  //     )
  
  return response
}


// ********* Set permissions ************
// params: user addr, bool
function set_user_permissions(params){
  var user_addr = params['user_addr']
  var permission = params['permission']

  // console.log("CALL:")
  // var response = deviceData.set_user_permissions.call(user_addr, permission)

  console.log('Transaction:')
  var response = deviceData.set_user_permissions.sendTransaction(
      user_addr, permission, {
                  from:defaultAccount, 
                  data: data,
                  gas: 1000000
                }
      )
}


// ************************
// ****** Helper methods **
// ************************


// init the event listeners on the device contract
// object of event: filter
function createEventListeners(events){
  // set up listeners to watch for events within the contract
  // note the function names to watch are the actual events in the contract

  // DATA UPLOAD
  deviceData.newDataUpload().watch(function(error, result) {
    console.log('')
    console.log('********* NEW DATA UPLOAD ************')
    console.log('')

      if (!error)
          console.log(result.args)
      else
        console.log("Err: " + error)
  })


  // USER PERMISSIONS CHANGED
  deviceData.userPermissionsRevised().watch(function(error, result) {
    console.log("********* USER Permission Revised ************")

      if (!error)
          console.log(result.args)
      else
        console.log("Err: " + error)
    })


  // DATA RECEIVED
  deviceData.dataHashesReceived().watch(function(error, result) {
    console.log()
    console.log("********* DATA RECEIVED ************")
    console.log()

      if (!error)
          // return value is the concat string of the hashes 
          console.log(result.args.return_value)
      else
        console.log("Err: " + error)
    })

}
