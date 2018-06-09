from xml.etree import ElementTree
import time
import json

class NaaccrXmlParser:

    def __init__(self,xml):
        self.xml = xml

    def expandtag(self,tag):
        return '{http://naaccr.org/naaccrxml}' + tag

    def parse(self):
        count = 1
        for event, elem in ElementTree.iterparse(self.xml, events=('end',)):
            if event == "end":
                if elem.tag == self.expandtag("Patient"):
                    count += 1
                    self.parsepatient(elem)
                    elem.clear()

    def parsepatient(self,elem):
        record = {}
        for patientitem in list(elem):
            if patientitem.tag == self.expandtag('Item'):
                key = patientitem.get('naaccrId')
                value = patientitem.text
                record[key] = value
            if patientitem.tag == self.expandtag('Tumor'):
                if not record.has_key('tumors'):
                    record['tumors'] = []
                record['tumors'].append(self.parsetumor(patientitem))
        print (json.dumps(record,indent=True))
        return record

    def parsetumor(self,elem):
        tumorrecord = {}
        for tumoritem in list(elem):
            if tumoritem.tag == self.expandtag('Item'):
                key = tumoritem.get('naaccrId')
                value = tumoritem.text
                tumorrecord[key] = value
        return tumorrecord

if __name__ == "__main__":
    start = time.time()
    parser = NaaccrXmlParser("test.xml")
    parser.parse()
    print(time.time() - start)