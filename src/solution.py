## Student Name: Artin Kiany
## Student ID:  219457969
 

# New requirement lab 6
"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

def to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m

def to_time_str(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.
    """

    # NEW: Weekend restriction
    if day in {"Sat", "Sun"}:
        return []

    WORK_START = 9 * 60      # 09:00
    WORK_END = 17 * 60       # 17:00
    LUNCH_START = 12 * 60    # 12:00
    LUNCH_END = 13 * 60      # 13:00
    STEP = 15                # 15-minute granularity
    BUFFER = 15              # mandatory gap after events
    FRIDAY_CUTOFF = 15 * 60  # 15:00

    # Convert events to minutes and ignore ones fully outside work hours
    event_ranges = []
    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"])
        if end <= WORK_START or start >= WORK_END:
            continue
        event_ranges.append((start, end + BUFFER))

    valid_slots = []

    for start in range(WORK_START, WORK_END, STEP):
        end = start + meeting_duration

        # Must fully fit within working hours
        if end > WORK_END:
            continue

        # Friday-specific restriction
        if day == "Fri" and start > FRIDAY_CUTOFF:
            continue

        # Cannot start during lunch break
        if LUNCH_START <= start < LUNCH_END:
            continue

        # Check conflicts (including buffer)
        conflict = False
        for ev_start, ev_end in event_ranges:
            if start < ev_end and end > ev_start:
                conflict = True
                break

        if not conflict:
            valid_slots.append(to_time_str(start))

    return valid_slots
