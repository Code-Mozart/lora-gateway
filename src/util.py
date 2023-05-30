import math


class DataSplitter:
    def __init__(self, data_string: str, block_size_bytes: int):
        self.data_string = data_string
        self.block_size_bytes = block_size_bytes

        # index for splitting the data_string into blocks
        self.data_index = 0

        # index of a single block in the array
        self.block_index = -1
        self.byte_array_array = []

        self.total_length = len(data_string)
        self.total_blocks = math.ceil(len(data_string) / block_size_bytes)

    def has_next_block(self) -> bool:
        if self.data_index <= self.total_length:
            return True

        return False

    def next_block(self):
        self.block_index += 1
        byte_array = []
        sub_string = self.data_string[self.data_index:self.data_index + self.block_size_bytes]

        for i in range(0, len(sub_string)):
            hex_char = sub_string[i].encode('utf-8').hex()
            dec_char: int = int(hex_char, 16)
            byte_array.append(dec_char)

        self.data_index += self.block_size_bytes
        self.byte_array_array.append(byte_array)

        return self.total_blocks, self.block_index, byte_array

    def get_block(self, index: int):
        if index > self.block_index or index < 0:
            return []

        return self.byte_array_array[index]
