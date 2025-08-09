# Data Structures

## global_bitmap = bytearray(MAP_SIZE)
For feature1, I created a global_bitmap which is a bytearray of size 1 << 16. I modified the check_coverage function by iterating
over the raw_bitmap of a seed and comparing every position in the raw_bitmap with the global_bitmap. If an edge was visited in the raw_bitmap
but the same edge was not visited in the global_bitmap, I set new_edge_covered to True and I set the global_bitmap at that position to visited.

# Functions

## run_fuzzing
To save mutated seeds that cover new edges, in the fuzzing loop, if a new edge was covered by a mutated seed, I save the mutated seed into the path
that is created by full_path = os.path.join(conf['queue_folder'], f"seed{str(len(seed_queue))}"), where len(seed_queue) is the total number of mutated
seeds that I've saved. I use shutil.copyfile to copy the mutated seed into that path. 