import pytest
from models.segment_manager import SegmentManager
from models.segment_data import SegmentData

def create_segment_data(transcript, curr_index):
    segment_data = SegmentData()
    segment_data.curr_index = curr_index
    return segment_data

def test_no_overlap():
    transcript = [
        [0.0, 1.0, 'KAY', 'ENG', 'one'],
        [2.0, 3.0, 'KAY', 'SPA', 'two'],
        [3.5, 4.0, 'VAL', 'ENG', 'three'],
        [4.5, 5.0, 'KAY', 'SPA', 'four']
    ]
    for i in range(len(transcript)):
        segment_data = create_segment_data(i, transcript)  
        segment_manager = SegmentManager(segment_data, None)
        assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == None



def test_overlap_with_same_label():
    transcript = [
        [0.0, 1.0, 'KAY', 'ENG', 'one'],
        [0.5, 2.0, 'KAY', 'SPA', 'two'],
        [2.5, 3.5, 'VAL', 'ENG', 'three'],
        [3.5, 4.0, 'KAY', 'SPA', 'four']
    ]
    for i in range(len(transcript)):
        segment_data = create_segment_data(i, transcript)
        segment_manager = SegmentManager(segment_data, None)
        if i != 1:
            assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == None
        else:
            assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == "Line 0 overlaps line 1"


def test_overlap_with_repeating_label():
    transcript = [
        [0.0, 3.0, 'A', 'ENG', 'one'],
        [0.5, 2.0, 'B', 'SPA', 'two'],
        [2.5, 3.5, 'C', 'ENG', 'three'],
        [3.0, 4.0, 'A', 'SPA', 'four']
    ]
    for i in range(len(transcript)):
        segment_data = create_segment_data(i, transcript)
        segment_manager = SegmentManager(segment_data, None)
        if i != 3:
            assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == None
        else:
            assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == "Line 0 overlaps line 3"


def test_adjacent_segments_with_same_label():
    transcript = [
        [0.0, 1.0, 'A', 'ENG', 'one'],
        [0.0, 1.0, 'A', 'SPA', 'two'],
        [2.0, 3.0, 'B', 'ENG', 'three'],
        [3.0, 4.0, 'C', 'SPA', 'four']
    ]
    for i in range(len(transcript)):
        segment_data = create_segment_data(i, transcript)
        segment_manager = SegmentManager(segment_data, None)
        if i == 1:
            assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == "Line 0 overlaps line 1"
        else:
            assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == None


def test_label_fully_encompassing_another():
    transcript = [
        [0.0, 3.0, 'A', 'ENG', 'one'],
        [1.0, 2.0, 'A', 'SPA', 'two'], 
        [3.5, 4.5, 'C', 'ENG', 'three'],
        [4.5, 5.0, 'A', 'SPA', 'four']
    ]
    for i in range(len(transcript)):
        segment_data = create_segment_data(i, transcript)
        segment_manager = SegmentManager(segment_data, None)
        if i != 1:
            assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == None
        else:
            assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == "Line 0 overlaps line 1"


def test_speaker_a_encompassing_speaker_b_c_b_with_overlap():
    transcript = [
        [0.0, 5.0, 'A', 'ENG', 'one'], 
        [1.0, 2.0, 'B', 'SPA', 'two'],
        [2.0, 3.0, 'C', 'ENG', 'three'],
        [1.5, 3.5, 'B', 'SPA', 'four'], 
        [5.5, 6.0, 'A', 'SPA', 'five']
    ]
    for i in range(len(transcript)):
        segment_data = create_segment_data(i, transcript)
        segment_manager = SegmentManager(segment_data, None)

        if i == 3:
            assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == "Line 1 overlaps line 3"
        else:
            assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == None


def test_speaker_a_encompassing_speaker_b_c_b_with_overlap():
    transcript = [
        [0.0, 5.0, 'A', 'ENG', 'one'], # Encompasses the next three segments
        [1.0, 2.0, 'B', 'SPA', 'two'],
        [2.0, 3.0, 'C', 'ENG', 'three'],
        [2.5, 3.5, 'B', 'SPA', 'four'], # Overlaps with 'C'
        [5.5, 6.0, 'A', 'SPA', 'five']
    ]
    for i in range(len(transcript)):
        segment_data = create_segment_data(i, transcript)
        segment_manager = SegmentManager(segment_data, None)

        assert segment_manager.detect_overlap(curr_index=i, transcript=transcript) == None
