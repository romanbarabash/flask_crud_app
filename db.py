from sqlalchemy import Table, Column, String, Integer, MetaData


class Database:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def get_db_structure(self, table_name: str, meta: MetaData):
        return Table(table_name, meta,
                     Column('book_id', Integer),
                     Column('title', String))
