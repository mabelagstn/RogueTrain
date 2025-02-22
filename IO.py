# CS1010S --- Programming Methodology
#
# Mission 6
#

import datetime
import csv

def read_csv(csvfilename):
    rows = ()
    with open(csvfilename) as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            rows += (tuple(row), )
    return rows

###############
# Station ADT #
###############

def make_station(station_code, station_name):
    return (station_code, station_name)

def get_station_code(station):
    return station[0]

def get_station_name(station):
    return station[1]

test_station1 = make_station('CC2', 'Bras Basah')
test_station2 = make_station('CC3', 'Esplanade')
test_station3 = make_station('CC4', 'Promenade')


#############
# Train ADT #
#############

def make_train(train_code):
    return (train_code,)

test_train = make_train('TRAIN 0-0')

def get_train_code(train):
    return train[0]

############
# Line ADT #
############

def make_line(name, stations):
    return (name, stations)

def get_line_name(line):
    return line[0]

def get_line_stations(line):
    return line[1]

def get_station_by_name(line, station_name):
    p = tuple(filter(lambda x: x[-1] == station_name, line[-1]))
    return p[0] if len(tuple(p)) > 0 else None

def get_station_by_code(line, station_code):
    q = tuple(filter(lambda x: x[-2] == station_code, line[-1]))
    return q[0] if len(tuple(q)) > 0 else None

def get_station_position(line, station_code):
    try:
        return list(map(lambda x: x[0], line[-1])).index(station_code)
    except:
        return -1

test_line = make_line('Circle Line', (test_station1, test_station2, test_station3))

def parse_lines(data_file):
    rows = read_csv(data_file)[1:]
    lines = ()
    curr_line_name = rows[0][2]
    curr_line_stations = ()
    for row in rows:
        code, station_name, line_name = row
        if line_name == curr_line_name:
            # Addition 1
            curr_line_stations += (make_station(code, station_name),)
        else:
            # Addition 2
            curr_line = make_line(curr_line_name, curr_line_stations)
            lines += (curr_line,)
            curr_line_name = line_name
            curr_line_stations = ()
            curr_line_stations += (make_station(code, station_name),)
    # Addition 3
    lines += (make_line(curr_line_name, curr_line_stations),)
    return lines

LINES = parse_lines('station_info.csv')
CCL = tuple(filter(lambda line: get_line_name(line) == 'Circle Line', LINES))[0]

#####################
# ScheduleEvent ADT #
#####################

def make_schedule_event(train, train_position, time):
    return (train, train_position, time)

def get_train(schedule_event):
    return schedule_event[0]

def get_train_position(schedule_event):
    return schedule_event[1]

def get_schedule_time(schedule_event):
    return schedule_event[2]

test_loc_id1 = 2.5
test_loc_id2 = 1

###############
# Scorer ADT  #
###############

def make_scorer():
    return {}

def blame_train(scorer, train_code):
    scorer[train_code] = scorer.get(train_code, 0) + 1
    return scorer

def get_blame_scores(scorer):
    return tuple(scorer.items())

# Use this to keep track of each train's blame score.
SCORER = make_scorer()


