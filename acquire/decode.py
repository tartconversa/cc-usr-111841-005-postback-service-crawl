import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

class ResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows=[]
        self.key=None
        self.cells=[]
        self.cell=None
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='tr' and 'data-result-id' in attrs:
            self.key=attrs['data-result-id']; self.cells=[]
        if tag=='td' and self.key is not None:
            self.cell=[]
    def handle_data(self,data):
        if self.cell is not None:
            self.cell.append(data)
    def handle_endtag(self,tag):
        if tag=='td' and self.cell is not None:
            self.cells.append(''.join(self.cell)); self.cell=None
        if tag=='tr' and self.key is not None:
            self.rows.append(dict(key=self.key,value=dict(cells=self.cells)))
            self.key=None

def decode(body, headers):
    p=ResultParser(); p.feed(body.decode('utf-8')); return p.rows
