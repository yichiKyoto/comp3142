# Functions

## havoc_mutation(conf, seed)
The main mutation function that initalises valid_sizes and use_stacking (represents the number of times a mutation is applied).
A for loop is iterated from 0 to use_stacking. Each iteration chooses a mutation, represented by the functions mutation1, mutation2,
mutation3, mutation4 and mutation5. After the for loop finishes, the mutation of the seed finishes, and will be written back into
the file conf['current_input']. 

## mutation1(data, data_len, valid_sizes)
Chooses a random value of 2, 4 or 8, and replaces a random segment of size value with random bytes.

## mutation2(data, data_len, valid_sizes)
Chooses a random value of 2, 4 or 8, and replaces a random segment of size value with a random interesting value, which
range from the minimum value for that byte size, maximum value for that byte size, 0, -1 and 1.

## mutation3(data, data_len, valid_sizes)
Chooses a random value of 2, 4 or 8. Chooses two random segments of size value and swaps them.

## mutation4(data, data_len)
Flips a random bit in the data segment.

## mutation5(data, data_len, valid_sizes)
Chooses a random value of 2, 4 or 8. Chooses a random segment of size value and deletes it.