import numpy as np
import csv

with open("result_buffer.csv") as history_file:
    dummy = []
    log_history = csv.reader(history_file)
    for row_record in log_history:
        dummy.append(row_record)

print(dummy[-1])