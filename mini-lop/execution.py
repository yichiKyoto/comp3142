import os
import signal
import threading
import time
from feedback import clear_shm

# this is the timeout per execution in milliseconds
# in practice, this is better to be implemented as a configurable option in the config file
# but for now, we hardcode it here (to have fewer changes in the code)
TIMEOUT = 100
TIMEOUT_SEC = float(TIMEOUT/10000)


def monitor_timeout(grandchild_pid):
    """Thread function to monitor if the status byte is read within the timeout period."""
    time.sleep(TIMEOUT_SEC)
    try:
        # Kill the grandchild process if the main thread hasn't read the status byte
        os.kill(grandchild_pid, signal.SIGKILL)
        print(f"Timeout of {TIMEOUT} ms reached. Killed grandchild process {grandchild_pid}.")
    except OSError:
        # Process may already be terminated or doesn't exist
        # print(f"Grandchild process {grandchild_pid} already terminated.")
        pass


def run_target(ctl_write_fd, st_read_fd, trace_bits):
    # need to clear the shared memory before running the target
    clear_shm(trace_bits)

    # lscpu | grep "Byte Order"
    os.write(ctl_write_fd, (0).to_bytes(4, byteorder='little'))
    start_time = time.time()

    # print only for debugging purpose
    grandchild_pid_bytes = os.read(st_read_fd, 4)
    grandchild_pid = int.from_bytes(grandchild_pid_bytes, byteorder='little', signed=False)
    # print("grandchild pid is {}".format(int.from_bytes(grandchild_pid_bytes, byteorder='little', signed=False)))
    status_bytes = None

    timeout_thread = threading.Thread(target=monitor_timeout, args=(grandchild_pid,))
    timeout_thread.start()

    if timeout_thread.is_alive():
        # don't poll too frequently, sleep for 1ms
        timeout_thread.join(0.0001)

    status_bytes = os.read(st_read_fd, 4)
    status_code = int.from_bytes(status_bytes, byteorder='little', signed=False)
    end_time = time.time()
    exec_time = end_time - start_time
    # print(f"status is {status_code}")
    # You can uncomment the following lines to better observe the execution logs when debugging
    # print(f"Execution time: {float(exec_time*1000)} ms")
    # time.sleep(1)

    return status_code, exec_time
