import ctypes, ctypes.util
import sys

def get_libc():
    libc_path = ctypes.util.find_library("c")
    if not libc_path:
        sys.exit("cannot find libc")

    # load libc
    libc = ctypes.CDLL(libc_path)
    if not libc:
        sys.exit("cannot load libc")

    return libc
