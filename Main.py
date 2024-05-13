import sys
from PySide2.QtWidgets import QApplication
from GUI import GUI
from api_manager import APIManager

def main():
    app = QApplication(sys.argv)

    # Fetch the API key securely, this is a placeholder for wherever you might securely store or retrieve it.
    api_key = 'caf6429d5d94023d5089fb656817efad'  # Consider fetching this from an environment variable or a secure store for production

    try:
        # Initialize the API Manager with your secure API key
        api_manager = APIManager(api_key)

        # Create and display the GUI, passing the API manager for API interactions
        window = GUI(api_manager)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Failed to start the application due to: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
