import json

class ConsoleOutput:
    def output(self,record):
        print(json.dumps(record))