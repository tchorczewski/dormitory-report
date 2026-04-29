import json

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def _read_data(self):
        '''Reads data from a JSON file and returns it as a Python object.
        Returns: A Python object (e.g., list or dictionary) containing the data from the JSON file. If the file is not found or an error occurs, it returns None.
        '''
        try:
            data = json.load(open(self.file_path))
            return data
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file {self.file_path} does not contain valid JSON.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _convert_data(self, data):
        '''Converts a list of dictionaries to a list of tuples for database insertion.
        Args:
            data: A list of dictionaries where each dictionary represents a record.
        Returns:  A list of tuples where each tuple contains the values from the corresponding dictionary.
        '''
        return [tuple(row.values()) for row in data]


    def _insert_rooms(self, conn, data):
        """Inserts room data into the database.
        Args:            
            conn: A psycopg2 connection object.
            data: A list of tuples containing room data (id, name).
        """
        query = """INSERT INTO rooms (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING"""
        self._insert(conn, data, query)
    
    def _insert_students(self, conn, data):
        '''Inserts student data into the database.
        Args:
            conn: A psycopg2 connection object.
            data: A list of tuples containing student data (birthday, id, name, room, sex).
        '''
        query = """INSERT INTO students (birthday, id, name, room, sex) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING"""
        self._insert(conn, data, query)

    def load_data(self, conn, data):
        '''Helper method to insert data into the database using executemany for efficiency.
        Args:
            conn: A psycopg2 connection object.
            data: A list of tuples containing the data to be inserted.
            query: The SQL query string with placeholders for the data.
        '''
        x = self._read_data()
        data = self._convert_data(x)
        if self._check_file(x) == 'students':
            self._insert_students(conn, data)
        else:
            self._insert_rooms(conn, data)
        
    def _insert(self, conn, data, query):
        try:
            with conn.cursor() as cursor:
                cursor.executemany(query, data)
                conn.commit()
        except Exception as e:
            print(f"Error occurred while inserting data: {e}")
            conn.rollback()

    def _check_file(self, data):
        """Checks the data within the file, and assigns it to the appropriate table based on the keys."""
        if 'birthday' in data[0]:
            return 'students'
        else:
            return 'rooms'
