import os
import argparse
import signal
import shutil
from conf import *
from libc import *
from feedback import *
from execution import *
from seed import *
from schedule import *
from mutation import *


FORKSRV_FD = 198

# appended_seeds = set()

# listen for user's signal
def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Ending the fuzzing session...')
    sys.exit(0)


def run_forkserver(conf, ctl_read_fd, st_write_fd):
    os.dup2(ctl_read_fd, FORKSRV_FD)
    os.dup2(st_write_fd, FORKSRV_FD + 1)
    # prepare command
    cmd = [conf['target']] + conf['target_args']
    print(cmd)
    print(f'shmid is {os.environ[SHM_ENV_VAR]}')
    print(f'st_write_fd: {st_write_fd}')

    # eats stdout and stderr of the target
    dev_null_fd = os.open(os.devnull, os.O_RDWR)
    os.dup2(dev_null_fd, 1)
    os.dup2(dev_null_fd, 2)

    os.execv(conf['target'], cmd)


def run_fuzzing(conf, st_read_fd, ctl_write_fd, trace_bits):
    read_bytes = os.read(st_read_fd, 4)
    if len(read_bytes) == 4:
        print("forkserver is up! starting fuzzing... press Ctrl+C to stop")

    crash_queue = []
    seed_queue = []
    total_seeds_processed = 0
    avg_bitmap_size = 0
    avg_exec_time = 0

    # do the dry run, check if the target is working and initialize the seed queue
    shutil.copytree(conf['seeds_folder'], conf['queue_folder'])
    for i, seed_file in enumerate(os.listdir(conf['queue_folder'])):
        seed_path = os.path.join(conf['queue_folder'], seed_file)
        # copy the seed content to "current_input"
        shutil.copyfile(seed_path, conf['current_input'])
        # run the target with the seed
        status_code, exec_time = run_target(ctl_write_fd, st_read_fd, trace_bits)

        if status_code == 9:
            print(f"Seed {seed_file} caused a timeout during the dry run")
            sys.exit(0)

        if check_crash(status_code):
            print(f"Seed {seed_file} caused a crash during the dry run")
            sys.exit(0)


        new_edge_covered, coverage = check_coverage(trace_bits)
        avg_bitmap_size = calculate_new_avg(avg_bitmap_size, total_seeds_processed, coverage)
        avg_exec_time = calculate_new_avg(avg_exec_time, total_seeds_processed, exec_time)
        total_seeds_processed += 1

        new_seed = Seed(seed_path, i, coverage, exec_time)
        process_edges(trace_bits, new_seed)

        seed_queue.append(new_seed)



    print("Dry run finished. Now starting the fuzzing loop...")
    # start the fuzzing loop
    while True:
        selected_seed = select_next_seed(seed_queue)
        power_schedule = get_power_schedule(selected_seed, avg_exec_time, avg_bitmap_size)
        # generate new test inputs according to the power schedule for the selected seed
        for i in range(0, power_schedule):
            # TODO: implement the strategy for selecting a mutation operator
            havoc_mutation(conf, selected_seed)
            # run the target with the mutated seed
            status_code, exec_time = run_target(ctl_write_fd, st_read_fd, trace_bits)

            if status_code == 9:
                print("Timeout, skipping this input")
                continue

            if check_crash(status_code):
                print(f"Found a crash, status code is {status_code}")

                crash_index = len(crash_queue)
                new_crash_filename = f"crash_{crash_index}"

                new_crash_path = os.path.join(conf['crashes_folder'], new_crash_filename)
                shutil.copyfile(conf['current_input'], new_crash_path)
                crash_queue.append(new_crash_filename)

                continue

            new_edge_covered, coverage = check_coverage(trace_bits)
            avg_bitmap_size = calculate_new_avg(avg_bitmap_size, total_seeds_processed, coverage)
            avg_exec_time = calculate_new_avg(avg_exec_time, total_seeds_processed, exec_time)
            total_seeds_processed += 1

            if new_edge_covered:
                print("Found new coverage!")
                full_path = os.path.join(conf['queue_folder'], f"seed{str(len(seed_queue))}")
                # TODO: save the current test input as a new seed
                shutil.copyfile(conf['current_input'], full_path)
                new_seed = Seed(full_path, len(seed_queue), coverage, exec_time)
                process_edges(trace_bits, new_seed)
                seed_queue.append(new_seed)


def main():

    print("====== Welcome to use Mini-Lop ======")

    parser = argparse.ArgumentParser(description='Mini-Lop: A lightweight grey-box fuzzer')

    parser.add_argument('--config', '-c', required=True, help='Path to config file', type=str)

    args = parser.parse_args()

    config_path = os.path.abspath(args.config)

    config_valid, conf = parse_config(config_path)

    if not config_valid:
        print("Config file is not valid")
        return

    libc = get_libc()

    shmid, trace_bits = setup_shm(libc)
    # share the shmid with the target via an environment variable
    os.environ[SHM_ENV_VAR] = str(shmid)
    # clean the shared memory
    clear_shm(trace_bits)

    signal.signal(signal.SIGINT, signal_handler)

    # setup pipes for communication
    # st: status, ctl: control
    (st_read_fd, st_write_fd) = os.pipe()
    (ctl_read_fd, ctl_write_fd) = os.pipe()

    child_pid = os.fork()

    if child_pid == 0:
        run_forkserver(conf, ctl_read_fd, st_write_fd)
    else:
        run_fuzzing(conf, st_read_fd, ctl_write_fd, trace_bits)


if __name__ == '__main__':
    main()