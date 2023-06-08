import math


class DataSplitter:
    def __init__(self, block_size_bytes: int):
        self.data_string = None
        self.block_size_bytes = block_size_bytes

        # index for splitting the data_string into blocks
        self.data_index = 0

        # index of a single block in the array
        self.block_index = -1
        self.byte_array_array = []

        self.total_length = None
        self.total_blocks = None

    def set_new_data(self, data_string: str):
        self.data_string = data_string
        self.total_length = len(data_string)
        self.total_blocks = math.ceil(len(data_string) / self.block_size_bytes)

        self.data_index = 0
        self.block_index = -1
        self.byte_array_array = []

    def has_next_block(self) -> bool:
        if self.data_index <= self.total_length:
            return True

        return False

    def next_block(self):
        self.block_index += 1
        byte_array = []
        sub_string = self.data_string[self.data_index:self.data_index + self.block_size_bytes]

        for i in range(0, len(sub_string)):
            hex_char = sub_string[i].encode('ascii').hex()
            dec_char: int = int(hex_char, 16)
            byte_array.append(dec_char)

        self.data_index += self.block_size_bytes
        self.byte_array_array.append(byte_array)

        return self.total_blocks, self.block_index, byte_array

    def get_block(self, index: int):
        if self.data_string is None:
            raise Exception('No update available yet')

        if index > self.block_index or index < 0:
            raise Exception('Invalid index for update block')

        return self.byte_array_array[index]
