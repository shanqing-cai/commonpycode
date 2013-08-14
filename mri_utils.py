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

def get_dcm_slice_timing(dicom_files):
# From Satrajit Ghosh's code at: https://github.com/satra/nipype/blob/enh/restingwf/examples/rsfmri_preprocessing.py#L47
    from dcmstack.extract import default_extractor
    from dicom import read_file
    from nipype.utils.filemanip import filename_to_list

    meta = default_extractor(read_file(filename_to_list(dicom_files)[0],
                                       stop_before_pixels=True,
                                       force=True))
    return (meta['RepetitionTime'] / 1000., meta['CsaImage.MosaicRefAcqTimes'],
            meta['SpacingBetweenSlices'])
