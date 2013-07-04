from scai_utils import *

def get_pdf_npages(pdfFN):
#if __name__ == "__main__":
#    pdfFN = "/mnt/My_Dropbox/GreenCard_EB1A/citing/TourvilleEtAl-2013.pdf"

    check_file(pdfFN)

    # Make sure that pdftk is availalbe 
    so = cmd_stdout("which pdftk")
    if len(so) == 0:
        raise Exception, "pdftk does not appear to be available"

    (so, se) = cmd_stdout("pdftk %s dump_data output" % pdfFN)
    assert(len(se) == 0)
    so = so.split("\n")
    
    pCount = -1
    for (i0, tline) in enumerate(so):
        if tline.startswith("NumberOfPages: "):
            pCount = int(tline.replace("NumberOfPages: ", ""))
            break

    assert(pCount > 0)

    return pCount
    
    
