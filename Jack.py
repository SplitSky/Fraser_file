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
        self.dictKeys = ['EPH_PN_Reference_only', 'Item_Number', 'Item_Name', 'Product_Family', 'Item_Category', 'Product_Type', 'Revenue_Type', 'Kofax_Product_Code', 'Attribute_Type', 'Product_Line_Code', 'Fulfillment_Channel', 'Maintenance_Required', 'Default_Renewal_Pricing_Method', 'Term_on_Prem_Schedule', 'Delivery_Method', 'Asset_Conversion', 'Asset_Amendment_Behavior', 'Entitlement_Conversion_used_with_Term_on_Prem_only', 'Country_Of_Origin', 'Warehouse', 'Dropship_Enabled', 'Special_Handling', 'Default_Term', 'Default_Pack', 'Default_SLO', 'Default_Quantity', 'Subscription_Term', 'Default_Attribute', 'Charge_Type', 'Billing_Type', 'Subscription_Type', 'Price_Editable', 'Quantity_Editable', 'Subscription_Pricing', 'eCopy_Loyalty_Check', 'Perpetual_to_Term_Mapping_CPQ_rationalized_part_number', 'Perpetual_to_Term_Mapping_AX_rationalized_part_number', 'Licence_Fulfillment_Only', 'NSI_Upgrade_Check_for_V7', 'Associated_Maintenance_sku', 'Bundle_set_up_required', 'Configurations_Event', 'Configuration_Type', 'Pricing_Method', 'Block_Pricing_Field', 'Services_Billing_Type', 'Allow_Override_Prediscounted_Sales_Price', 'Feature', 'Configuration_attributes_to_set_up_1', 'Configuration_attributes_to_set_up_2', 'Configuration_attributes_to_set_up_3', 'Product_Options_Set_up_1']
        for name in self.dictKeys:
            self.other_data.append(row[name])
        # Delimit sku
        self.sku = row['Legacy_SKU_Search'].split(';')
    
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