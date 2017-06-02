
console.log("INIT");

var Web3 = require('web3');
var web3 = new Web3();

web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));

var coinbase = web3.eth.coinbase;
var balance = web3.eth.getBalance(coinbase);

console.log("Balances:");
console.log(coinbase)
console.log(balance)



var not_mined = true;
var test_contract;

var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function(){


    if(xmlhttp.status == 200 && xmlhttp.readyState == 4){
        var source = xmlhttp.responseText;
        console.log(source);
        var compiled = web3.eth.compile.solidity(source);
        console.log(compiled);

        web3.personal.unlockAccount(web3.eth.accounts[0], "geth");

        web3.eth.defaultAccount = web3.eth.accounts[0];

        test_contract = web3.eth.contract(compiled.test.info.abiDefinition);

        //var test_contract_instance = test_contract.at(web3.eth.coinbase);

        var Test = test_contract.new({from: web3.eth.accounts[0], data: compiled.test.code, gas: 300000}, function(e, contract){
            if(!e) {
                if(!contract.address) {
                    console.log("Contract transaction send: TransactionHash: " + contract.transactionHash + " waiting to be mined...");

                } else {

                    console.log("Contract mined! Address: " + contract.address);
                    console.log(contract);
                    not_mined = false;

                    console.log("OUTPUT:");
                    console.log(contract.multiply.call(10));

                }
            }
            else {
              console.log("err: " + e)
            }
        })
    }
};
xmlhttp.open("GET","read_contract",true);
xmlhttp.send();


