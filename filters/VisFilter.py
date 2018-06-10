import re

class VisFilter:

    def __init__(self, items = None):
        self.initialized = True
        if items == None:
            self.items = ["patientIdNumber","sex","ageAtDiagnosis"]
        else:
            self.items = items

    def expandtag(self,tag):
        return '{http://naaccr.org/naaccrxml}' + tag

    def filter(self,element):
        tumors = []
        # loop through all Item tags at the patient level
        patient_record = {}
        for patientitem in list(element.findall(self.expandtag("Item"))):
            if patientitem.get("naaccrId") in self.items:
                key = patientitem.get("naaccrId")
                value = patientitem.text
                # additional field-specific filtering
                if re.match('^\d+$',value):
                    value = int(value)
                # commit
                patient_record[key] = value

        # loop through all of the tumors
        for tumor in list(element.findall(self.expandtag("Tumor"))):
            tumor_record = {}
            # copy patient record into the tumor to flatten
            for key in patient_record.keys():
                tumor_record[key] = patient_record[key]
            # read tumor items from tumor element tree
            for tumoritem in list(tumor.findall(self.expandtag("Item"))):
                if tumoritem.get("naaccrId") in self.items:
                    key = tumoritem.get("naaccrId")
                    value = tumoritem.text
                    # additional field-specific filtering
                    if re.match('^\d+$', value):
                        value = int(value)

                    #commit
                    tumor_record[key] = value
            tumors.append(tumor_record)

        return tumors



