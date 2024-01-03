def find_missing_values(file_path):
    # Create a set to store the integers read from the file
    numbers_set = set()

    # Read integers from the file and add them to the set
    with open(file_path, 'r') as file:
        for line in file:
            number = int(line.strip())  # Convert each line to an integer
            numbers_set.add(number)

    # Create a set containing all integers from 1 to 700
    full_range_set = set(range(1, max(numbers_set)))
    print(max(numbers_set))

    # Find the missing values by subtracting the numbers_set from the full_range_set
    missing_values = full_range_set - numbers_set
    print(len(missing_values))
    return sorted(missing_values)  # Return sorted list of missing values

# Replace 'file_path.txt' with the path to your .txt file
file_path = 'dir.txt'

missing_values_list = find_missing_values(file_path)

if missing_values_list:
    print("Missing values:")
    print(missing_values_list)
else:
    print("No missing values found.")
