from seed import *
MAP_SIZE = (1 << 16)
global_bitmap = [0] * MAP_SIZE
# favoured_seeds = {int : Seed[]}
favoured_seeds = {}

def add_to_favoured_seeds(edge_num, seed):
    if not edge_num in favoured_seeds:
        favoured_seeds[edge_num] = []
    seed_list = favoured_seeds[edge_num]
    if not seed in seed_list:
        seed_list[0].unmark_favored()
        seed_list.append(seed)
        seed_list.sort(key=lambda s: s.exec_time * s.file_size)
        seed_list[0].mark_favored()
