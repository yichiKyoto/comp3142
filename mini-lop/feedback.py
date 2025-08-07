import ctypes
import sys
import sysv_ipc

SHM_ENV_VAR   = "__AFL_SHM_ID"
MAP_SIZE_POW2 = 16
MAP_SIZE = (1 << MAP_SIZE_POW2)
global_bitmap = bytearray(MAP_SIZE)


def setup_shm(libc):
    # map functions
    shmget = libc.shmget
    shmat = libc.shmat

    shmat.restype = ctypes.c_void_p
    shmat.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.c_int)

    # get the shared memory segment

    shmid = shmget(sysv_ipc.IPC_PRIVATE, MAP_SIZE, sysv_ipc.IPC_CREAT | sysv_ipc.IPC_EXCL | 0o600)

    if shmid < 0:
        sys.exit("cannot get shared memory segment with key %d" % (sysv_ipc.IPC_PRIVATE))

    # map the shared segment into the current process' memory
    # the location (size + 4096) is just a hint
    shmptr = shmat(shmid, None, 0)
    if shmptr == 0 or shmptr== -1:
        sys.exit("cannot attach shared memory segment with id %d" % (shmid))

    print(f'created shared memory, shmid: {shmid}')

    return shmid, shmptr


def clear_shm(trace_bits):
    ctypes.memset(trace_bits, 0, MAP_SIZE)


def check_crash(status_code):
    crashed = False
    if status_code == 6:
        crashed = True
        print("Found an abort!")
    elif status_code == 134:
        crashed = True
        print("Found an abort!")
    elif status_code == 8:
        crashed = True
        print("Found a float-point error!")
    elif status_code == 11:
        crashed = True
        print("Found a segfault!")
    elif status_code == 139:
        crashed = True
        print("Found a segfault!")
    return crashed


# def check_coverage(trace_bits):
#     raw_bitmap = ctypes.string_at(trace_bits, MAP_SIZE)
#     total_hits = 0
#     new_edge_covered = False
#
#     for edge_num, value in enumerate(raw_bitmap):
#
#         if value != 0:
#             total_hits += 1
#             if not global_bitmap[edge_num]:
#                 new_edge_covered = True
#             global_bitmap[edge_num] = 1
#
#     return new_edge_covered, total_hits


def check_coverage(trace_bits):
    raw_bitmap = ctypes.string_at(trace_bits, MAP_SIZE)
    num_edges_covered = 0
    new_edges_found = 0

    for edge_num in range(MAP_SIZE):
        # TODO: maintain a global coverage of all seeds, check if this seed covers a new edge
        value = raw_bitmap[edge_num]

        if value:  # Edge was hit in this run
            num_edges_covered += 1

            # Track if this edge is newly discovered
            if not global_bitmap[edge_num]:
                new_edges_found += 1

            # Update global hit count
            new_count = global_bitmap[edge_num] + value
            global_bitmap[edge_num] = min(new_count, 255)

    return (new_edges_found > 0), num_edges_covered



