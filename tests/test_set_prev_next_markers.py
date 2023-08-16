import pytest
from controllers.window_model import WindowManager
from models.window_data import WindowData


def test_set_prev_next_markers_empty_transcript():
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(0, [])
    assert wm.window_data.prev_marker is None
    assert wm.window_data.next_marker is None


def test_set_prev_next_markers_no_matching_labels():
    transcript = [(0, 1, "A", "", ""), (2, 3, "B", "", "")]
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(0, transcript)
    assert wm.window_data.prev_marker is None
    assert wm.window_data.next_marker is None


def test_set_prev_next_markers_matching_labels():
    transcript = [(0, 1, "A", "", ""), (2, 3, "A", "", ""), (4, 5, "B", "", "")]
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(1, transcript)
    assert wm.window_data.prev_marker == 1
    assert wm.window_data.next_marker is None


def test_set_prev_next_markers_with_multiple_matching_labels():
    transcript = [
        (0, 1, "A", "", ""),
        (1, 2, "A", "", ""),
        (2, 3, "B", "", ""),
        (3, 4, "A", "", ""),
    ]
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(1, transcript)
    assert wm.window_data.prev_marker == 1
    assert wm.window_data.next_marker == 3


def test_set_prev_next_markers_with_multiple_matching_labels_2():
    transcript = [
        (0, 1, "A", "", ""),
        (1, 2, "A", "", ""),
        (2, 3, "B", "", ""),
        (3, 4, "A", "", ""),
    ]
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(3, transcript)
    assert wm.window_data.prev_marker == 2
    assert wm.window_data.next_marker == None


def test_set_prev_next_markers_with_no_next_label_match():
    transcript = [(0, 1, "A", "", ""), (1, 2, "B", "", ""), (2, 3, "B", "", "")]
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(0, transcript)
    assert wm.window_data.prev_marker is None
    assert wm.window_data.next_marker is None


def test_set_prev_next_markers_with_prev_label_match_but_no_next_match():
    transcript = [(0, 1, "B", "", ""), (1, 2, "A", "", ""), (2, 3, "A", "", "")]
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(2, transcript)
    assert wm.window_data.prev_marker == 2
    assert wm.window_data.next_marker is None


def test_set_prev_next_markers_with_all_same_labels():
    transcript = [(0, 1, "A", "", ""), (1, 2, "A", "", ""), (2, 3, "A", "", "")]
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(1, transcript)
    assert wm.window_data.prev_marker == 1
    assert wm.window_data.next_marker == 2


def test_set_prev_next_markers_with_overlap_in_prev_match():
    transcript = [
        (0, 1, "A", "", ""),
        (1, 4, "A", "", ""),
        (2, 3, "B", "", ""),
        (3, 4, "A", "", ""),
    ]
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(3, transcript)
    assert wm.window_data.prev_marker == 4
    assert wm.window_data.next_marker == None


def test_set_prev_next_markers_with_overlap_in_next_match():
    transcript = [
        (0, 1, "A", "", ""),
        (1, 4, "A", "", ""),
        (2, 3, "B", "", ""),
        (3, 4, "A", "", ""),
    ]
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(1, transcript)
    assert wm.window_data.prev_marker == 1
    assert wm.window_data.next_marker == 3


def test_set_prev_next_markers_with_double_overlap():
    transcript = [
        (0, 9, "A", "", ""),
        (0, 10, "A", "", ""),
        (2, 3, "B", "", ""),
        (3, 4, "A", "", ""),
    ]
    data = WindowData()
    wm = WindowManager(data)
    wm.set_prev_next_markers(3, transcript)
    assert wm.window_data.prev_marker == 10
    assert wm.window_data.next_marker == None
