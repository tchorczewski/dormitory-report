class SchemaManager:
    def __init__(self, conn):
        self.conn = conn

    def create_tables(self):
        '''Creates the necessary tables (rooms and students) in the database if they do not already exist.'''
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
            