from sqlalchemy import (
    create_engine, 
    text,
    MetaData,
)
from typing import Optional

class SqlAlchemy:
    def __init__(self, db_path) -> None:
        self.engine = create_engine(f'sqlite:///{db_path}')

    def get_metadata(self) -> None:
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        return metadata
    
    def execute_sql_statement(self, sql_statement: str) -> Optional[list]:
        with self.engine.connect() as conn:
            return list(conn.execute(text(sql_statement)))
        
    def get_table_columns(self, table_name: str) -> list:
        table = self.get_metadata().tables[table_name]
        return table.columns.keys()
