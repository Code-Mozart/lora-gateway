class DataSplitter:
    def __init__(self, data_string: str, chunk_size_bytes: int):
        self.data_string = data_string
        self.chunk_size_bytes = chunk_size_bytes
        self.index = 0
        self.total_length = len(data_string)

    def has_next_chunk(self) -> bool:
        if self.index <= self.total_length:
            return True

        return False

    def next_chunk(self) -> list:
        byte_array = []
        sub_string = self.data_string[self.index:self.index + self.chunk_size_bytes]

        for i in range(0, len(sub_string)):
            hex_char = sub_string[i].encode('utf-8').hex()
            dec_char: int = int(hex_char, 16)
            byte_array.append(dec_char)

        self.index += self.chunk_size_bytes

        return byte_array
