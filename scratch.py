import csv, copy
output_base_filename = "output.csv"
encoding = 'utf-8'


with open('FullDataConverted.csv', 'r', encoding=encoding) as input_file:
    reader = csv.DictReader(input_file)
    fieldnames = reader.fieldnames
    i = 0
    for row in reader:
        if i == 0:
            print(list(row.keys()))
        i += 1
        
