import calendar
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams



target_year = 2024
target_month = 9
member_list = ["REDACTED", "REDACTED", "REDACTED", "REDACTED", "REDACTED", "REDACTED"]
pitch_list = ["영덕", "보정", "상하"]

def get_date_by_day(target_day):
    return [day for day, weekday in calendar.Calendar().itermonthdays2(target_year, target_month) if
            weekday == target_day and day != 0]

mondays = get_date_by_day(calendar.MONDAY)
thursdays = get_date_by_day(calendar.THURSDAY)
sundays = get_date_by_day(calendar.SUNDAY)

all_days = mondays + thursdays + sundays

def set_pitch(days, pitches):
    day_with_pitch = []
    for pitch in pitches:
        for day in days:
            day_with_pitch.append((day, pitch))
    return day_with_pitch

monday_pitch = set_pitch(mondays, [pitch_list[0]])
thursday_pitch = set_pitch(thursdays, [pitch_list[1]])
sunday_pitch = set_pitch(sundays, [pitch_list[1], pitch_list[2]])

all_days_with_pitch = monday_pitch + thursday_pitch + sunday_pitch

k_day = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

def get_unassigned_pitch(day_with_pitch, day_pitch_member):
    return sorted(list(set(day_with_pitch) - {(day, pitch) for day, pitch, _ in day_pitch_member}),
        key=lambda x: (k_day[calendar.weekday(target_year, target_month, x[0])], x[0]))

assignments = {member: [0, 0, 0] for member in member_list}

def distributor():
    schedule = []

    # 첫 번째 분배
    for day, pitch in all_days_with_pitch:
        for member in member_list:
            if sum(assignments[member]) < 3:
                pitch_index = pitch_list.index(pitch)
                assignments[member][pitch_index] += 1
                schedule.append((day, pitch, member))
                break

    first_total_assignments = {member: sum(counts) for member, counts in assignments.items()}

    # 두 번째 분배
    if len(all_days_with_pitch) > len(schedule):
        unassigned_pitch = get_unassigned_pitch(all_days_with_pitch, schedule)

        if len(unassigned_pitch) % len(member_list) == 0:
            max_assignments = len(unassigned_pitch) // len(member_list)
        else:
            max_assignments = len(unassigned_pitch) // len(member_list) + 1

        for day, pitch in unassigned_pitch:
            for member in member_list:
                if sum(assignments[member]) - first_total_assignments[member] < max_assignments:
                    pitch_index = pitch_list.index(pitch)

                    already_scheduled = any(
                        scheduled_day == day and scheduled_member == member for scheduled_day, _, scheduled_member in
                        schedule)

                    if assignments[member][pitch_index] < 3 and not already_scheduled:
                        schedule.append((day, pitch, member))
                        assignments[member][pitch_index] += 1
                        break

    # 출력
    if len(get_unassigned_pitch(all_days_with_pitch, schedule)) > 0:
        print(f"예약 인원이 부족합니다. {len(get_unassigned_pitch(all_days_with_pitch, schedule))}개 누락")

    print(f"{target_year}년 {target_month}월")
    print(f"월요일 {len(mondays)}일, 목요일 {len(thursdays)}일, 일요일 {len(sundays)}일")
    print(f"총 {len(all_days)}일, {len(all_days_with_pitch)}개 예약 필요\n")

    for date, pitch, member in schedule:
        day = calendar.weekday(target_year, target_month, date)
        print(f"{date:02d}일 | {k_day[day]} | {pitch} | {member}")

    print("\n"+", ".join(f"{name}: {sum(count)}개" for name, count in assignments.items()))

    return schedule


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


weekday_times = {
    "Sunday": "10:00-12:00",
    "Monday": "20:00-22:00",
    "Tuesday": "20:00-22:00",
    "Wednesday": "20:00-22:00",
    "Thursday": "20:00-22:00",
    "Friday": "20:00-22:00",
    "Saturday": "12:00-14:00"
}

# schedule = distributor()
schedule = reservations = [
    (2, '영덕', 'REDACTED'),
    (16, '영덕', 'REDACTED'),
    (29, '상하', 'REDACTED'),
    (22, '보정', 'REDACTED'),
    (29, '보정', 'REDACTED'),
    (1, '상하', 'REDACTED'),
    (12, '보정', 'REDACTED'),
    (19, '보정', 'REDACTED'),
    (5, '보정', 'REDACTED'),
    (9, '영덕', 'REDACTED'),
    (30, '영덕', 'REDACTED'),
    (8, '상하', 'REDACTED'),
    (15, '상하', 'REDACTED'),
    (22, '상하', 'REDACTED'),
    (1, '보정', 'REDACTED'),
    (15, '보정', 'REDACTED'),
    (9, '죽전', '조용신')
]

data = {
    "date": [f"{target_year}-{target_month:02d}-{day:02d}" for day, _, _ in schedule],
    "day": [calendar.day_name[calendar.weekday(target_year, target_month, day)] for day, _, _ in schedule],
    "stadium": [pitch for _, pitch, _ in schedule],
    "booked_by": [member for _, _, member in schedule]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

plot_calendar(df, target_year, target_month, weekday_times)