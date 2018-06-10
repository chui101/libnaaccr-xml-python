import re
from datetime import date,timedelta
# filters an xml etree element and returns the records
class VisFilter:

    def __init__(self, items = None):
        self.initialized = True
        self.convert_to_int_keys = ['dateOfDiagnosis','dateOfLastContact','patientIdNumber','derivedAjcc7StageGrp','ageAtDiagnosis']
        if items == None:
            self.items = ["patientIdNumber","sex","primarySite"]
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
                if key == "dateOfLastContact" and len(value) < 8:
                    pad = "00000101"
                    value = value + pad[len(value) - 8:]
                if key in self.convert_to_int_keys:
                    value = int(value)
                if key == "sex" or key == "vitalStatus":
                    value = str(value)
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
                    if key == "dateOfDiagnosis" and len(value) < 8:
                        pad = "00000101"
                        value = value + pad[len(value)-8:]
                    if key in self.convert_to_int_keys:
                        value = int(value)
                    if key == "primarySite":
                        value = value[0:3]
                    if key == "derivedAjcc7StageGrp":
                        if value < 100:
                            tumor_record['majorStageGrp'] = '0'
                        if value < 300 and value >= 100:
                            tumor_record['majorStageGrp'] = '1'
                        if value < 500 and value >= 300:
                            tumor_record['majorStageGrp'] = '2'
                        if value < 700 and value >= 500:
                            tumor_record['majorStageGrp'] = '3'
                        if value < 800 and value >= 700:
                            tumor_record['majorStageGrp'] = '4'
                    # commit
                    tumor_record[key] = value

            # tumor specific maths here (e.g. survival data)
            if tumor_record.has_key('dateOfLastContact') and tumor_record.has_key('dateOfDiagnosis'):
                start = tumor_record['dateOfDiagnosis']
                start = date(int(str(start)[0:4]), int(str(start)[4:6]), int(str(start)[6:8]))
                end = tumor_record['dateOfLastContact']
                end = date(int(str(end)[0:4]), int(str(end)[4:6]), int(str(end)[6:8]))
                followupdelta = end - start
                tumor_record['lengthOfFollowup'] = followupdelta.days
                tumors.append(tumor_record)
            else:
                print "WARNING: Dropping case with no date of last contact"
                print tumor_record

        return tumors



