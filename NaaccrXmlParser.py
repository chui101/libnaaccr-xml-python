from xml.etree import ElementTree
from filters import VisFilter
from output import ConsoleOutput
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
                    result = self.filter.filter(elem)
                    self.output.output(result)
                    elem.clear()

if __name__ == "__main__":
    start = time.time()
    filter = VisFilter.VisFilter()
    output = ConsoleOutput.ConsoleOuptut()
    parser = NaaccrXmlParser("test.xml",filter,output)
    parser.parse()
    print(time.time() - start)

