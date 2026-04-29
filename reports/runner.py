class ReportRunner:
    def __init__(self, conn, extension='json'):
        self.conn = conn
        self.extension = extension

    def _run_report(self,query):
        '''Helper method to run a report query and return results'''
        from psycopg2.extras import RealDictCursor
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error occurred while running report: {e}")
            return []

    def mixed_gender(self):
        '''Helper method to run the mixed gender report query and return results'''
        query = """
            SELECT r.id, r.name
            FROM rooms r
            INNER JOIN students s on r.id=s.room
            GROUP BY r.id
            HAVING COUNT(DISTINCT s.sex) >1;"""
        return self._run_report(query)
    
    def headcount(self):
        '''Helper method to run the headcount report query and return results'''
        query = """
            SELECT r.id, r.name, COUNT(s.name) as headcount
            FROM rooms r
            LEFT JOIN students s on r.id=s.room
            GROUP BY r.id;"""
        return self._run_report(query)
    
    def lowest_avg_age(self):
        '''Helper method to run the lowest average age report query and return results'''
        query = """WITH students_with_age as 
        (Select id, room, name, sex, EXTRACT(YEAR FROM AGE(birthday)) as age 
        FROM STUDENTS)
        SELECT r.id, r.name, AVG(swa.age)::float as avg_age 
        FROM rooms r 
        LEFT JOIN students_with_age swa on r.id = swa.room 
        GROUP BY r.id 
        ORDER BY avg_age ASC 
        LIMIT 5;"""
        return self._run_report(query)
    
    def age_difference(self):
        '''Helper method to run the age difference report query and return results'''
        query = """WITH students_with_age as 
        (Select id, room, name, sex, EXTRACT(YEAR FROM AGE(birthday)) as age 
        FROM STUDENTS)
        SELECT r.id, r.name, (MAX(swa.age) - MIN(swa.age))::float as age_diff 
        FROM rooms r 
        LEFT JOIN students_with_age swa on r.id = swa.room
        GROUP BY r.id 
        ORDER BY age_diff DESC 
        LIMIT 5;"""
        return self._run_report(query)
    
    def perform_analysis(self):
        '''Performs all the report analyses and exports the results with the specified file format (JSON/XML) using the Formatter class'''
        return self._export_report({
            "mixed_gender": self.mixed_gender(),
            "headcount": self.headcount(),
            "lowest_avg_age": self.lowest_avg_age(),
            "age_difference": self.age_difference()
        }, self.extension)


    def _export_report(self, report_data, extension):
        '''Helper method to export the report data in the specified format (JSON/XML) using the Formatter class'''
        from output.formatter import Formatter
        Formatter(report_data, extension).export()