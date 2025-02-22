# CS1010S --- Programming Methodology
#
# Mission 4
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

#############    DO NOT MODIFY THIS SECTION  #####################
import datetime
from IO import * # IMPORT ALL DATA VARIABLE AND ADT FUNCTIONS
##################################################################

###########
# Task 1  #
###########

def make_train_position(is_moving, from_station, to_station):
    ''' Do NOT modify this function'''
    return (is_moving, from_station, to_station)

def get_is_moving(train_position):
    return train_position[0]

def get_direction(line, train_position):
    if get_station_position(line, get_station_code(train_position[1])) < get_station_position(line, get_station_code(train_position[2])):
        return 0
    else:
        return 1
    
def get_stopped_station(train_position):
    if get_is_moving(train_position):
        return None
    else:
        return train_position[1]
    
def get_previous_station(train_position):
    if get_is_moving(train_position):
        return train_position[1]
    else:
        return None
    
def get_next_station(train_position):
    return train_position[2]


# UNCOMMENT THE CODE BELOW TO TEST YOUR TASK 1
print("## Task 1 ##")
test_train_position1 = make_train_position(False, test_station1, test_station2)
test_train_position2 = make_train_position(True, test_station3, test_station2)
print(get_is_moving(test_train_position2))
print(get_direction(test_line, test_train_position1))
print(get_stopped_station(test_train_position1))
print(get_previous_station(test_train_position2))
print(get_next_station(test_train_position2))

# Expected Output #
# True
# 0
# ('CC2', 'Bras Basah')
# ('CC4', 'Promenade')
# ('CC3', 'Esplanade')

def parse_events_in_line(data_file, line):
    rows = read_csv(data_file)[1:]
    events = ()
    for row in rows:
        train, is_moving, from_station, to_station, date, time = row
        train = make_train(train)
        is_moving = (lambda x: True if x == 'True' else False)(is_moving)
        from_station = get_station_by_code(line, from_station)
        to_station = get_station_by_code(line, to_station)
        train_position = make_train_position(is_moving, from_station, to_station)
        datetime_date = tuple(map(int, tuple(date.split('/'))))[::-1]
        datetime_time = tuple(map(int, tuple(time.split(':'))))
        time = datetime_date + datetime_time
        events += (make_schedule_event(train, train_position,
                                       datetime.datetime(time[0], time[1], time[2],
                                                         time[3], time[4])),)
    return events

def is_valid_event_in_line(bd_event, line):
    # From and To stations are adjacent
    # must occur between 7am - 11pm
    if get_is_moving(get_train_position(bd_event)):
        if abs(get_station_position(line, get_station_code(get_previous_station(get_train_position(bd_event)))) -
           get_station_position(line, get_station_code(get_next_station(get_train_position(bd_event))))) == 1:
            if get_schedule_time(bd_event).hour >= 7 and not (get_schedule_time(bd_event).hour == 23 and get_schedule_time(bd_event).minute > 0):
                return True
            else:
                return False
        else:
            return False
    else:
        if abs(get_station_position(line, get_station_code(get_stopped_station(get_train_position(bd_event)))) -
           get_station_position(line, get_station_code(get_next_station(get_train_position(bd_event))))) == 1:
            if get_schedule_time(bd_event).hour >= 7 and not (get_schedule_time(bd_event).hour == 23 and get_schedule_time(bd_event).minute > 0):
                return True
            else:
                return False
        else:
            return False

def get_valid_events_in_line(bd_events, line):
    return tuple(filter(lambda ev: is_valid_event_in_line(ev, line), bd_events))


# UNCOMMENT THE CODE BELOW AFTER YOU ARE DONE WITH TASK 1. THIS IS NOT OPTIONAL TESTING #
test_bd_event1 = make_schedule_event(test_train, test_train_position2, datetime.datetime(2016, 1, 1, 9, 27))
test_bd_event2 = make_schedule_event(test_train, test_train_position1, datetime.datetime(2016, 1, 1, 2, 25))
BD_EVENTS = parse_events_in_line('breakdown_events.csv', CCL)
VALID_BD_EVENTS = get_valid_events_in_line(BD_EVENTS, CCL)
FULL_SCHEDULE = parse_events_in_line('train_schedule.csv', CCL)


###########
# Task 2a #
###########

def get_schedules_at_time(train_schedule, time):
    schedule = ()
    for t in train_schedule:
        if get_schedule_time(t) == time:
            schedule += (t,)
    return schedule

# UNCOMMENT THE CODE BELOW TO TEST YOUR TASK 2A
print("## Task 2a ##")
test_datetime = datetime.datetime(2017, 1, 6, 6, 0)
test_schedules_at_time = get_schedules_at_time(FULL_SCHEDULE[:5], test_datetime)
print(test_schedules_at_time[1])

# Expected Output #
# (('TRAIN 1-0',), (False, ('CC29', 'HarbourFront'), ('CC28', 'Telok Blangah')), datetime.datetime(2017, 1, 6, 6, 0))

###########
# Task 2b #
###########

def get_location_id_in_line(bd_event, line):
    pos       = get_train_position(bd_event)
    moving    = get_is_moving(pos)
    st1,st2   = get_previous_station(pos) if moving else get_stopped_station(pos),\
                get_next_station(pos)     if moving else get_stopped_station(pos)
    pos1,pos2 = get_station_position(line, get_station_code(st1)),\
                get_station_position(line, get_station_code(st2))
    return min(pos1,pos2) + 0.5 if moving else min(pos1,pos2)


def get_schedules_near_loc_id_in_line(train_schedule, line, loc_id):
    schedule = ()
    for t in train_schedule:
        if abs(loc_id - get_location_id_in_line(t, line)) <= 0.5:
            schedule += (t,)
    return schedule

# UNCOMMENT THE CODE BELOW TO TEST YOUR TASK 2B
# print("## Task 2b ##")
# test_schedules_near_loc_id = get_schedules_near_loc_id_in_line(FULL_SCHEDULE[:10], CCL, test_loc_id1)
# print(test_schedules_near_loc_id[1])

# Expected Output #
# (('TRAIN 0-0',), (True, ('CC3', 'Esplanade'), ('CC4', 'Promenade')), datetime.datetime(2017, 1, 6, 6, 5))


###########
# Task 2c #
###########

def get_rogue_schedules_in_line(train_schedule, line, time, loc_id):
    return get_schedules_near_loc_id_in_line(get_schedules_at_time(train_schedule, time), line, loc_id)

# UNCOMMENT THE CODE BELOW TO TEST YOUR TASK 2C
# print("## Task 2c ##")
# test_bd_event3 = VALID_BD_EVENTS[0]
# test_loc_id3 = get_location_id_in_line(test_bd_event3, CCL)
# test_datetime3 = get_schedule_time(test_bd_event3)
# test_rogue_schedules = get_rogue_schedules_in_line(FULL_SCHEDULE[1000:1100], CCL, test_datetime3, test_loc_id3)
# print(test_rogue_schedules[2])

# Expected Output #
# (('TRAIN 1-11',), (True, ('CC24', 'Kent Ridge'), ('CC23', 'one-north')), datetime.datetime(2017, 1, 6, 7, 9))

###########
# Task 3a #
###########

def calculate_blame_in_line(full_schedule, valid_bd_events, line, scorer):
    for t in valid_bd_events:
        time = get_schedule_time(t)
        loc_id = get_location_id_in_line(t, line)
        filtered_sched = get_rogue_schedules_in_line(full_schedule, line, time, loc_id) # train schedules nearby and during the breakdown event 
        
        blamed_train_code = ()
        for i in filtered_sched:
            if get_train_code(i)[0] not in blamed_train_code:
                blame_train(scorer, get_train_code(i)[0])
                blamed_train_code += (get_train_code(i)[0],)
    return scorer

# UNCOMMENT THE CODE BELOW WHEN YOU ARE DONE WITH TASK 3A. THIS IS NOT OPTIONAL TESTING!
calculate_blame_in_line(FULL_SCHEDULE, VALID_BD_EVENTS, CCL, SCORER)

# UNCOMMENT THE CODE BELOW TO TEST YOUR TASK 3A
print("## Task 3a ##")
print(sorted(get_blame_scores(SCORER))[7])

# Expected Answer
# ('TRAIN 0-5', 2)


###########
# Task 3b #
###########

def find_max_score(scorer):
    scores = tuple(map(lambda x : x[1], get_blame_scores(scorer)))
    return max(scores)

# UNCOMMENT THE CODE BELOW TO TEST YOUR TASK 3B
print("## Task 3b ##")
test_max_score = find_max_score(SCORER)
print(test_max_score)

# Expected answer
# 180


###########
# Task 3c #
###########

def find_rogue_train(scorer, max_score):
    for score in get_blame_scores(scorer):
        if score[1] == max_score:
            return score[0]

# UNCOMMENT THE CODE BELOW TO TEST YOUR TASK 3C
print("## Task 3c ##")
print("Rogue Train is '%s'" % find_rogue_train(SCORER, test_max_score))

# Expected Answer
# Rogue Train is 'TRAIN 0-4'
