import xml.etree.ElementTree as ET

class VisFilter:

    def __init__(self):
        self.initialized = True
        self.dataItems = ["patientIdNumber","sex","ageAtDiagnosis"]

    def expandtag(self,tag):
        return '{http://naaccr.org/naaccrxml}' + tag

    def filter(self,element):
        tumors = []
        # loop through all Item tags at the patient level
        patient_record = {}
        for patientitem in list(element.findall(self.expandtag("Item"))):
            if patientitem.get("naaccrId") in self.dataItems:
                patient_record[patientitem.get("naaccrId")] = patientitem.text

        # loop through all of the tumors
        for tumor in list(element.findall(self.expandtag("Tumor"))):
            tumor_record = {}
            # copy patient record into the tumor to flatten
            for key in patient_record.keys():
                tumor_record[key] = patient_record[key]
            # read tumor items from tumor element tree
            for tumoritem in list(tumor.findall(self.expandtag("Item"))):
                if tumoritem.get("naaccrId") in self.dataItems:
                    tumor_record[tumoritem.get("naaccrId")] = tumoritem.text
            tumors.append(tumor_record)

        return tumors


