import psycopg2
from config.data_manager import DataManager

import inspect
class Postgres:

    def __init__(self):

        data_manager: DataManager = DataManager.get_instance()
        self.host = data_manager._DataManager__postgres_info.host
        self.port = data_manager._DataManager__postgres_info.port
        self.database = data_manager._DataManager__postgres_info.database
        self.user = data_manager._DataManager__postgres_info.user
        self.password = data_manager._DataManager__postgres_info.password

    def __call__(self):
        try:
            self.connection = psycopg2.connect(
                host = self.host,
                port = self.port,
                database = self.database,
                user = self.user,
                password = self.password)
            print(f"Connected to the {self.database} database")

        except Exception as e:
            print("Error connecting to the PostgreSQL database:", str(e))

    def check_connection(self):
        if not self.connection:
            print("Not connected to the database!")
            return

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection to the PostgreSQL database closed")

    def get_table_names(self):

        self.check_connection()
        cursor = self.connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        table_names = cursor.fetchall()
        cursor.close()
        return [table[0] for table in table_names]

    def create_table(self, table_name, *columns):
        try:
            cursor = self.connection.cursor()
            schema = ''
            for column in columns:
                name, data_type = column
                schema += f"{name} {data_type}, "

            sql_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema[:-2] + ');'}"
            cursor.execute(sql_query)
            self.connection.commit()
            print(f"Table {table_name} created successfully")
            cursor.close()
        except Exception as e:
            print(f"Error creating '{table_name}' table:", str(e))


    def load_table_from_db(self, table_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name};")
            table = cursor.fetchall()
            return table
        except Exception as e:
            print(f"Error loading {table_name} from database:", str(e))
            return []

    def insert_into_table(self, table_name, columns, values):

        self.check_connection()

        placeholders = ', '.join('%s' for _ in range(len(values)))
        column_names = ', '.join(column for column in columns)
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders});"

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print("Project inserted successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            print(f"Ошибка при выполнении запроса: {error}")
        finally:
            cursor.close()
