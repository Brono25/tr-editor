from session_manager import SessionManager

def test_trim_types():
    session_manager = SessionManager([])
    trim_times = [
        ([1, 5, 1, 5], "delete"),
        ([0, 5, 1, 5], "delete"),
        ([1, 6, 1, 5], "delete"),
        ([0, 6, 1, 5], "delete"),
        ([2, 4, 1, 5], "trim_middle"),
        ([0, 4, 1, 5], "trim_start"),
        ([1, 3, 1, 5], "trim_start"),
        ([0, 1, 1, 5], None),
        ([2, 6, 1, 5], "trim_end"),
        ([2, 5, 1, 5], "trim_end"),
        ([5, 6, 1, 5], None),
        ([6, 8, 1, 5], None),
        ([0, 0.5, 1, 5], None),
        ([0, 1, 1, 5], None),
        ([5, 6, 1, 5], None),
    ]

    for input, answer in trim_times:
        result = session_manager._trim_type(*input)
        assert result == answer, f"Expected {answer} but got {result}"
