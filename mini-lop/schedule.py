import random
from seed import *

index = 0

num_visited = 0
# TODO: implement the "favor" feature of AFL
def select_next_seed(seed_queue : list[Seed], visited: dict[Seed, bool]):
    global index
    global num_visited

    if num_visited >= len(seed_queue):
        # reset the visited array to all false
        for s in visited.keys():
            visited[s] = False

    has_favored_in_cycle = False
    for seed in visited.keys():
        if seed.favored and not visited[seed]:
            has_favored_in_cycle = True
            break

    if not has_favored_in_cycle:
        while visited[seed_queue[index]]:
            index = (index + 1) % len(seed_queue)
        current_index = index
        index = (index + 1) % len(seed_queue)
        visited[seed_queue[current_index]] = True
        num_visited += 1
        return seed_queue[current_index]

    while not seed_queue[index].favored:
        if visited[seed_queue[index]]:
            index = (index + 1) % len(seed_queue)
            continue

        visited[seed_queue[index]] = True
        num_visited += 1
        if random.random() < 0.1:
            break
        index = (index + 1) % len(seed_queue)

    current_index = index
    index = (index + 1) % len(seed_queue)
    return seed_queue[current_index]




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

    return perf_score
