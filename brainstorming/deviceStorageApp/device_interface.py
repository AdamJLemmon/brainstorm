import cv2
from ipfs_server import IPFS
from datetime import datetime
import time
import zerorpc


class Device:

    def __init__(self, _id):
        print('New Device, ID:', _id)
        self.storage = IPFS(url="127.0.0.1", port=5001)

    def grab_frame(self):

        cap = cv2.VideoCapture(1)

        # def retrieve_frame():
        retrieved, frame = cap.read()

        if retrieved:
            return frame
        else:
            self.grab_frame()

    def show_frame(self, _frame):
        cv2.imshow('frame', _frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# TEST METHODS

# *************************
# ****** PUT Frame ********
# *************************
# pulls frames from static camera, stores bytes in ipfs and hash in contract
def put_frame(quantity, delay):

    # pull the define quantity of frames at the desired interval
    for i in range(quantity):
        print('Pulling frame:', i)

        # grab raw numpy frame and shape is required when pulling the bytes back
        frame = device.grab_frame()
        shape = frame.shape
        # timestamp down to micro seconds? int to drop the decimals
        timestamp = int(datetime.now().timestamp()*1000000)
        # device.show_frame(frame)

        # convert numpy array to bytes and store as block
        put_response = device.storage.put_block(frame.tobytes())
        print("PUT:", put_response)

        # pull out hash, will need to store in data contract
        data_hash = put_response['Key']
        print('Data hash:', data_hash)

        # ***************************
        # ****** Web3 New Upload ****
        # ***************************
        # update the data contract with hash on new data
        print(web3.executeMethod("new_data_upload",
                                 {'data_hash': data_hash,
                                  'shape': shape,
                                  'timestamp': timestamp}))

        time.sleep(delay)


# ***************************
# ******** Get Data *********
# ***************************
# finds all hashes within time frame from contract and then gets the block data from ipfs
# shape back to original format and show with cv2
def get_frames(start, end):

    # get a list of hashes from contract within time interval
    returned_hash_list = web3.executeMethod("get_uploaded_device_data",
                                            {'start_time': start,
                                             'end_time': end})

    # list returned as string with commas separating hashes, split string into list
    hash_list = returned_hash_list.split(',')

    # pop the leading ,
    hash_list.pop(0)
    print(len(hash_list))

    # grab each data hash from storage and show
    for _hash in hash_list:
        frame = device.storage.get_camera_frame_block(_hash, shape=[480, 640, 3])
        device.show_frame(frame)


if __name__ == '__main__':
    web3 = zerorpc.Client()
    web3.connect("tcp://127.0.0.1:4242")

    # init device that will be monitored
    device = Device('test')

    # put_frame(5, 5)

    # get_frames(start=int(datetime(2016, 12, 12).timestamp()*1000000),
    #            end=int(datetime.now().timestamp()*1000000))

    # web3.executeMethod("set_user_permissions",
    #                    {'user_addr': "0x3ba900ba8797378c9eb3743ac220fc7f583c64ff",
    #                     'permission': True})
