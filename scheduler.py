import calendar
import pandas as pd
from numpy.ma.core import minimum

from config import *



def get_date_by_day(target_day):
    return [day for day, weekday in calendar.Calendar().itermonthdays2(TARGET_YEAR, TARGET_MONTH) if
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

def set_biweekly_pitch(days, pitch1, pitch2):
    day_with_pitch = []
    for i, day in enumerate(days):
        pitch = pitch1 if i % 2 == 0 else pitch2
        day_with_pitch.append((day, pitch))
    return day_with_pitch

monday_pitch = set_pitch(mondays, [PITCH_LIST[0]])
thursday_pitch = set_pitch(thursdays, [PITCH_LIST[1]])
sunday_pitch = set_biweekly_pitch(sundays, PITCH_LIST[1], PITCH_LIST[2])

all_days_with_pitch = monday_pitch + thursday_pitch + sunday_pitch

print(all_days_with_pitch)

k_day = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

def get_unassigned_pitch(day_with_pitch, day_pitch_member):
    return sorted(list(set(day_with_pitch) - {(day, pitch) for day, pitch, _, _ in day_pitch_member}),
        key=lambda x: (k_day[calendar.weekday(TARGET_YEAR, TARGET_MONTH, x[0])], x[0]))

assignments = {member: [0, 0, 0] for member in MEMBER_LIST}

def distributor():
    schedule = []

    # 첫 번째 분배
    for day, pitch in all_days_with_pitch:
        for member in MEMBER_LIST:
            minimum_num = len(all_days) // len(MEMBER_LIST)

            if minimum_num > 3:
                raise ValueError("예약 인원이 부족합니다.")

            if sum(assignments[member]) < minimum_num:
                pitch_index = PITCH_LIST.index(pitch)
                assignments[member][pitch_index] += 1
                schedule.append((day, pitch, member, None))
                break

    first_total_assignments = {member: sum(counts) for member, counts in assignments.items()}

    # 두 번째 분배
    if len(all_days_with_pitch) > len(schedule):
        unassigned_pitch = get_unassigned_pitch(all_days_with_pitch, schedule)

        if len(unassigned_pitch) % len(MEMBER_LIST) == 0:
            max_assignments = len(unassigned_pitch) // len(MEMBER_LIST)
        else:
            max_assignments = len(unassigned_pitch) // len(MEMBER_LIST) + 1

        for day, pitch in unassigned_pitch:
            for member in MEMBER_LIST:
                if sum(assignments[member]) - first_total_assignments[member] < max_assignments:
                    pitch_index = PITCH_LIST.index(pitch)

                    already_scheduled = any(
                        scheduled_day == day and scheduled_member == member for scheduled_day, _, scheduled_member, _ in schedule)

                    if assignments[member][pitch_index] < 3 and not already_scheduled:
                        schedule.append((day, pitch, member, None))
                        assignments[member][pitch_index] += 1
                        break

    #출력
    if len(get_unassigned_pitch(all_days_with_pitch, schedule)) > 0:
        raise ValueError(f"예약 인원이 부족합니다. {len(get_unassigned_pitch(all_days_with_pitch, schedule))}개 누락")

    print(f"{TARGET_YEAR}년 {TARGET_MONTH}월")
    print(f"월요일 {len(mondays)}일, 목요일 {len(thursdays)}일, 일요일 {len(sundays)}일")
    print(f"총 {len(all_days)}일, {len(all_days_with_pitch)}개 예약 필요\n")

    for date, pitch, member, _ in schedule:
        day = calendar.weekday(TARGET_YEAR, TARGET_MONTH, date)
        print(f"{date:02d}일 | {k_day[day]} | {pitch} | {member}")

    print("\n"+", ".join(f"{name}: {sum(count)}개" for name, count in assignments.items()))

    return schedule

