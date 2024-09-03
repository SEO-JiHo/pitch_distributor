import calendar
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams['font.family'] = 'NanumBarunGothic'

def plot_calendar(df, year, month, weekday_times):
    cal = calendar.Calendar(firstweekday=6).monthdayscalendar(year, month)

    fig, ax = plt.subplots(figsize=(12, 8))

    for week_idx, week in enumerate(cal):
        for day_idx, day in enumerate(week):
            if day != 0:
                weekday = calendar.day_name[(day_idx + 6) % 7]
                matches = df[df['date'] == pd.Timestamp(f"{year}-{month:02d}-{day:02d}")]

                if not matches.empty:
                    event_time = weekday_times.get(weekday, "")
                    event_lines = [f"{row['stadium']} ({row['booked_by']})" for idx, row in matches.iterrows()]
                    event_info = "\n".join(event_lines)
                    color = "black"
                else:
                    event_time = ""
                    event_info = ""
                    color = "grey"

                ax.text(day_idx, -week_idx + 0.3, f"{day}", ha='center', va='center', color=color, fontweight='bold', fontsize=12)

                if event_time:
                    ax.text(day_idx, -week_idx + 0.1, event_time, ha='center', va='center', color=color, fontsize=10)

                if event_info:
                    ax.text(day_idx, -week_idx - 0.2, event_info, ha='center', va='center', color=color, fontsize=13)

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