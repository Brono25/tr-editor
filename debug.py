
from segment_data import Segment

class Debug:

    def __init__(self):
        pass
    
    @classmethod
    def print_session_data(cls, data, string):
        print(f"\n{string}")
        print('-' * 30)
        for attr, value in data.__dict__.items():
            if isinstance(value, (Segment)):
                print(f"{attr}:")
                for subattr, subvalue in value.__dict__.items(): 
                    print(f"    {subattr}: {subvalue}")
            elif attr == 'transcript':
                print(f"{attr}:")
                for line in value:
                    print(f"    {line}")
            else:
                print(f"{attr}: {value}")
        print('-' * 30)
