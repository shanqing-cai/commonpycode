import os
import sys

def saydo(cmd, echo=True):
    if echo:
        print(cmd + '\n')

    os.system(cmd)

def qsubmit(cmd, queue, jobname):
    os.system('ezsub -c "%s" -q %s -n %s'%(cmd, queue, jobname))

def remove_empty_strings(lst):
    while lst.count('') > 0:
        lst.remove('')
    return lst

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

def check_file(fn):
    if not os.path.isfile(fn):
        raise Exception, "Missing file: %s"%fn

def check_dir(dn, bCreate=False):
    if not os.path.isdir(dn):
        if not bCreate:
            raise Exception, "Missing directory: %s"%dn
        else:
            os.system("mkdir -p %s"%dn)
            if not os.path.isdir(dn):
                raise Exception, "Failed to create directory: %s"%dn
            else:
                print("INFO: Created directory: %s"%dn)

def delete_file_if_exists(fn):
    if os.path.isfile(fn):
        os.system("rm -f %s" % fn)
        if os.path.isfile(fn):
            raise Exception, "Failed to remove file: %s" % fn

def read_text_file(txtfn):
    txtf = open(txtfn, "rt")
    t = txtf.read().split("\n")
    txtf.close()

    return t


def write_list_to_text_file(tlist, txtfn):
    txtf = open(txtfn, "wt")
    for (i0, tline) in enumerate(tlist):
        txtf.write("%s\n" % tline)
    txtf.close()


def cmd_stdout(cmd):
    from subprocess import Popen, PIPE
    
    (sout, serr) = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)\
                   .communicate()
    return (sout, serr)
