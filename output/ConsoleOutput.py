import json

class ConsoleOuptut:
    def output(self,record):
        print(json.dumps(record))