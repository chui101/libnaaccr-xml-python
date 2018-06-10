from xml.etree import ElementTree
from filters import VisFilter
from output import MongoOutput
import time


class NaaccrXmlParser:

    def __init__(self, xml, filter, output):
        self.xml = xml
        self.filter = filter
        self.output = output

    def expandtag(self,tag):
        return '{http://naaccr.org/naaccrxml}' + tag

    def parse(self):
        count = 1
        for event, elem in ElementTree.iterparse(self.xml, events=('end',)):
            if event == "end":
                if elem.tag == self.expandtag("Patient"):
                    count += 1
                    results = self.filter.filter(elem)
                    for result in results:
                        self.output.output(result)
                    elem.clear()

if __name__ == "__main__":
    start = time.time()
    filter = VisFilter(items=["patientIdNumber","sex","vitalStatus","ageAtDiagnosis","countyAtDx2010","addrAtDxState","dateOfDiagnosis","primarySite","dateOfLastContact","derivedAjcc6StageGrp","derivedAjcc7StageGrp","race1"])
    output = MongoOutput()
    parser = NaaccrXmlParser("test.xml",filter,output)
    parser.parse()
    print(time.time() - start)

