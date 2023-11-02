import csv

# Function to generate a new output CSV file name
def get_output_filename(base_filename, count):
    return f"{base_filename}_{count}.csv"

input_filename = "Milwaukee Contacts - Wired+_With_PK.csv"
output_base_filename = "output"  # Replace with your desired output base filename
max_rows_per_file = 9998

with open(input_filename, 'r', newline='', encoding='iso-8859-1') as input_file:
    csv_reader = csv.reader(input_file)
    header = next(csv_reader)  # Read the header row

    line_count = 0
    file_count = 1

    output_filename = get_output_filename(output_base_filename, file_count)
    
    # Open the first output file for writing and write the header
    output_file = open(output_filename, 'w', newline='', encoding='iso-8859-1')
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(header)

    for row in csv_reader:
        csv_writer.writerow(row)
        line_count += 1

        if line_count >= max_rows_per_file:
            output_file.close()
            file_count += 1
            line_count = 0
            output_filename = get_output_filename(output_base_filename, file_count)
            
            # Open a new output file for writing and write the header
            output_file = open(output_filename, 'w', newline='', encoding='iso-8859-1')
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(header)

    # Close the last output file when the loop is finished
    output_file.close()

print("CSV files created successfully.")
