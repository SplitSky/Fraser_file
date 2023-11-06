import csv

def replace_unsupported_chars(text):
    return ''.join(char if ord(char) < 256 else '?' for char in text)

input_file = 'Project_Timecards.csv'
output_file = 'Test2.csv'

with open(input_file, 'r', encoding='utf-8-sig') as utf8_file:
    csv_reader = csv.reader(utf8_file)
    data = [[replace_unsupported_chars(cell) for cell in row] for row in csv_reader]

with open(output_file, 'w', encoding='iso-8859-1') as iso8859_file:
    csv_writer = csv.writer(iso8859_file)
    csv_writer.writerows(data)

print(f"Conversion completed. Data has been saved to {output_file}.")
