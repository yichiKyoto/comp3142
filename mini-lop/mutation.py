import random


def havoc_mutation(conf, seed):
    # this is a dummy implementation, it just randomly flips some bytes
    # TODO: implement the havoc mutation similar to AFL
    with open(seed.path, 'rb') as f:
        data = bytearray(f.read())

        data_len = len(data)
        valid_sizes = []
        if data_len >= 2:
            valid_sizes.append(2)
        if data_len >= 4:
            valid_sizes.append(4)

        if data_len >= 8:
            valid_sizes.append(8)

        if not valid_sizes:
            return

        mutation1(data, data_len, valid_sizes)
        mutation2(data, data_len, valid_sizes)
        mutation3(data, data_len, valid_sizes)

        # write the mutated data back to the current input file
        with open(conf['current_input'], 'wb') as f_out:
            f_out.write(data)

# randomly select 2/4/8 bytes from the seed file and add/sub a random value
def mutation1(data, data_len, valid_sizes):

    for _ in range(random.randint(1, int(data_len / 5))):
        size = random.choice(valid_sizes)

        # Randomly select a byte index to flip
        byte_index = random.randint(0, data_len - size)

        byte_chunk = data[byte_index:byte_index + size]
        current_val = int.from_bytes(byte_chunk, byteorder='little', signed=True)

        max_val = 1 << (size * 8)

        random_int = random.randrange(0, max_val)
        new_val = (current_val + random_int) % max_val
        new_val_bytes = new_val.to_bytes(size, 'little')

        for i in range(0, size):
            data[i + byte_index] = new_val_bytes[i]

# randomly replace a short int/int/long int (2/4/8 bytes) with an interesting value (min/max/0/-1/1)
def mutation2(data, data_len, valid_sizes):
    for _ in range(random.randint(1, int(data_len / 5))):
        size = random.choice(valid_sizes)
        size_min = -(1 << (size * 8 - 1))
        size_max = (1 << (size * 8 - 1)) - 1
        interesting_values = [size_min, size_max, 0, -1, 1]
        random_value = random.choice(interesting_values)
        random_value = random_value.to_bytes(size, byteorder='little', signed=True)
        # Randomly select a byte index to flip
        byte_index = random.randint(0, data_len - size)

        for i in range(0, size):
            data[i + byte_index] = random_value[i]

# randomly replace a random length chunk of bytes in the seed input with another chunk in the same file.
def mutation3(data, data_len, valid_sizes):
    for _ in range(random.randint(1, int(data_len / 5))):
        size = random.choice(valid_sizes)

        # Randomly select the two byte indexes to flip
        byte_index = random.randint(0, data_len - size)
        other_byte_index = random.randint(0, data_len - size)

        byte_chunk = data[byte_index:byte_index + size]
        other_byte_chunk = data[other_byte_index:other_byte_index + size]


        for i in range(0, size):
            data[i + byte_index] = other_byte_chunk[i]

        for j in range(0, size):
            data[j + other_byte_index] = byte_chunk[j]