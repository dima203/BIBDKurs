import sqlite3


class DataBase:
    __instance = None

    def __new__(cls, *args, **kwargs) -> 'DataBase':
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, debug=False) -> None:
        if debug:
            self.__connection = sqlite3.connect(':memory:')
            original_base = sqlite3.connect('./database.db')
            original_base.backup(self.__connection)
            original_base.close()
        else:
            self.__connection = sqlite3.connect('./database.db', 10)
        self.__cursor = self.__connection.cursor()

    def get_records_from_table(self, table_name: str) -> list[tuple]:
        return self.__cursor.execute(f'''
            SELECT * FROM "{table_name}"
        ''').fetchall()

    def get_record(self, table_name: str, id_name: str, record_id: str) -> list:
        record = self.__cursor.execute(f'''
            SELECT * FROM "{table_name}"
            WHERE {id_name} = '{record_id}'
        ''').fetchall()

        if record is None or not record:
            raise KeyError(f'Key {record_id} is not in "{table_name}"')

        return record

    def update_record(self, table_name: str, id_name: str, record_id: str, record_data: dict) -> None:
        set_string = ''
        for key, value in record_data.items():
            if isinstance(value, str):
                set_string += f"{key} = '{value}', "
            else:
                set_string += f"{key} = {value}, "
        self.__cursor.execute(f'''
            UPDATE "{table_name}" SET {set_string[:-2]}
            WHERE {id_name} = '{record_id}'
        ''')

    def add_record(self, table_name: str, record_data: dict) -> None:
        self.__cursor.execute(f'''
            INSERT INTO "{table_name}" {tuple(record_data.keys())}
            VALUES ({", ".join(['?'] * len(record_data))})
        ''', tuple(record_data.values()))

    def delete_record(self, table_name: str, id_name: str, record_id: str) -> None:
        self.__cursor.execute(f'''
            DELETE FROM "{table_name}"
            WHERE {id_name} = '{record_id}'
        ''')

    def commit(self) -> None:
        self.__connection.commit()

    def backup(self, path: str) -> None:
        backup_connection = sqlite3.connect(path)
        self.__connection.backup(backup_connection)
        backup_connection.close()

    def restore(self, path: str) -> None:
        restore_connection = sqlite3.connect(path)
        restore_connection.backup(self.__connection)
        restore_connection.close()

    def __del__(self) -> None:
        self.__cursor.close()
        self.__connection.close()
