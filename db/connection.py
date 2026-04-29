import psycopg2
class Connector:
    def __init__(self, host, dbname, user, password):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
    
    def connect(self):
        '''Establishes a connection to the PostgreSQL database using the provided credentials.
        Returns: A psycopg2 connection object if the connection is successful, or None if an error occurs.
        '''
        try:
            conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            return conn
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def __enter__(self):
        '''Enables the use of the Connector class as a context manager, allowing for automatic connection management (opening and closing connections).'''
        self.conn = self.connect()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Closes the database connection when exiting the context manager block.'''
        if self.conn:
            self.conn.close()
    
    
