import os
import sys

def saydo(cmd, echo=True, logFN=None, bLogDate=True):
    if bLogDate:
        import datetime
        dtStr = datetime.datetime.isoformat(datetime.datetime.now())

    if echo:
        if bLogDate:
            print("Running command @ %s:" % dtStr)
            print(cmd + '\n')
        
    if logFN == None or logFN == "":
        
        os.system(cmd)
    else:
        

        logF = open(logFN, "at")

        if bLogDate:
            logF.write("\nCOMMAND @ %s: %s\n\n" % (dtStr, cmd))
        else:
            logF.write("\nCOMMAND: %s\n\n" % cmd)
            
        logF.close()

        os.system("%s 2>&1 | tee -a %s" % (cmd, logFN))

def info_log(info, logFN=None, bWarn=False):
    import datetime

    if not bWarn:
        str = "INFO @ %s: %s" \
              % (datetime.datetime.isoformat(datetime.datetime.now()), info)
    else:
        str = "WARNING @ %s: %s" \
              % (datetime.datetime.isoformat(datetime.datetime.now()), info)

    if logFN != None and logFN != "":
        logF = open(logFN, "at")
        logF.write("%s\n" % str)
        logF.close()

    if not bWarn:
        print(str)
    else:
        print("\033[93m" + str + "\033[0m")
    

def error_log(errInfo, logFN=None):
    import datetime

    errDTStr = "ERROR @ %s: %s" \
               % (datetime.datetime.isoformat(datetime.datetime.now()), 
                  errInfo)

    if logFN != None and logFN != "":
        logF = open(logFN, "at")
        logF.write("\n%s\n" % errDTStr)
        logF.write("%s\n\n" % errInfo)
        logF.close()

    print("\033[91m" + errDTStr + "\033[0m")
    raise Exception, errInfo

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

def check_file(fn, logFN=None):
    if not os.path.isfile(fn):
        error_log("Missing file: %s" % fn, logFN=logFN)

def check_dir(dn, bCreate=False, logFN=None):
    if not os.path.isdir(dn):
        if not bCreate:
            error_log("Missing directory: %s" % dn, logFN=logFN)
        else:
            saydo("mkdir -p %s" % dn, logFN=logFN)
            if not os.path.isdir(dn):
                error_log("Failed to create directory: %s" % dn, logFN=logFN)
            else:
                info_log("Created directory: %s"%dn, logFN=logFN)



def delete_file_if_exists(fn, recursive=False):
    if os.path.isfile(fn):
        if not recursive:
            os.system("rm -f %s" % fn)
        else:
            os.system("rm -rf %s" % fn)
            
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


def check_bin_path(bfn, logFN=None):
    (tpath, se) = cmd_stdout("which %s" % bfn)
    assert(len(se) == 0)
    
    if len(tpath) == 0:
        error_log("Cannot find the path to program: %s" % bfn, logFN=logFN)

    return tpath
