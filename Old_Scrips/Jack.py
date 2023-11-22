import csv, copy
output_base_filename = "output.csv"
encoding = 'utf-8'

class dataGroup(object):
    def __init__(self, filename):
        # reads in a csv file and popul ates it with groups
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
        self.dictKeys = ['Type', 'SFDC Product ID QA', 'SFDC Product ID PRODUCTION', 'EPH PN Reference only', 'Item Number', 'Item Name', 'Sort Order', 'Main Section', 'Product Status', 'Active (product', 'System ID Required', 'Product Family', 'Item Category', 'Legacy NDI Product Family', 'Product Type', 'Fees Product Type', 'Revenue Type', 'Kofax Product Code', 'Attribute Type', 'Product Line Code', 'Fulfillment Channel', 'ULP Set up notes (Include in the OFP', 'Reseller 10x5 (formerly Standard)', 'Direct 10x5 (formerly Direct)', 'Direct 24x7', 'Reseller 24x7', 'Reseller Legacy 10x5', 'Direct Legacy 10x5', 'Exception', 'Maintenance Required', 'Default Renewal Pricing Method', 'USD', 'EUR', 'GBP', 'AUD', 'SGD', 'Pricing Note', 'Max. Discount (Per Royalty Obligation)', 'Royalty Note', 'Pack Pricing Status', 'Discount Schedule Name (If removal, please add remove to this field', 'Discount Schedule Status (if applicable, include volume pricing set up on discount schedule tab)', 'Term on Prem Schedule', 'Perpetual to Term Mapping (CPQ rationalized part number)', 'Perpetual to Term Mapping (AX rationalized part number)', 'Licence Fulfillment Only', 'NSI Upgrade Check (for V7)', 'Associated Maintenance sku', 'Bundle set up required', 'Configurations Event', 'Configuration Type', 'Pricing Method', 'Block Pricing Field', 'IsServicesProduct', 'Services Billing Type', 'Allow Override Prediscounted Sales Price', 'Royalty (Build out tab for 3rd party tab', 'Finance Notification for Royalty Set up in NetSuite', 'GPL Note', 'CPM Notes', 'Maintenance PN for product options', 'Feature', 'Configuration attributes to set up 1', 'Configuration attributes to set up 2', 'Configuration attributes to set up 3', 'Product Options Set up 1', 'Product Options Set up 2', '']
        
        for name in self.dictKeys:
            self.other_data.append(row[name])
        # Delimit sku
        self.sku = row['Legacy SKU Search'].split(';')
    
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
    test_name = 'FullDataConverted.csv'
    a = dataGroup(test_name)
    
main()