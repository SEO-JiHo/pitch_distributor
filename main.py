from scheduler import distributor
from visualizer import plot_calendar
from config import *
import calendar
import pandas as pd


#1
# distributed_list = distributor()

#2
distributed_list = final_schedule

data = {
    "date": [f"{TARGET_YEAR}-{TARGET_MONTH:02d}-{day:02d}" for day, _, _, _ in distributed_list],
    "day": [calendar.day_name[calendar.weekday(TARGET_YEAR, TARGET_MONTH, day)] for day, _, _, _ in distributed_list],
    "stadium": [pitch for _, pitch, _, _ in distributed_list],
    "booked_by": [member for _, _, member, _ in distributed_list],
    "time": [time if time is not None else None for _, _, _, time in distributed_list]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

plot_calendar(df, TARGET_YEAR, TARGET_MONTH)