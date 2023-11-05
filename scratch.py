import csv
from datetime import datetime, timedelta
import hashlib

def hash_strings(*args):
    # Concatenate the strings
    concatenated_strings = ''.join(args)
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    # Update the hash object with the concatenated strings
    sha256_hash.update(concatenated_strings.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    hashed_value = sha256_hash.hexdigest()
    return hashed_value


print(hash_strings())