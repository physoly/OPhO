import csv

bcc_addresses = []
with open('/mnt/c/Users/va648/downloads/vscode/opho/scripts/data/2023/opho2023-logins.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header
    for row in reader:
        receiver_address = row[0]
        bcc_addresses.append(receiver_address)

bcc_string = ', '.join(bcc_addresses)
print(bcc_string)