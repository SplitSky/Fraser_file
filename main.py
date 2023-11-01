import numpy as np
import os

filename = ""

file_out = "Milw_cont_"
headings = str()

with open(filename, 'r') as f:
    i = 0
    temp_f = open(file_out + str(i), 'w+');
    for line in f.readlines():
        if i % 1000:
            temp_f.close()
            temp_f = open(file_out + str(i), 'w+');
        temp_f.writeline(line)
    f.close()
    