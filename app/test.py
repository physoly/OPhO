import csv

REQUIRED_FIELDS = [0,2,3,4,5]

def valid_entry(line):
    for field in REQUIRED_FIELDS:
        if line[field] == '':
            return False
    return True

names = []
with open ('/mnt/c/Users/va648/downloads/vscode/OPhO/scripts/data/2023/opho2023.csv', 'r') as csvin:
    for line in csv.reader(csvin):
        if valid_entry(line):
                uname = line[2].strip().replace(" ", "_")
                email = line[5].strip()

                if len(uname) > 25:
                    uname=uname[:26]
                    
                idx = 1
                while uname in names:
                    uname = uname + str(idx)
                    idx = idx + 1
        names.append(uname)
        print(names)
        names = []