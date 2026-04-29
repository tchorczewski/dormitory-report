from db import connection, loader, schema
from os import getenv
from dotenv import load_dotenv
import argparse
from reports import runner
load_dotenv()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run reports on the dormitory database.')
    parser.add_argument('--rooms', help='Load rooms data from JSON file', required=True)
    parser.add_argument('--students', help='Load students data from JSON file', required=True)
    parser.add_argument('--extension', help='Specify the output format for reports (json or xml)', default='json')
    args = parser.parse_args()

    conn = connection.Connector(
        host=getenv("host"),
        dbname=getenv("dbname"),
        user=getenv("user"),
        password=getenv("password")
    ).connect()

    if conn:
        schema.SchemaManager(conn).create_tables()

        loader.DataLoader(args.rooms).load_data(conn, args.rooms)
        loader.DataLoader(args.students).load_data(conn, args.students)

        report_runner = runner.ReportRunner(conn, args.extension)
        report_runner.perform_analysis()

