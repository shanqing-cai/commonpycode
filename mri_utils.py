import os
import sys
from scai_utils import *

def get_n_frames(dfn):
    (tpath, se) = cmd_stdout("which mri_info")
    assert(len(se) == 0)
    if len(tpath) == 0:
        raise Exception, "Unable to find the required program: mri_info"

    (so, se) = cmd_stdout("mri_info %s" % dfn)
    assert(len(se) == 0)

    so = so.split("\n")
        
    nVols = -1
    for (i1, tline) in enumerate(so):
        if len(tline) == 0:
            continue

        tline = tline.strip()
        if tline.startswith("dimensions"):
            nVols = int(tline.split(" ")[-1])
            break
        
    return nVols
