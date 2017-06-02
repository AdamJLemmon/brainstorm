import zerorpc
from .constants import *


# methods require an instance to point at rpc
def init_web3():
    # # # init client to connect to web3 server
    web3 = zerorpc.Client()
    #
    # # connection with web3 api being served over rpc
    web3.connect(ZPC_IP + ':' + ZPC_PORT)

    return web3


# method called from front end when user selects they would like to create a new account
def create_account(request, storage_manager):

    username = request.GET.get(USERNAME, None)
    password = request.GET.get(PASSWORD, None)
    email = request.GET.get(EMAIL, None)

    # init return data
    data = {USERNAME: username}

    # query users to see if username already exists
    cursor = storage_manager.find(USERS_COLLECTION, data)

    # if there is an item in the cursor than name exits
    if cursor.count():
        data[RESPONSE] = 'Username already exists'

    # new user, create
    else:
        print('New user! Creating your blockchain account :)')
        # init connection to rpc
        web3 = init_web3()

        # first create a new ethereum account!
        # insert this address with user account
        eth_account_address = web3.executeMethod('create_account', password)
        print('New eth address:', eth_account_address)

        # web3 has done its job, close the client connection
        web3.close()

        # update session
        request.session[USER_ID] = username
        # set session to expire after 30, 1800s, minutes of inactivity
        request.session.set_expiry(SESSION_EXPIRY)

        # insert new user account into database
        storage_manager.insert(USERS_COLLECTION,
                               {
                                   USERNAME: username,
                                   PASSWORD: password,
                                   EMAIL: email,
                                   ETH_ACCOUNT_ADDR: eth_account_address
                               })

    return data


# when a new node is being registered, create new contract
def create_node_contract(ssid, user_address, password):
    print('New Contract:', ssid, user_address, password)

    web3 = init_web3()

    contract_addr = web3.executeMethod('deploy_node_contract',
                                        {SSID: ssid,
                                         ETH_ACCOUNT_ADDR: user_address,
                                         PASSWORD: password})

    # web3 has done its job, close the client connection
    web3.close()

    return contract_addr
