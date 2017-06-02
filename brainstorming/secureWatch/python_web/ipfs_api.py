# import requests
import cv2
import ipfsapi
import numpy as np
import io


class IPFS:

    def __init__(self):
        self.api_server_url = "127.0.0.1"
        self.api_server_port = 5001

        # aggregate above to final url for usage
        self.api = ipfsapi.connect(self.api_server_url, self.api_server_port)

    def add_file(self, file_path):
        print('add file:', file_path)

        # requires file path to read data from
        response = self.api.add(file_path)

        return response

    def put_block(self, block_data, **kwargs):
        # <class 'bytes'> required as input
        print('put block')
        print(kwargs)
        # convert to bytes so accepted as block by ipfs
        byte_data = io.BytesIO(block_data)
        response = self.api.block_put(byte_data)

        return response

    def get_camera_frame_block(self, block_hash):
        print('get frame block:', block_hash)

        block_data = self.api.block_get(block_hash)

        # reshape so the image can be viewed, require the reshape params!
        block_array = np.fromstring(block_data, np.uint8).reshape(480, 640)

        return block_array

    def get_data(self, data_hash):
        # downloads data into active directory where file name is the hash
        response = self.api.get(data_hash)
        return response
