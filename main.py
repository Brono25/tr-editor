
from session_io import SessionIO
from session_manager import SessionManager
from session_data import SessionData
def main():
    
    session_data = SessionData()
    io = SessionIO(session_data)
    manager = SessionManager(session_data, io)
    manager.view.run()

if __name__ == "__main__":
    main()
