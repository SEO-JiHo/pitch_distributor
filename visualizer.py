import calendar
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib import rcParams
from config import WEEKDAY_TIMES


rcParams['font.family'] = 'NanumBarunGothic'


def plot_calendar(df, year, month):
    cal = calendar.Calendar(firstweekday=6).monthdayscalendar(year, month)

    fig, ax = plt.subplots(figsize=(12, 8))

    for week_idx, week in enumerate(cal):
        for day_idx, day in enumerate(week):
            if day != 0:
                weekday = calendar.day_name[(day_idx + 6) % 7]
                matches = df[df['date'] == pd.Timestamp(f"{year}-{month:02d}-{day:02d}")]

                if weekday == 'Saturday':
                    color = 'blue'
                elif weekday == 'Sunday':
                    color = 'red'
                else:
                    color = 'black'

                if not matches.empty:
                    # for idx, row in matches.iterrows():
                    #     if pd.notna(row.get('time')):
                    #         specific_time = row['time']
                    #         event_lines = [f"{row['stadium']} ({row['booked_by']}) \n{specific_time}"]

                    event_lines = [f"{row['stadium']} ({row['booked_by']})" for idx, row in matches.iterrows()]
                    event_info = "\n".join(event_lines)

                    event_time_str = WEEKDAY_TIMES.get(weekday, "")

                    ax.text(day_idx, -week_idx + 0.3, f"{day}", ha='center', va='center', color=color, fontweight='bold', fontsize=12)
                    ax.text(day_idx, -week_idx + 0.15, event_time_str, ha='center', va='center', color='black', fontsize=10)

                    ax.text(day_idx, -week_idx - 0.1, event_info, ha='center', va='center', color='black', fontsize=13)

                    for _, row in matches.iterrows():
                        if pd.notna(row.get('time')):
                            specific_time = row['time']
                            ax.text(day_idx, -week_idx - 0.4, f"({specific_time})", ha='center', va='center', color='black', fontsize=10)

                else:
                    if weekday not in ['Sunday', 'Saturday']:
                        color = 'grey'

                    ax.text(day_idx, -week_idx + 0.3, f"{day}", ha='center', va='center', color=color, fontweight='light', fontsize=11)

                ax.add_patch(Rectangle((day_idx - 0.5, -week_idx - 0.5), 1, 1, fill=False, edgecolor='black'))


    ax.xaxis.set_ticks_position('top')
    ax.set_xticks(range(7))
    ax.set_xticklabels(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], fontsize=12)

    ax.set_yticks(range(-len(cal), 0))
    ax.set_yticklabels([])

    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-len(cal) + 0.5, 0.5)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.tight_layout()

    plt.show()