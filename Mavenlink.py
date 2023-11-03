import csv
from datetime import datetime, timedelta

output_base_filename = "output.csv"

def get_week_and_year(date_str):
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")  # Assuming date format is "MM/DD/YYYY"
    week_number = date_obj.strftime("%U")  # Get the week number
    year = date_obj.year
    return int(week_number), year

def get_monday_of_week(date_str):
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")  # Assuming date format is "MM/DD/YYYY"
    monday = date_obj - timedelta(days=date_obj.weekday())  # Calculate Monday by subtracting days
    return monday.strftime("%d/%m/%Y")

def are_dates_in_same_week_and_year(date_str1, date_str2):
    # Convert the input date strings to datetime objects using the same format
    date_obj1 = datetime.strptime(date_str1, "%d/%m/%Y")
    date_obj2 = datetime.strptime(date_str2, "%d/%m/%Y")
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
    
        with open(filename, 'r') as input_file:
            reader = csv.DictReader(input_file)
            fieldnames = reader.fieldnames
            i = 0
            for row in reader:
                if i == 0:
                    print(row.keys())
                    print(list(row.keys())[0])
                    self.header = list(str(item) for item in row.keys())
                    self.header[0] = self.header[0].replace('\ufeff', '')
                self.check_group(row)
                i += 1
        # Write into a file
        self.write_row(self.header)
        for entry in self.fullList:
            timecards = entry.getRow(24)
            for timecard in timecards:
                self.write_row(timecard)
        
    def check_groupExists(self, userName, projectName, shareDate):
        # returns the index or false
        i = 0
        for group in self.fullList:
            if (group.User_Name == userName and group.Project_Name == projectName):
                # found group > return index
                if (are_dates_in_same_week_and_year(group.Date_Shared_Created, shareDate)):
                    # check for date
                    print("Group found")
                    return i
            i += 1
        print("Group not found")
        return False
        
    def check_group(self, row):
        exist = self.check_groupExists(userName=row['User: Name'], projectName=row['Project: Name'], shareDate=row['Date (Shared)'])
        if (exist == False):
            self.fullList.append(group(row))
        else:
            hoursTemp = float(row['Hours Actual'])
            idTemp = row['\ufeffTime Entry: ID']
            self.fullList[exist].updateExisting(hoursTemp, idTemp)
        
    def write_row(self, row):
        with open(self.output_filename, 'a', newline='', encoding='iso-8859-1') as output_file:
            csv_writer = csv.writer(output_file)
            print("Pringitng row")
            print(row)
            csv_writer.writerow(row)
            
class group(object):
    def __init__(self,row):
        self.Time_Entry_ID = row['\ufeffTime Entry: ID']
        self.Time_Entry_Approved = row['Time Entry: Approved']
        self.Time_Entry_Billable = row['Time Entry: Billable']
        self.Time_Entry_Notes = row['Time Entry: Notes']
        self.Time_Entry_Requires_Approval = row['Time Entry: Requires Approval']
        self.Time_Entry_Status = row['Time Entry: Status']
        self.Note = row['Time Entry: Status Note']
        self.Time_Entry_Taxable = row['Time Entry: Taxable']
        self.Time_Entry_Type = row['Time Entry: Type']
        self.User_Name = row['User: Name']
        self.Project_Name = row['Project: Name']
        self.Task_Name = row['Task: Name']
        self.Role = row['Role']
        self.Currency = row['Currency']
        self.Location = row['Location']
        self.Date_Shared = row['Date (Shared)']
        self.Date_Shared_Created = row['Date (Shared Created)']
        self.Date_Submission_Submitted = row['Date (Submission Submitted)']
        self.Date_Submission_Approved = row['Date (Submission Approved)']
        self.Date_Submission_Rejected = row['Date (Submission Rejected)']
        self.Hours_Actual = float(row['Hours Actual'])
        self.Fees_Actual = row['Fees Actual']
        self.Cost_Actual = row['Cost Actual']
        self.User_Cost_Rate = row['User Cost Rate']
        self.Users_Bill_Rate = row['Users Bill Rate (from User Record)']
        self.TE_Bill_Rate = row['TE Bill Rate']
        self.TE_Cost_Rate = row['TE Cost Rate']
        
        self.spareIDs = [self.Time_Entry_ID]
        
    def change_Date(self):
        self.Date_Shared = get_monday_of_week(self.Date_Shared)
        
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
                    j -= 1
                    # assign leftover hours
                    self.Hours_Actual = total_time
                    rows_out.append(self.compileData())
                else:
                    # assign spare ID
                    self.Time_Entry_ID = self.spareIDs[j]
                    j -= 1
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
    full_name = 'Project_Timecard_test.csv'
    a = dataGroup('Test1.csv')
    
main()