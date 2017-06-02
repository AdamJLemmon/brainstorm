// tut #2 from ethereum home

function deploy_token_contract(web3, source){
  var compiled = web3.eth.compile.solidity(source)

  console.log(compiled)

  var tokenContract = web3.eth.contract(compiled.MyToken.info.abiDefinition);

  // unlock account to deploy contract
  web3.personal.unlockAccount(web3.eth.accounts[0], "geth");

  // vars to instantiate contract with
  var initialSupply = 1000000
  var tokenName = "adamCoin"
  var decimalUnits = 2
  var tokenSymbol = "AC"

  var gasEstimate = web3.eth.estimateGas({data: compiled.MyToken.code});
  console.log('gas Estimate '+gasEstimate);

  var token = tokenContract.new(initialSupply, tokenName, decimalUnits, tokenSymbol,{from:web3.eth.accounts[0], data: compiled.MyToken.code, gas: 3000000}, function(e, contract){
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


function getAccountBalance(web3, addr, source, accountAddr){
  var compiled = web3.eth.compile.solidity(source)
  var token = web3.eth.contract(compiled.MyToken.info.abiDefinition).at(addr)

  console.log("Account: " + accountAddr)

  // web3.personal.unlockAccount(web3.eth.accounts[0], "geth");
  console.log("Balance: " + token.balanceOf(accountAddr).toString(10))
}


function transfer(web3, contractAddr, source, fromAddr, toAddr, amount){
  var compiled = web3.eth.compile.solidity(source)
  var token = web3.eth.contract(compiled.MyToken.info.abiDefinition).at(contractAddr)

  console.log(token)

  console.log("To Account: " + toAddr)
  console.log("Amount: " + amount)

  // unlock accont to release tokens and set as default
  web3.personal.unlockAccount(fromAddr, "geth")
  web3.eth.defaultAccount = fromAddr

  console.log(token.transfer.sendTransaction(toAddr, amount))
}