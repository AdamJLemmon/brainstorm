
// create and deploy bet contract on start
$("#start-highlow").on('click', function () {
    var bet_amount = $("#bet_amount").val()

    $.ajax({
        url: '/read_highlow_contract',
        data: {},
        dataType: 'json',
        success: function (data) {
            // console.log(data['data'])
            deployBet(window.web3, data['data'], bet_amount)
        } // success fn
    }); // ajax req
});


// call the deployed contract in order to generate cards
$("#next_card").on('click', function () {

    $.ajax({
        url: '/read_highlow_contract',
        data: {},
        dataType: 'json',
        success: function (data) {
            // console.log(data['data'])
            getNextCard(window.web3, "0xcb4647b0182ac4080e2afe7415709bf265b46cff", data['data'], "0xebce491de02237fdf569f4a328b51ba60ea0f797", "geth")
        } // success fn
    }); // ajax req
});


function deployBet(web3, source, bet_amount){
  var compiled = web3.eth.compile.solidity(source)

  console.log(compiled)

  var betContract = web3.eth.contract(compiled.HighLowBet.info.abiDefinition);

  // TODO need to get actual user's account
  // unlock account to deploy contract
  web3.personal.unlockAccount("0xebce491de02237fdf569f4a328b51ba60ea0f797", "geth");

  // vars to instantiate contract with
  var ltAddress = web3.eth.accounts[0]
  var userAddress = "0xebce491de02237fdf569f4a328b51ba60ea0f797"

  var bet = betContract.new(ltAddress, userAddress, bet_amount, {from:web3.eth.accounts[0], data: compiled.HighLowBet.code, gas: 3000000}, function(e, contract){
      if(!e) {

        if(!contract.address) {
          console.log("Bet transaction send: TransactionHash: " + contract.transactionHash + " waiting to be mined...");

        } else {
          console.log("Bet mined! Address: " + contract.address);
        }

      }
      else {
        console.log("err: " + e)
      }
  })
}


function getNextCard(web3, betAddr, betSource, accountAddr, pword){
  // compile to get abi def
  var compiled = web3.eth.compile.solidity(betSource)
  
  // unlock user account and set default
  web3.personal.unlockAccount(accountAddr, pword);
  web3.personal.unlockAccount(web3.eth.accounts[0], pword);
  web3.eth.defaultAccount = web3.eth.accounts[0]

  console.log("unlocked")

  var bet = web3.eth.contract(compiled.HighLowBet.info.abiDefinition).at(betAddr)

  // web3.personal.unlockAccount(web3.eth.accounts[0], "geth");
  // console.log("Card Transaction: " + bet.generate_card().toString(10))

	bet.generate_card(function(e, contract){
      if(!e) {
        console.log(bet.generate_card.call()['c'][0])
      }
      else{
      	console.log('err: ' + e)
      }
  }) // bet.generate_card
}