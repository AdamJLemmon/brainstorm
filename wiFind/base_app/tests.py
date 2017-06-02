from django.test import TestCase
from . import eth_api

# Create your tests here.


def create_node_contract():
    user_address = '0x16b89424220b8f0962434bb1d609dd2cf47c5807'
    password = 'geth'
    ssid = 'test_network'

    # contract_response = eth_api.create_node_contract(ssid, user_address, password)

    # some assertions?
    # print(contract_response)


if __name__ == '__main__':

    create_node_contract()