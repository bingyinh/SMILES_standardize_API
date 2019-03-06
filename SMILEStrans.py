import mechanize
from bs4 import BeautifulSoup

class SMILEStrans(object):
    def __init__(self, smiles = ''):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.set_handle_redirect(False)
        self.br.set_handle_refresh(False)
        self.br.set_debug_redirects(True)
        self.br.addheaders=[('User-Agent', 'Mozilla/5.0'),
                            ('Cache-Control', 'max-age=0'),
                            ('Connection', 'keep-alive')]
        self.br.open('https://cactus.nci.nih.gov/translate/index.html#Form')
        self.SMILES = smiles
        self.brtxt = None
        self.trans = ''
        self.response = None
        self.responsetxt = ''
        self.result = ''

    def setSMILES(self, smiles):
        if isinstance(smiles, str) or isinstance(smiles, unicode):
            self.__init__()
            self.SMILES = smiles
            print("SMILES: %s" %(self.SMILES))
            self.trans = ''

    def translate(self):
        self.br.select_form(name="form")
        self.brtxt = self.br.form.find_control("smiles")
        if self.brtxt is None:
            raise ValueError("[Form] Cannot translate %s" %(self.SMILES))
        self.brtxt.value = self.SMILES
        self.response = self.br.submit()
        self.responsetxt = self.response.read()
        print 
        soup = BeautifulSoup(self.responsetxt, 'html.parser')
        if soup.title.text == u'USMILES Result':
            if soup.find('b') is not None:
                self.result = soup.find('b').text
                return self.result
            else:
                raise ValueError("[Parse] Cannot find results in the page returned.")
        elif soup.title.text == u'Translation Error':
            if soup.find('h3') is not None:
                raise ValueError(soup.find('h3').text)
            else:
                raise ValueError('[Translation] Unknown translation error.')
        else:
            raise ValueError('Unknown error.')