var zerorpc = require("zerorpc");
var Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

// server object to expose web3 methods to python
var server = new zerorpc.Server({

	hello: function(reply){
		console.log('hello')
		reply(null, "hello")
	},

    // create a new eth account, requires a password
    createNewAccount: function(password, reply){
    	console.log('Creating new eth account')
    	var address = web3.personal.newAccount(password);
    	reply(null, address);
    },

    deployDeviceContract: function(deviceAddress, contractSource, ownerAccount, ownerPassword, reply){
    	console.log('deploying contract')
    	var compiled = web3.eth.compile.solidity(contractSource)

		  var deviceContract = web3.eth.contract(compiled.Device.info.abiDefinition);

		  // unlock account to deploy contract
		  web3.personal.unlockAccount(ownerAccount, ownerPassword);

		  // estimate gas for contract
		  var gasEstimate = web3.eth.estimateGas({data: compiled.Device.code});
		  console.log('gas Estimate ' + gasEstimate);

		  // deploy contract from owner account unlocked
		  var device = deviceContract.new(deviceAddress, {from:ownerAccount, data: compiled.Device.code, gas: 3000000000}, function(e, contract){
		      if(!e) {
		        if(!contract.address) {
		          console.log("Contract transaction send: TransactionHash: " + contract.transactionHash + " waiting to be mined...");
		          // reply("Contract transaction sent, waiting to be mined...");
		        } else {
		          console.log("Contract mined! Address: " + contract.address);

		          // return contract address
		          reply(null, contract.address);
		        }

		      }
		      else {
		        console.log("err: " + e)
		        reply("err:" + e)
		      }
		  })
    },

    retrieveContract: function(source, contractName, addr){
    	var compiled = web3.eth.compile.solidity(source)
  		var contract = web3.eth.contract(compiled[contractName].info.abiDefinition).at(source)

  		return contract
    },

    killContract: function(){

    },

    pushDatatoContract: function(deviceAddress, contractSource, contractAddress, data, reply){
    	console.log('Pushing new data: ' + data + ' ' + deviceAddress)
    	var device = this.retrieveDeviceContract(contractSource, contractAddress)

    	// unlock account to deploy contract
	  	web3.personal.unlockAccount(web3.eth.accounts[0], "geth");

    	console.log('returning contract')

    	web3.eth.defaultAccount = web3.eth.accounts[0]

    	// console.log(device)
    	console.log(device.hello())

    	reply(null, 'success')
    },

    deployContract: function(contractSource, contractName, ownerAccount, ownerPassword, params, reply){
    	console.log('Deploying contract: ' + contractName)
    	var compiled = web3.eth.compile.solidity(contractSource)
		var contract = web3.eth.contract(compiled[contractName].info.abiDefinition);

		// unlock account to deploy contract
		web3.personal.unlockAccount(ownerAccount, ownerPassword);

		// estimate gas for contract
		var gasEstimate = web3.eth.estimateGas({data: compiled[contractName].code});
		console.log('gas Estimate ' + gasEstimate);

		// deploy contract from owner account unlocked
		var deployedContract = contract.new({from:ownerAccount, data: compiled[contractName].code, gas: gasEstimate*1.5}, 
			function(e, contract){
				contractDeploymentCallback(e, contract, reply)
		})
    },

    callContractMethod: function(source, name, addr, methodName, params, reply){
    	var response;

    	// compile suorce to find abi definition
    	var compiled = web3.eth.compile.solidity(source)

    	console.log("Method: " + methodName)

    	// retrieve contract object
		var contract = web3.eth.contract(compiled[name].info.abiDefinition).at(addr)

		web3.eth.defaultAccount = web3.eth.accounts[0];

		// exec the string passed in an method
		if (params)
			response = contract[methodName](params);
		else
			response = contract[methodName]();

		console.log(response)
		reply(null, response)
	}
    
});


// callback method for all contract deployments, returns address or error
function contractDeploymentCallback(e, contract, reply){
	if(!e) {
        if(!contract.address) {
          console.log("Contract transaction send: TransactionHash: " + contract.transactionHash + " waiting to be mined...");
          // reply("Contract transaction sent, waiting to be mined...");
        } else {
          console.log("Contract mined! Address: " + contract.address);

          // return contract address
          reply(null, contract.address)
        }

      }
  else {
  	console.log('deploy callback')
    console.log("err: " + e)
    reply(null, e)
  }
}

// parameters to serve the api
var ip = "0.0.0.0";
var port = "4242";

server.bind("tcp://"+ ip +":"+ port);
console.log("Web3 Server running at: tcp://"+ ip +":"+ port);

// Error reporting for api server
server.on("error", function(error) {
    console.error("Web3 API RPC server error:", error);
});