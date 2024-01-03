import csv, copy
output_base_filename = "output.csv"
encoding = 'utf-8'

class dataGroup(object):
    def __init__(self, filename):
        # reads in a csv file and populates it with groups
        self.fullList = []
        self.header = []
        self.output_filename = output_base_filename
        with open(filename, 'r', encoding=encoding) as input_file:
            reader = csv.DictReader(input_file)
            fieldnames = reader.fieldnames
            i = 0
            for row in reader:
                if i == 0:
                    self.header = row.keys()
                self.fullList.append(group(row))
                i += 1
        
        # Write into a file
        print("Done processing. Now Writing")
        print(f'number of groups = {len(self.fullList)}')
        self.write_row(self.header)
        for entry in self.fullList:
            timecards = entry.getRows()
            for timecard in timecards:
                self.write_row(timecard)
        print("Finished writing")
        
    def write_row(self,row):
        with open(self.output_filename, 'a', newline='', encoding='utf-8') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(row)
            
class group(object):
    def __init__(self,row):
        self.other_data = []
        print('Keys')
        print(list(row.keys()))
        key1  = '\ufeffDuplicate: Master Bean No'
        key2 =  'Kofax Account Email Domains (PROD)'
        key3 = 'Duplicate: Account: List of Unique Email Domains'
        key4 = ''
        self.dictKeys = [key1, key2]
        
        for name in self.dictKeys:
            self.other_data.append(row[name])
        # Delimit sku
        if len(row[key3]) != row[key3].split(';'):
            print("Delimited")
        self.sku = row[key3].split(';')

    
    def getRows(self):
        data_out = []
        print(self.sku)
        for value in self.sku:
            temp = []
            print(f'value={value}')
            temp = self.other_data.copy()
            temp.append(value)
            print(f'len={len(self.other_data)}')
            data_out.append(temp)
            print(temp)
        return data_out
        
# Open the input CSV file
def main():
    full_name = 'Project_Timecards.csv'
    test_name = 'Test.csv'
    a = dataGroup(test_name)
    
main()