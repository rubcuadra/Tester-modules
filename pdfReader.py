from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

class PDF():
    def __init__(self, filePath):
        self.path = filePath
    def convert_to_string(self):
        rsrcmgr,retstr = PDFResourceManager(), StringIO()
        device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
        with file(self.path, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp,set(),check_extractable=True): #set(),maxpages=0, password="",caching=True, 
                interpreter.process_page(page)
        device.close()
        result = retstr.getvalue()
        retstr.close()
        return result
    def get_layouts_to_analyse(self): #<class 'pdfminer.layout.LTPage'>.
        layouts = []
        rsrcmgr,retstr = PDFResourceManager(), StringIO()
        device = PDFPageAggregator(rsrcmgr, laparams=LAParams()) #MAIN DIFFERENCE WITH CONVERT
        with file(self.path, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr,device)
            for page in PDFPage.get_pages(fp,set(),check_extractable=True): #set(),maxpages=0, password="",caching=True, 
                interpreter.process_page(page)
                layouts.append(device.get_result())
        device.close()
        result = retstr.getvalue()
        retstr.close()
        print result
        return layouts
    def get_table_of_contents(self):
        with open(self.path,'rb') as fp:
            outlines = PDFDocument(PDFParser(fp)).get_outlines()
            for (level,title,dest,a,se) in outlines:
                print (level, title)
    def get_as_list(self):
        return self.convert_to_string().split('\n')
    def print_as_list(self):
        l = self.get_as_list()
        for i in xrange(0,len(l)):
            print '[%s] %s'%(i,l[i]) 