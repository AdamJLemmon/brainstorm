import numpy as np
import cv2
from django.http import JsonResponse
from .mongo_storage_api import StorageManager
import zerorpc
from .constants import *
from .ipfs_api import IPFS

# mongo storage connection
storage_manager = StorageManager('localhost', 27017, 'secureWatch')

# distributed object storage
# ipfs = IPFS()


# init client connection to web3 server
def init_web3():
    web3 = zerorpc.Client()
    web3.connect("tcp://0.0.0.0:4242")

    return web3


def open_and_view_cam():
    print('Opening cam')

    cap = cv2.VideoCapture(0)

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def grab_frame():
    cap = cv2.VideoCapture(1)

    # Capture frame-by-frame
    ret, frame = cap.read()
    cap.release()

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # convert to list in order to JSON-ify to reture to javascript
    # image = gray.tolist()  # nested lists with same data, indices
    # return JsonResponse(image, safe=False)
    return frame


def push_data_packet(request):
    # pull frames from cam and push to contract / ipfs
    web3 = init_web3()

    # grab frame and push to contract
    # frame = grab_frame()
    #
    # # require shape to decode data upon getting
    # shape = frame.shape
    #
    # # convert to raw bytes for storage in ipfs
    # frame_bytes = frame.tobytes()
    #
    # # put the data into ipfs and retrieve the data hash
    # put_res = ipfs.put_block(frame_bytes, shape=shape)
    # print(put_res)
    #
    # # pull out hash key to access at a later date
    # data_key = put_res[KEY]

    # update contract with newest data hash
    # retrieve devide address
    device_address = '0x3de30c5ef7318ade67e166eb0767ff7a6792831a'
    contract_source = get_contract_source('contracts/Device.sol')
    contract_address = '0x3a8d4ceec6a1a41657b12ac9fa520d22fe06bdf6'
    data = 15

    print('push data')

    contract = web3.pushDatatoContract(device_address, contract_source, contract_address, data)
    print('received contract')
    print(contract)

    return JsonResponse({'data': contract})


def discover_usb_devices(request):
    import re
    import subprocess

    # device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []

    for i in df.split(b'\n'):
        devices.append(str(i))

    print(type(devices))
    return JsonResponse(devices, safe=False)


def create_new_eth_account(web3, password):
    # create new eth account and return the address
    address = web3.createNewAccount(password)
    print("NEW ACCOUNT: " + address)

    return address


def get_contract_source(contract_path):
    print("Reading contract")
    f = open(contract_path, "r")
    contract_source = f.read()
    f.close()

    return contract_source


def register_new_device(request):
    # create local connection to rpc
    web3 = zerorpc.Client()
    web3.connect("tcp://0.0.0.0:4242")

    print("NEW Device")
    device_id = request.GET.get(DEVICE_ID, None)

    # create or gen this? todo
    password = "geth"

    device_address = create_new_eth_account(web3, password)

    # deploy smart contract for device! require user address(owner) and device addr
    # read device contract file
    contract_source = get_contract_source("contracts/Device.sol")

    print('Deploying contract')
    # deploy device contract, require account credentials of the user deploying
    contract_address = web3.deployDeviceContract(device_address, contract_source, "0x28a48f121ca4b2b335554b20b972d3542f496149", "geth")

    print('Contract deployed:', contract_address)
    # create mongo entry to hold data for this device
    storage_manager.insert(DEVICES, {DEVICE_ID: device_id, PASSWORD: password,
                                     ACCOUNT_ADDRESS: device_address,
                                     CONTRACT_ADDRESS: contract_address})

    return JsonResponse({'data': 'success'})


def show_image(image_array):
    cv2.imshow('Image', image_array)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#     TEST
def deploy_contract(web3, source, contract_name, constructor_params):
    user_account = '0x28a48f121ca4b2b335554b20b972d3542f496149'
    password = 'geth'
    return web3.deployContract(source, contract_name, user_account, password, constructor_params)


def call_contract_method(web3, source, contract_name, contract_address, method, params=None):
    print(web3.hello())
    print('Response:', web3.callContractMethod(source, contract_name, contract_address, method, params))


# PARAMS
web3 = init_web3()
source = get_contract_source('contracts/greeter.sol')
contract_name = 'device'
constructor_params = "0x28a48f121ca4b2b335554b20b972d3542f496149"

print(deploy_contract(web3, source, contract_name, constructor_params))

contract_address = '0xa04b109510d5265d06902b313222a94026bf674d'
# method = 'set_device_permission'
method = 'add_transaction'
# call_contract_method(web3, source, contract_name, contract_address, method, '0x6093bb26193dc29b2cd2596362b823e8ec7d39a6')
# call_contract_method(web3, source, contract_name, contract_address, method, 'QmaG4FuMqEBnQNn3C8XJ5bpW8kLs7zq2ZXgHptJHbKDDVx')

if __name__ == "__main__":
    pass