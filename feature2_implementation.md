# Data Structures

## edge_map = {}
The key represents the edge number, and the value represents an array of seeds that trigger that edge
favored_set.

## favored_set = {}
This contains all the Seed objects that are marked as favoured at a particular point of time.
The key represents the seed and the value represents how many times it was marked favoured.

## favored_visited = set()
This represents all the favoured seeds that were selected in the cycle at a particular point of time.

## unfavored_visited = set()
This represents all the non-favoured seeds that were selected in the cycle at a particular point of time.

## index
This represents the current position of the seed_queue array while it is being looped through.

## cycle_num
This represents how many cycles were travelled in the seed_queue array.

# Functions

## select_next_seed(seed_queue)
This function loops through the seed_queue array to select a seed. The first nested while loop checks whether there are still
favoured seeds in the cycle. It loops through all the unvisited seeds in the seed_queue until it finds an unvisited favored seed and returns that.
However, for every unvisited seed that it loops through, there is also 0.4 chance that it will return that unvisited seed even
through it might be unfavoured.

If all favoured seeds have been visited, the second nested while loop loops and wraps around the seed queue, returning the first instance
of an unvisited seed.

Otherwise, if all unfavoured and favoured seeds are visited, increase the cycle, reset the favored_visited and unfavored_visited arrays
and set index to 0. The process described above will begin again.

## add_to_edge_map(edge_num, seed)
This function takes two parameters, edge_num and seed. It will add the seed to the array at the specified edge_num key in the edge_map data structure.
First, it will get the seed array at edge_map[edge_num]. It will insert the seed at an appropriate position in that array based on the seed's
execution time * file size. As it inserts seeds, it will maintain the edge_map[edge_num] array by marking old first indices as unfavoured
and marking new first indices as favoured.

## add_to_favoured(seed)
Takes a parameter, seed, and marks it as favoured. It also adds it to the favoured_set dictionary and increases the number of times it was marked favoured.

## remove_from_favoured(seed)
Takes a parameter, seed, and subtracts its value by 1 (the number of times it was marked favoured) in the favoured_set dictionary. If this value
becomes 0, removes it from the favoured_set dicationary and mark it as unfavoured.

## process_edges(trace_bits, seed)
Takes two parameters, trace_bits and seed, where trace_bits represents the edges that the seed as covered.
It goes through the trace_bits bitmap and checks if the edge is not 0. If so, it means that the seed triggers the edge, and therefore,
it will add the seed to the respective array in the edge_map by calling add_to_edge_map(edge_num, seed). The process edges function
is called every time a mutated/unmutated seed is selected in the fuzzy loop or in the dry run.



