## Student Name: Artin Kiany
## Student ID: 219457969

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.solution import suggest_slots


def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots

def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{"start": "07:00", "end": "08:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "16:00" in slots

def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00"},
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert  slots[1] == "10:15"
    assert "09:30" not in slots

def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots

def test_meeting_must_fully_fit_before_5pm():
    """
    Constraint:
    A meeting must fully fit within working hours (09:00–17:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "16:00" in slots      # 16:00–17:00 fits
    assert "16:15" not in slots  # 16:15–17:15 exceeds work hours

def test_back_to_back_event_requires_buffer():
    """
    Constraint:
    Meetings cannot start immediately after an event (15-minute buffer required).
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "11:00" not in slots
    assert "11:15" in slots

def test_event_overlapping_lunch_extends_blocking():
    """
    Constraint:
    Events overlapping lunch still enforce buffer beyond their end.
    """
    events = [{"start": "11:30", "end": "12:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:45" not in slots  # 12:30 + 15 buffer
    assert "13:00" in slots

def test_event_partially_outside_working_hours():
    """
    Constraint:
    Events partially overlapping working hours must still block availability.
    """
    events = [{"start": "08:30", "end": "09:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots
    assert "09:30" not in slots
    assert "09:45" in slots

def test_no_available_slots_returns_empty_list():
    """
    Functional requirement:
    Return an empty list when no valid meeting times exist.
    """
    events = [{"start": "09:00", "end": "17:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert slots == []

def test_slots_are_returned_in_ascending_order():
    """
    Functional requirement:
    Output must be sorted in ascending time order.
    """
    events = [
        {"start": "14:00", "end": "15:00"},
        {"start": "09:00", "end": "10:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert slots == sorted(slots)

def test_no_meetings_on_saturday():
    """
    Functional requirement:
    The system must not suggest meetings on weekends.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Sat")

    assert slots == []

def test_no_meetings_on_sunday_even_with_no_events():
    """
    Functional requirement:
    Weekend restriction applies regardless of event availability.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="Sun")

    assert slots == []

def test_friday_allows_meeting_starting_at_1500():
    """
    Edge case:
    Meetings starting exactly at 15:00 on Friday are allowed.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "15:00" in slots

def test_friday_excludes_meetings_after_1500():
    """
    Functional requirement:
    Meetings starting after 15:00 on Friday must be excluded.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "15:15" not in slots
    assert "16:00" not in slots

def test_friday_cutoff_overrides_other_constraints():
    """
    Edge case:
    Even if a slot satisfies all other constraints, it must be excluded
    if it violates the Friday cutoff.
    """
    events = [{"start": "13:00", "end": "14:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "15:15" not in slots

