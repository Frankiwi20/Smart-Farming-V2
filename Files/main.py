import sys
from PySide2.QtWidgets import QApplication
from GUI import GUI
from api_manager import APIManager

def main():
    app = QApplication(sys.argv)

    # Fetch the API key securely, this is a placeholder for wherever you might securely store or retrieve it.
    api_key = ''  # add your api key here 

    try:
        # Initialize the API Manager with your secure API key
        api_manager = APIManager(api_key)

        # Create and display the GUI, passing the API manager for API interactions
        window = GUI(api_manager)
        window.show()
        sys.exit(app.exec_())
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        sys.exit(1)
    except ImportError as e:
        print(f"Import error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to start the application due to an unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
