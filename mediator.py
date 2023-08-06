
from tk_gui import TkGui
from session import Session

class Mediator:
    def __init__(self):
        self.gui = TkGui()
        self.session = Session()
        self.gui.run()