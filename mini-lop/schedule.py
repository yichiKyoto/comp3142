import ctypes
import random
from seed import *


# edge_map = {int : Seed[]} where int represents the edge number and str represents the file name of the seed
edge_map = {}
favored_set = {}
favored_visited = set()
unfavored_visited = set()

index = 0
cycle_num = 0
# TODO: implement the "favor" feature of AFL
def select_next_seed(seed_queue):

    # print(f"favored: {[seed.path for seed in favored_set]}")
    global index
    global cycle_num
    global favored_visited
    global unfavored_visited

    while True:
        while len(favored_visited) < len(favored_set):
            current_entry = seed_queue[index]
            if current_entry in favored_visited or current_entry in unfavored_visited:
                index = (index + 1) % len(seed_queue)
                continue

            if current_entry.favored:
                index = (index + 1) % len(seed_queue)
                return current_entry
            else:
                if random.random() < 0.4:
                    index = (index + 1) % len(seed_queue)
                    return current_entry
            index = (index + 1) % len(seed_queue)

        while (len(favored_visited) + len(favored_set)) < len(seed_queue):
            current_entry = seed_queue[index]
            if current_entry in favored_visited or current_entry in unfavored_visited:
                index = (index + 1) % len(seed_queue)
                continue
            index = (index + 1) % len(seed_queue)
            return current_entry

        cycle_num += 1
        favored_visited = set()
        unfavored_visited = set()
        index = 0


    # while True:
    #     current_entry = seed_queue[index]
    #     if current_entry.favored:
    #         index = (index + 1) % len(seed_queue)
    #         return current_entry
    #     else:
    #         if random.random() < 0.1:
    #             index = (index + 1) % len(seed_queue)
    #             return current_entry
    #     index = (index + 1) % len(seed_queue)
    # print(f"number of favored seeds visited: {len(favored_visited)}")
    # print(f"number of unfavored seeds visited: {len(unfavored_visited)}")
    # print(f"total number of favored seeds: {len(favored_set)}")
    # print(f"len(seed_queue) = {len(seed_queue)})")
    # while True:
    #
    #     if (len(favored_visited) + len(unfavored_visited)) >= len(seed_queue):
    #         index = 0
    #         cycle_num += 1
    #         favored_visited = set()
    #         unfavored_visited = set()
    #
    #     current_entry = seed_queue[index]
    #
    #     # if all favoured seeds are visited
    #     if len(favored_visited) == len(favored_set):
    #         while current_entry in favored_visited or current_entry in unfavored_visited:
    #
    #             index = (index + 1) % len(seed_queue)
    #         current_entry = seed_queue[index]
    #         unfavored_visited.add(current_entry)
    #         index = (index + 1) % len(seed_queue)
    #         return current_entry
    #
    #     # if not all favoured seeds are visited
    #     while current_entry in favored_visited or current_entry in unfavored_visited:
    #         print(f"index: {index}")
    #         index = (index + 1) % len(seed_queue)
    #
    #     current_entry = seed_queue[index]
    #
    #     if current_entry.favored:
    #         favored_visited.add(current_entry)
    #         index = (index + 1) % len(seed_queue)
    #         return current_entry
    #     else:
    #         if random.random() < 0.5:
    #             unfavored_visited.add(current_entry)
    #             index = (index + 1) % len(seed_queue)
    #             return current_entry






# get the power schedule (# of new test inputs to generate for a seed)
def get_power_schedule(seed, avg_exec_us, avg_bitmap_size):
    # this is a dummy implementation, it just returns a random number
    # TODO: implement the power schedule similar to AFL (should consider the coverage, and execution time)
    perf_score = 0
    if seed.exec_time * 0.1 > avg_exec_us:
        perf_score = 10
    elif seed.exec_time * 0.25 > avg_exec_us:
        perf_score = 25
    elif seed.exec_time * 0.5 > avg_exec_us:
        perf_score = 50
    elif seed.exec_time * 0.75 > avg_exec_us:
        perf_score = 75
    elif seed.exec_time * 4 < avg_exec_us:
        perf_score = 300
    elif seed.exec_time * 3 < avg_exec_us:
        perf_score = 200
    elif seed.exec_time * 2 < avg_exec_us:
        perf_score = 150
    else:
        perf_score = 100

    if seed.coverage * 0.3 > avg_bitmap_size:
        perf_score *= 3
    elif seed.coverage * 0.5 > avg_bitmap_size:
        perf_score *= 2
    elif seed.coverage * 0.75 > avg_bitmap_size:
        perf_score *= 1.5
    elif seed.coverage * 3 < avg_bitmap_size:
        perf_score *= 0.25
    elif seed.coverage * 2 < avg_bitmap_size:
        perf_score *= 0.5
    elif seed.coverage * 1.5 < avg_bitmap_size:
        perf_score *= 0.75

    return int(perf_score/100)


def add_to_edge_map(edge_num, seed):
    if not edge_num in edge_map:
        edge_map[edge_num] = [seed]
        add_to_favored(seed)
        return

    seeds_at_edge = edge_map[edge_num]
    # print(favored_set)
    # print(seeds_at_edge)

    this_efficiency = seed.exec_time * seed.file_size

    count = 0
    while count < len(seeds_at_edge):
        other_seed = seeds_at_edge[count]
        if other_seed == seed:
            return
        other_efficiency = other_seed.exec_time * other_seed.file_size
        if this_efficiency < other_efficiency:
            if count == 0:
                add_to_favored(seed)
                remove_from_favored(seeds_at_edge[0])
            seeds_at_edge.insert(count, seed)
            # print(f"seed was marked favored {seeds_at_edge[0]}")
            return
        count += 1
    seeds_at_edge.append(seed)

    # print(f"seed was marked favored {seeds_at_edge[0]}")



def add_to_favored(seed):
    seed.mark_favored()
    if not seed in favored_set:
        favored_set[seed] = 1
    else:
        favored_set[seed] += 1

def remove_from_favored(seed):
    favored_set[seed] -= 1
    if favored_set[seed] == 0:
        del favored_set[seed]
        seed.unmark_favored()

def process_edges(trace_bits, seed):
    raw_bitmap = ctypes.string_at(trace_bits, 1 << 16)
    for edge_num, value in enumerate(raw_bitmap):
        if value != 0:
            add_to_edge_map(edge_num, seed)