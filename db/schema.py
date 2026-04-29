class SchemaManager:
    def __init__(self, conn):
        self.conn = conn

    def create_tables(self):
        '''Creates the necessary tables (rooms and students) in the database if they do not already exist.'''
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rooms (
                        id INT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL
                    );
                """)
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS students (
                            id INT PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            birthday TIMESTAMP,
                            sex CHAR(1) NOT NULL,
                            room INT NOT NULL,
                            FOREIGN KEY (room) REFERENCES rooms(id));
                            """)
                self.conn.commit()
        except Exception as e:
            print(f"Error occurred while creating tables: {e}")
            self.conn.rollback()

    def create_indexes(self):
        """Creates indexes on the students table to optimize query performance for the reports."""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("Create INDEX IF NOT EXISTS idx_students_room ON students(room);")
                cursor.execute("Create INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);")
                self.conn.commit()
        except Exception as e:
            print(f"Error occurred while creating indexes: {e}")
            self.conn.rollback()