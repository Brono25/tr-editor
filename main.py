
from session_data import SessionData
from tr_editor_gui import TrEditorGui
from session_manager import SessionManager

def main():
    # Instantiate the Model
    session = SessionData()
    
    # Instantiate the Controller, passing the Model to it
    manager = SessionManager(session)
    
    # Start the main loop of the GUI
    manager.view.run()

if __name__ == "__main__":
    main()
