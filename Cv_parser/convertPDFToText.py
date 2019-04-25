import PyPDF2,re,cv2
import itertools,pytesseract
import sys
import os



# pdfFileObj = open('D:\History\Practices\dataextraction\ALTMP_PRD_1.pdf', 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
def convertPDFToText(path):
    import os
    count=0
    increase=0
    print("enter",path)
    a=[]
    from PyPDF2 import PdfFileReader
    from pdf2image import convert_from_path
    out=[]
    paths=cwd=os.getcwd()+"/"+"resumes"
    pdftoppm_path = r"D:\poppler-0.512\bin\pdftoppm.exe"
    for filename in os.listdir(paths):
        
        
        files=paths+"/"+filename
        from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfpage import PDFPage
        from io import StringIO
        print (files)
        
        rsrcmgr = PDFResourceManager()
        print(rsrcmgr,"rsrcmgr")
        retstr = StringIO()
        print(retstr,"retstr")
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(files, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()
        print(text)
        fp.close()
        device.close()
        retstr.close()

        print(text,"string")
        print('inside')            
        return(text)



    
