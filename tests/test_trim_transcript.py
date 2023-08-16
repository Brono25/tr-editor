import pytest
from controllers.session_model import SessionManager


def run_test(trim_start, trim_end, transcript, expected_result):
    session_manager = SessionManager([], None)
    trimmed = session_manager.trim_transcript(trim_start, trim_end, transcript)

    assert trimmed == expected_result, (
        "Expected:\n"
        + "\n".join(map(str, expected_result))
        + "\n\nGot:\n"
        + "\n".join(map(str, trimmed))
    )


def test_trim_whole_segment():
    transcript = [[1, 2, "BBB", "ENG", "two"]]
    expected_result = []
    run_test(0, 3, transcript, expected_result)


def test_trim_whole_segment_on_start_bound():
    transcript = [[1, 2, "BBB", "ENG", "two"]]
    expected_result = []
    run_test(1, 3, transcript, expected_result)


def test_trim_whole_segment_on_end_bound():
    transcript = [[1, 2, "BBB", "ENG", "two"]]
    expected_result = []
    run_test(0, 2, transcript, expected_result)


def test_trim_whole_segment_on_both_bounds():
    transcript = [[1, 2, "BBB", "ENG", "two"]]
    expected_result = []
    run_test(1, 2, transcript, expected_result)


def test_trim_from_start():
    transcript = [[1, 4, "BBB", "ENG", "two"]]
    expected_result = [[0, 2, "BBB", "ENG", "two"]]
    run_test(0, 2, transcript, expected_result)


def test_trim_from_start_on_start_bound():
    transcript = [[1, 4, "BBB", "ENG", "two"]]
    expected_result = [[1, 3, "BBB", "ENG", "two"]]
    run_test(1, 2, transcript, expected_result)


def test_trim_from_start_on_end_bound():
    transcript = [[1, 4, "BBB", "ENG", "two"]]
    expected_result = [[0, 3, "BBB", "ENG", "two"]]
    run_test(0, 1, transcript, expected_result)


def test_trim_from_end():
    transcript = [[1, 4, "BBB", "ENG", "two"]]
    expected_result = [[1, 3, "BBB", "ENG", "two"]]
    run_test(3, 5, transcript, expected_result)


def test_trim_from_end_on_start_bound():
    transcript = [[1, 4, "BBB", "ENG", "two"]]
    expected_result = [[1, 4, "BBB", "ENG", "two"]]
    run_test(4, 5, transcript, expected_result)


def test_trim_from_end_on_end_bound():
    transcript = [[1, 4, "BBB", "ENG", "two"]]
    expected_result = [[1, 3, "BBB", "ENG", "two"]]
    run_test(3, 4, transcript, expected_result)


def test_trim_in_middle():
    transcript = [[1, 4, "BBB", "ENG", "two"]]
    expected_result = [[1, 3, "BBB", "ENG", "two"]]
    run_test(2, 3, transcript, expected_result)


def test_invalid_trim_range():
    session_manager = SessionManager([], None)
    transcript = [[1, 4, "BBB", "ENG", "two"]]
    trim_start = 2
    trim_end = 2
    with pytest.raises(
        ValueError, match="Invalid Range: end time must be greater than start time."
    ):
        session_manager.trim_transcript(trim_start, trim_end, transcript)


def test_mix1():
    transcript = [
        [1, 3, "AAA", "ENG", "one"],
        [1, 3, "BBB", "ENG", "two"],
        [2, 5, "AAA", "ENG", "three"],
        [5, 6, "AAA", "ENG", "four"],
        [6, 8, "BBB", "ENG", "five"],
        [0, 5, "AAA", "ENG", "six"],
        [0, 10, "CCC", "ENG", "seven"],
    ]
    expected_result = [
        [1, 3, "AAA", "ENG", "three"],
        [3, 4, "AAA", "ENG", "four"],
        [4, 6, "BBB", "ENG", "five"],
        [0, 3, "AAA", "ENG", "six"],
        [0, 8, "CCC", "ENG", "seven"],
    ]
    run_test(1, 3, transcript, expected_result)


def test_mix2():
    transcript = [
        [1, 3, "AAA", "ENG", "one"],
        [1, 3, "BBB", "ENG", "two"],
        [2, 5, "AAA", "ENG", "three"],
        [5, 6, "AAA", "ENG", "four"],
        [6, 8, "BBB", "ENG", "five"],
        [0, 5, "AAA", "ENG", "six"],
        [0, 10, "CCC", "ENG", "seven"],
    ]

    expected_result = [  
        [1, 2, "AAA", "ENG", "one"],  
        [1, 2, "BBB", "ENG", "two"],  
        [2, 4, "AAA", "ENG", "three"],  
        [4, 5, "AAA", "ENG", "four"],  
        [5, 7, "BBB", "ENG", "five"],  
        [0, 4, "AAA", "ENG", "six"],  
        [0, 9, "CCC", "ENG", "seven"],  
    ]
    run_test(2, 3, transcript, expected_result)


def test_mix3():
    transcript = [
        [1, 3, "AAA", "ENG", "one"],
        [1, 3, "BBB", "ENG", "two"],
        [2, 5, "AAA", "ENG", "three"],
        [5, 6, "AAA", "ENG", "four"],
        [6, 8, "BBB", "ENG", "five"],
        [0, 5, "AAA", "ENG", "six"],
        [0, 10, "CCC", "ENG", "seven"],
    ]

    expected_result = [  

        [1, 2, "BBB", "ENG", "five"],
        [0, 1, "AAA", "ENG", "six"],  # [0, 5, "AAA", "ENG", "six"],
        [0, 4, "CCC", "ENG", "seven"],# [0, 10, "CCC", "ENG", "seven"],
    ]
    run_test(1, 7, transcript, expected_result)