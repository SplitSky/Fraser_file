import csv
from datetime import datetime, timedelta

output_base_filename = "output.csv"
encoding = 'iso-8859-1'

def get_week_and_year(date_str):
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")  # Assuming date format is "MM/DD/YYYY"
    date_obj += timedelta(days=1)
    week_number = date_obj.strftime("%U")  # Get the week number
    year = date_obj.year
    return int(week_number), year

def get_sunday_of_week(date_str):
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")  # Assuming date format is "MM/DD/YYYY"
    date_obj += timedelta(days=1)
    monday = date_obj - timedelta(days=date_obj.weekday())  # Calculate Monday by subtracting days
    sunday = monday - timedelta(days=1)
    return sunday.strftime("%d/%m/%Y")

def are_dates_in_same_week_and_year(date_str1, date_str2):
    # Convert the input date strings to datetime objects using the same format
    date_obj1 = datetime.strptime(date_str1, "%d/%m/%Y")
    date_obj1 += timedelta(days=1)
    date_obj2 = datetime.strptime(date_str2, "%d/%m/%Y")
    date_obj2 += timedelta(days=1)
    # Get the week and year for both dates
    week1, year1 = get_week_and_year(date_str1)
    week2, year2 = get_week_and_year(date_str2)
    # Check if both dates are in the same week and year
    return week1 == week2 and year1 == year2

class dataGroup(object):
    def __init__(self, filename):
        # reads in a csv file and populates it with groups
        self.fullList = []
        self.output_filename = output_base_filename
    
        with open(filename, 'r', encoding=encoding) as input_file:
            reader = csv.DictReader(input_file)
            fieldnames = reader.fieldnames
            i = 0
            for row in reader:
                if i == 0:
                    #print(row.keys())
                    #print(list(row.keys())[0])
                    self.header = list(str(item) for item in row.keys())
                    self.header[0] = self.header[0].replace('\ufeff', '')
                self.check_group(row)
                
                if i % 100 == 0:
                    print(f'{i//100}00')
                elif i % 1000 == 0:
                    print(f'{i// 1000}000')
                i += 1
            
        # Write into a file
        print("Done processing. Now Writing")
        print(f'number of groups = {len(self.fullList)}')
        self.write_row(self.header)
        for entry in self.fullList:
            timecards = entry.getRow(24)
            for timecard in timecards:
                self.write_row(timecard)
        print("Finished writing")
        
    def check_groupExists(self, userName, projectName, shareDate):
        # returns the index or false
        i = 0
        for group in self.fullList:
            if (group.User_Name == userName and group.Project_Name == projectName):
                # found group > return index
                if (are_dates_in_same_week_and_year(group.Date_Shared, shareDate)):
              
                    # check for date
                    #print("Group found")
                    return i
            i += 1
        #print("Group not found")
        return False
        
    def check_group(self, row):
        exist = self.check_groupExists(userName=row['User: Name'], projectName=row['Project: Name'], shareDate=row['Date (Shared)'])
        
        if (isinstance(exist, bool)):
            self.fullList.append(group(row))
        else:
            hoursTemp = float(row['Hours Actual'])
            idTemp = row['Time Entry: ID']
            self.fullList[exist].updateExisting(hoursTemp, idTemp)
        
    def write_row(self, row):
        with open(self.output_filename, 'a', newline='', encoding='utf-8') as output_file:
            csv_writer = csv.writer(output_file)
            #print("Pringitng row")
            #print(row)
            csv_writer.writerow(row)
            
class group(object):
    def __init__(self,row):
        self.Time_Entry_ID = str(row['Time Entry: ID'])
        self.Time_Entry_Approved = str(row['Time Entry: Approved'])
        self.Time_Entry_Billable = str(row['Time Entry: Billable'])
        self.Time_Entry_Notes = str(row['Time Entry: Notes'])
        self.Time_Entry_Requires_Approval = str(row['Time Entry: Requires Approval'])
        self.Time_Entry_Status = str(row['Time Entry: Status'])
        self.Note = str(row['Time Entry: Status Note'])
        self.Time_Entry_Taxable = str(row['Time Entry: Taxable'])
        self.Time_Entry_Type = str(row['Time Entry: Type'])
        self.User_Name = str(row['User: Name'])
        self.Project_Name = str(row['Project: Name'])
        self.Task_Name = str(row['Task: Name'])
        self.Role = str(row['Role'])
        self.Currency = str(row['Currency'])
        self.Location = str(row['Location'])
        self.Date_Shared = str(row['Date (Shared)'])
        self.Date_Shared_Created = str(row['Date (Shared Created)'])
        self.Date_Submission_Submitted = str(row['Date (Submission Submitted)'])
        self.Date_Submission_Approved = str(row['Date (Submission Approved)'])
        self.Date_Submission_Rejected = str(row['Date (Submission Rejected)'])
        self.Hours_Actual = float(row['Hours Actual'])
        self.Fees_Actual = str(row['Fees Actual'])
        self.Cost_Actual = str(row['Cost Actual'])
        self.User_Cost_Rate = str(row['User Cost Rate'])
        self.Users_Bill_Rate = str(row['Users Bill Rate (from User Record)'])
        self.TE_Bill_Rate = str(row['TE Bill Rate'])
        self.TE_Cost_Rate = str(row['TE Cost Rate'])
        
        self.spareIDs = [self.Time_Entry_ID]
        
    def change_Date(self):
        self.Date_Shared = get_sunday_of_week(self.Date_Shared)
        
    def updateExisting(self, hours, timeCardID):
        self.Hours_Actual += hours
        self.spareIDs.append(timeCardID)
        
    def compileData(self):
         return [
                self.Time_Entry_ID,
                self.Time_Entry_Approved,
                self.Time_Entry_Billable,
                self.Time_Entry_Notes,
                self.Time_Entry_Requires_Approval,
                self.Time_Entry_Status,
                self.Note,
                self.Time_Entry_Taxable,
                self.Time_Entry_Type,
                self.User_Name,
                self.Project_Name,
                self.Task_Name,
                self.Role,
                self.Currency,
                self.Location,
                self.Date_Shared,
                self.Date_Shared_Created,
                self.Date_Submission_Submitted,
                self.Date_Submission_Approved,
                self.Date_Submission_Rejected,
                self.Hours_Actual,
                self.Fees_Actual,
                self.Cost_Actual,
                self.User_Cost_Rate,
                self.Users_Bill_Rate,
                self.TE_Bill_Rate,
                self.TE_Cost_Rate
            ]
        
    def getRow(self, max_time):
        print("Get Row called")
        self.change_Date() # Fix date
        if (self.Hours_Actual > max_time):
            # fragment timecards
            rows_out = []
            total_time = self.Hours_Actual
            j = 0
            while (total_time > 0):
                if (total_time < max_time and total_time > 0):
                    # assign spare ID
                    self.Time_Entry_ID = self.spareIDs[j]
                    # assign leftover hours
                    self.Hours_Actual = total_time
                    total_time = 0
                    rows_out.append(self.compileData())
                    j += 1
                else:
                    # assign spare ID
                    self.Time_Entry_ID = self.spareIDs[j]
                    # assign leftover hours
                    self.Hours_Actual = max_time
                    total_time -= max_time
                    rows_out.append(self.compileData())
                    j += 1

            return rows_out
        else:
            return [self.compileData()]
    
# Open the input CSV file
def main():
    full_name = 'Project_Timecards.csv'
    test_name = 'FullDataConverted.csv'
    a = dataGroup(test_name)
    
main()