// init eth greeter example

function greet_greeter(web3, addr, source){
  var compiled = web3.eth.compile.solidity(source)
  var greeter = web3.eth.contract(compiled.greeter.info.abiDefinition).at(addr)

  // check if code exists and therefore contract alive
  if ("0x" != web3.eth.getCode(addr)){
      console.log(greeter.greet())
  }
  else {
    console.log("Contract has been killed")
  }

}


function kill_greeter(web3, addr, source){
  var compiled = web3.eth.compile.solidity(source)
  var greeter = web3.eth.contract(compiled.greeter.info.abiDefinition).at(addr)

  // check if code exists and therefore contract alive
  if ("0x" != web3.eth.getCode(addr)){
      console.log("Killing Greeter")
      web3.personal.unlockAccount(web3.eth.accounts[0], "geth");
      console.log(greeter.kill.sendTransaction({from: web3.eth.accounts[0]}))
  }
  else {
    console.log("Contract has been killed")
  }
}


function retrieve_compiled_greeter(web3){
  var greeterSource = 'contract mortal { address owner; function mortal() { owner = msg.sender; } function kill() { if (msg.sender == owner) selfdestruct(owner); } } contract greeter is mortal { string greeting; function greeter(string _greeting) public { greeting = _greeting; } function greet() constant returns (string) { return greeting; } }'

  var compiled = web3.eth.compile.solidity(greeterSource)

  return compiled
}

function deploy_greeter(web3, source){
  var _greeting = "Hello World!"
  var compiled = web3.eth.compile.solidity(source)
  // var compiled = retrieve_compiled_greeter(web3)

  var greeterContract = web3.eth.contract(compiled.greeter.info.abiDefinition);

  web3.personal.unlockAccount(web3.eth.accounts[0], "geth");

  var greeter = greeterContract.new(_greeting,{from:web3.eth.accounts[0], data: compiled.greeter.code, gas: 300000}, function(e, contract){
      if(!e) {

        if(!contract.address) {
          console.log("Contract transaction send: TransactionHash: " + contract.transactionHash + " waiting to be mined...");

        } else {
          console.log("Contract mined! Address: " + contract.address);
          console.log(contract);
        }

      }
      else {
        console.log("err: " + e)
      }
  })
}