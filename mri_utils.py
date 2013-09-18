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

def flirt_apply_xfm(inImg, refImg, xfmMat, outImg, interpMeth="", logFN=None):
    check_file(inImg, logFN=logFN)
    check_file(refImg, logFN=logFN)
    check_file(xfmMat, logFN=logFN)
    
    cmd = "flirt -in %s -ref %s -applyxfm -init %s -out %s " % \
          (inImg, refImg, xfmMat, outImg)

    if interpMeth != "":
        cmd += "-interp %s " % interpMeth

    saydo(cmd, logFN=logFN)
    
    check_file(outImg, logFN=logFN)

def invert_fsl_xfm_mat(inMatFN, outMatFN, logFN=None):
    check_bin_path("convert_xfm", logFN=logFN)

    check_file(inMatFN, logFN=logFN)
    
    cvtCmd = "convert_xfm -omat %s -inverse %s " % (outMatFN, inMatFN)
    saydo(cvtCmd, logFN=logFN)

    check_file(outMatFN, logFN=logFN)
    
    
def read_ctab(ctabfn):
    ctabf = open(ctabfn, 'r')
    ctxt = ctabf.read().split('\n')
    ctabf.close()
    
    roi_nums = []
    roi_names = []
    for clin in ctxt:
        clin = clin.replace("\t", " ")

        if len(clin) == 0:
            continue
        clin = clin.split(' ')
        while clin.count('') > 0:
            clin.remove('')

        #print(clin) # DEBUG
            
        if clin[1] == 'unknown' or clin[1] == 'bankssts' \
           or clin[1] == "corpuscallosum" or clin[1] == "Unknown" \
           or clin[1].startswith("None"):
            continue
        
        roi_nums.append(int(clin[0]))
        roi_names.append(clin[1])

    return (roi_nums, roi_names)

def nz_voxels(imgFN):
    check_file(imgFN)
    check_bin_path("fslstats")

    (so, se) = cmd_stdout("fslstats %s -V" % imgFN)
    assert(len(se) == 0)

    so = so.split(" ")
    assert(len(so) >= 2)

    nVoxels = int(so[0])
    mm3 = float(so[1])

    return (nVoxels, mm3)
