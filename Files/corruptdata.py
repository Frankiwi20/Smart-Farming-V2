class DataCorrupter:
    def __init__(self, filename):
        self.filename = filename

    def corrupt_data(self):
        """
        Simulate an attack by corrupting the data in the file.
        This method replaces all characters in the file with asterisks.
        """
        try:
            # Open the file to read its contents
            with open(self.filename, 'r') as file:
                data = file.read()

            # Replace all characters in the data with asterisks
            corrupted_data = '*' * len(data)

            # Write the corrupted data back to the file
            with open(self.filename, 'w') as file:
                file.write(corrupted_data)

            print("Data has been corrupted successfully.")

        except Exception as e:
            print(f"Failed to corrupt data: {e}")

# Example usage:
# corrupter = DataCorrupter('polygon_data.txt')
# corrupter.corrupt_data()
