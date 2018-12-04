from file_importer import FileImporter
from collections import defaultdict
import re

inp = FileImporter.get_input("/../input/4.txt").split("\n")
sorted_inp = sorted(inp, key = lambda x: re.match('\[(.*)\]', x).groups()[0])   # Sort by datetime

guard_asleep_chart = defaultdict(lambda: ['.' for i in range(60)])              # 2D Chart of date+guard mapped to the minutes they're asleep/awake
guards_total_min_slept = defaultdict(int)                                       # dict of guard id to total time slept

curr_guard = 0                                                                  # ID of current guard 
min_fall_asleep = 0                                                             # Minute the current guard fell asleep, tracking for when they wake.

for record in sorted_inp:
    re_match = re.match('\[(\d+-\d+-\d+ \d+:(\d+))\] (.*)', record) 
    [date, minute, action] = re_match.groups()                                  # Unpack date, minute, and action from the input
    date = date.split(' ')[0]                                                   # Get rid of hour/minute for date

    if action.startswith("Guard"):                                              # Starts shift
        curr_guard = int(action.split(' ')[1][1:])                              # Get guard ID from string

    elif action.startswith("falls"):
        min_fall_asleep = int(minute)

    elif action.startswith("wakes"):
        for i in range(min_fall_asleep, int(minute)):
            guard_asleep_chart[(date, curr_guard)][i] = '#'                    # Mark this entry as asleep

        guards_total_min_slept[curr_guard] += int(minute) - min_fall_asleep    

                                                                               # Get the guard ID with max sleep, 
                                                                               # filter our original chart by this ID, turn into 2D array
guard_max_sleep = max(guards_total_min_slept, key = guards_total_min_slept.get) 
filtered_chart = [ val for key, val in dict(guard_asleep_chart).items() if key[1] == guard_max_sleep ]

minute_most_likely = 0                                                         # Iterate through this guard's charts and find 
max_mins = 0                                                                   # The min he's most likely to be asleep
for col in range(0, 60):

    current_mins = 0
    for row in range(0, len(filtered_chart)):
        if filtered_chart[row][col] == '#':
            current_mins += 1

    if current_mins > max_mins:
        max_mins = current_mins
        minute_most_likely = col

print(guard_max_sleep * minute_most_likely)