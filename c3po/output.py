from __future__ import print_function

verbose = True

#so you can globally disable all prints
def vprint(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)
