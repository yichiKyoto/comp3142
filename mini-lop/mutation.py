import random


def havoc_mutation(conf, seed):
    use_stacking = 2 ** random.randint(0, 6)

    with open(seed.path, 'rb') as f:
        data = bytearray(f.read())
        data_len = len(data)

        # Initialize valid_sizes based on current data_len
        valid_sizes = []
        if data_len >= 2:
            valid_sizes.append(2)
        if data_len >= 4:
            valid_sizes.append(4)
        if data_len >= 8:
            valid_sizes.append(8)

        for _ in range(use_stacking):
            if data_len == 0:  # Stop if data becomes empty
                break

            choice = random.randint(1, 5)

            if choice == 1:
                new_len = mutation1(data, data_len, valid_sizes)
            elif choice == 2:
                new_len = mutation2(data, data_len, valid_sizes)
            elif choice == 3:
                new_len = mutation3(data, data_len, valid_sizes)
            elif choice == 4:
                new_len = mutation4(data, data_len)
            else:
                new_len = mutation5(data, data_len, valid_sizes)

            # Update data_len if mutation changed it
            if new_len != data_len:
                data_len = new_len
                # Recompute valid_sizes based on new length
                valid_sizes = []
                if data_len >= 2:
                    valid_sizes.append(2)
                if data_len >= 4:
                    valid_sizes.append(4)
                if data_len >= 8:
                    valid_sizes.append(8)

        # Write mutated data
        with open(conf['current_input'], 'wb') as f_out:
            f_out.write(data)


# Each mutation does one operation and returns new length
def mutation1(data, data_len, valid_sizes):
    if not valid_sizes:
        return data_len

    size = random.choice(valid_sizes)
    byte_index = random.randint(0, data_len - size)

    # Get current value and modify
    current_val = int.from_bytes(
        data[byte_index:byte_index + size],
        'little',
        signed=True
    )
    max_val = 1 << (size * 8)
    random_int = random.randrange(0, max_val)
    new_val = (current_val + random_int) % max_val
    new_val_bytes = new_val.to_bytes(size, 'little')

    # Write back
    data[byte_index:byte_index + size] = new_val_bytes
    return data_len  # Length unchanged


def mutation2(data, data_len, valid_sizes):
    if not valid_sizes:
        return data_len

    size = random.choice(valid_sizes)
    byte_index = random.randint(0, data_len - size)

    # Get interesting value
    size_min = -(1 << (size * 8 - 1))
    size_max = (1 << (size * 8 - 1)) - 1
    interesting_values = [size_min, size_max, 0, -1, 1]
    random_value = random.choice(interesting_values)
    random_value_bytes = random_value.to_bytes(size, 'little', signed=True)

    # Write to position
    data[byte_index:byte_index + size] = random_value_bytes
    return data_len  # Length unchanged


def mutation3(data, data_len, valid_sizes):
    if not valid_sizes:
        return data_len

    size = random.choice(valid_sizes)
    byte_index = random.randint(0, data_len - size)
    other_byte_index = random.randint(0, data_len - size)

    chunk1 = bytearray(data[byte_index:byte_index + size])
    chunk2 = bytearray(data[other_byte_index:other_byte_index + size])

    # Swap chunks
    data[byte_index:byte_index + size] = chunk2
    data[other_byte_index:other_byte_index + size] = chunk1
    return data_len  # Length unchanged


def mutation4(data, data_len):
    if data_len == 0:
        return data_len

    byte_index = random.randint(0, data_len - 1)
    bit_position = random.randint(0, 7)
    data[byte_index] ^= (1 << bit_position)  # Flip single bit
    return data_len  # Length unchanged


def mutation5(data, data_len, valid_sizes):
    if not valid_sizes:
        return data_len

    size = random.choice(valid_sizes)
    if data_len < size:
        return data_len

    byte_index = random.randint(0, data_len - size)

    del data[byte_index:byte_index + size]
    return data_len - size  # Return new length
