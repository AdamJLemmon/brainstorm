RUNNING PRIVATE NET:

cd into ../brainstorm/ethereum/


Initialize genesis block:
geth --datadir <some/location/where/to/create/chain> init genesis.json
EX:
geth --datadir /home/mike/.ethereum/mynet/ init genesis.json


Create coinbase account:
geth --datadir <some/location/where/to/create/chain> account new
EX:
geth --datadir /home/mike/.ethereum/mynet/ account new


(copy address with 0x in front to genesis block JSON below)

{
    "coinbase": "0x0000000000000000000000000000000000000000",
    "config": {
      "homesteadBlock": 5
    },
    "difficulty": "0x20000",
    "extraData": "0x",
    "gasLimit": "0x2FEFD8",
    "mixhash": "0x00000000000000000000000000000000000000647572616c65787365646c6578",
    "nonce": "0x0",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "timestamp": "0x00",
    "alloc": {
      "0x + <your coinbase address from account new>": {
          "balance": "100000000"
      },
      "0xfe91a6a5777698167f1dec05eee29a43c136760a": {
          "balance": "100000000"
      }
    }
}

Re-Initialize genesis block:
geth --datadir <some/location/where/to/create/chain> init genesis.json
EX:
geth --datadir /home/mike/.ethereum/mynet/ init genesis.json


Start blockchain (and mine):
geth --datadir <some/location/where/to/create/chain> --mine --rpc --rpcapi "db,eth,net,web3,personal" --rpcport "8545"
EX:
geth --datadir /home/mike/.ethereum/mynet/ --mine --rpc --rpcapi "db,eth,net,web3,personal" --rpcport "8545"


Attach to console:
geth attach <some/location/where/to/create/chain> + /geth.ipc
EX:
geth attach /home/mike/.ethereum/mynet/geth.ipc


TO ONLY USE 1 THREAD: (once in geth console)
miner.stop()
miner.start(1)



USEFUL COMMANDS:

Unlock coinbase account:
web3.personal.unlockAccount(eth.accounts[0])     <-- can also add time here
(type password)

Send transaction from account 0:
eth.sendTransaction({from: eth.accounts[0], to: "<your account here>", value: web3.toWei(<value>, "ether")})
EX:
eth.sendTransaction({from: eth.accounts[0], to: "0x997b5f2eab8dfaa9b3e1ba28f556d3eea2393986", value: web3.toWei(10000, "ether")})
(this will return transaction ID)

Check transaction:
eth.getTransaction("<transaction ID>")
EX:
eth.getTransaction("0x67511948c0561b99445d1ba67b2d2d600ec289c8baf85e01bbede01fbae91ee1")

Check ether balance of address:
web3.fromWei(eth.getBalance("<your account here>"), "ether")
EX:
web3.fromWei(eth.getBalance("0xfe91a6a5777698167f1dec05eee29a43c136760a"), "ether")








