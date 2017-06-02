from .constants import *
from django.http import JsonResponse
from wifi import Cell, Scheme
from . import eth_api


# return the user's eth address and password, when username provided
def get_user_address_and_password(username, storage_manager):
    user_account = storage_manager.find(USERS_COLLECTION, {USERNAME: username})
    user_address = user_account[0][ETH_ACCOUNT_ADDR]
    password = user_account[0][PASSWORD]

    return user_address, password


# function is executed when user select login
def login(request, storage_manager):

    username = request.GET.get(USERNAME, None)
    password = request.GET.get(PASSWORD, None)

    # init return data
    data = {USERNAME: username}

    # query users to find username
    cursor = storage_manager.find(USERS_COLLECTION, data)

    # if there is an item in the cursor than name exits
    if cursor.count():

        # check to see if password is incorrect
        if password != cursor[0][PASSWORD]:
            data[RESPONSE] = 'Incorrect password'

        # else successful login! Configure session
        else:
            request.session[USER_ID] = username
            # set session to expire after 30, 1800s, minutes of inactivity
            request.session.set_expiry(SESSION_EXPIRY)

    # user name does not exist
    else:
        data[RESPONSE] = 'Username does not exist'

    return data


def detect_wifi_networks():
    print('Detect WIFI')
    # return the ssid and quality
    # sort by greatest quality
    return sorted([
        (net.quality, net.ssid)
        for net in list(Cell.all(IFACE))
    ], reverse=True)


# register nodes associated with user accounts
def register_node(request, storage_manager):
    # init return data dict
    data = {}

    # pull ssid of node from the request
    ssid = request.GET.get(SSID, None)

    # pull out username from session
    username = request.session[USER_ID]

    print('Registering:', ssid, 'to:', username)

    # check db to see if ssid already registered
    node_query = storage_manager.find(NODE_COLLECTION, {SSID: ssid})

    # if the node is already registered than return with error
    if node_query.count():
        print('Node Exists!!')
        data[RESPONSE] = 'Node Exists'
    else:
        print('New node! Registering...')
        # pull address of the user in order to "own" the node contract
        user_address, password = get_user_address_and_password(username, storage_manager)

        # create ethereum contract
        node_address = eth_api.create_node_contract(ssid, user_address, password)

        print('New Node Contract:', node_address)

        # insert to mongo within the nodes collection
        # storage_manager.insert(NODE_COLLECTION, {SSID: ssid, ETH_CONTRACT_ADDR: node_address})

        # update owner of the node with its ssid
        # storage_manager.update(collection_name=USERS_COLLECTION,
        #                        query={USERNAME: username},
        #                        update={'$push':
        #                                    {REGISTERED_NODES: ssid}
        #                                })

    return data
