import ipfsapi
import numpy as np
import io


class IPFS:

    def __init__(self, url, port):
        # aggregate above to final url for usage
        self.api = ipfsapi.connect(url, port)
        print('Connected to IPFS at:', url, port)

    def add_file(self, file_path):
        print('add file:', file_path)

        # requires file path to read data from
        response = self.api.add(file_path)

        return response

    def put_block(self, block_data, **kwargs):
        # <class 'bytes'> required as input
        print('Put Block')
        # convert to bytes so accepted as block by ipfs
        byte_data = io.BytesIO(block_data)
        response = self.api.block_put(byte_data)

        return response

    def get_camera_frame_block(self, block_hash, shape):
        print('get frame block:', block_hash)

        block_data = self.api.block_get(block_hash)

        # reshape so the image can be viewed, require the reshape params!
        # for example shape=[480, 640, 3]
        block_array = np.fromstring(block_data, np.uint8).reshape(shape[0], shape[1], shape[2])

        return block_array

    def get_data(self, data_hash):
        # downloads data into active directory where file name is the hash
        response = self.api.get(data_hash)
        return response
