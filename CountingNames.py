from collections import defaultdict

def count_unique_entries(file_path):
    unique_entries = set()
    entry_count = defaultdict(int)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Remove leading/trailing whitespaces and newline characters
                cleaned_line = line.strip()
                
                # Add each line to the set of unique entries
                unique_entries.add(cleaned_line)
                
                # Count occurrences of each line
                entry_count[cleaned_line] += 1

        # Print number of unique entries
        print(f"Number of unique entries: {len(unique_entries)}")

        # Print occurrences of each unique entry
        print("Occurrences of each unique entry:")
        for entry, count in entry_count.items():
            print(f"{entry}: {count}")

    except FileNotFoundError:
        print("File not found.")

# Replace 'file_path.txt' with the path to your file
file_path = 'list.txt'
count_unique_entries(file_path)
