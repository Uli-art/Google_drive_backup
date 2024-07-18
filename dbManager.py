from sqlalchemy import create_engine, select, func, desc
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy_utils import create_database, database_exists
from models import Base, Session, Change


class DbManager:

    def __init__(self, user, password, user_id):
        self.user = user
        self.password = password
        self.user_id = user_id
        self.engine = self.create_engine()
        self.db_session_factory = sessionmaker(self.engine)

    def create_tables(self):
        with self.engine.connect() as conn:
            Base.metadata.drop_all(self.engine)
            Base.metadata.create_all(self.engine)
            conn.commit()

    def create_engine(self):
        url = f"postgresql+psycopg://{self.user}:{self.password}@localhost/{self.user_id}"
        if database_exists(url):
            self.engine = create_engine(url, echo=True)
        else:
            create_database(url)
            self.engine = create_engine(url, echo=True)
            self.create_tables()

        return self.engine

    def insert_changes(self, new_file_metadata, new_session_id, new_file_ref,
                       new_parent_id, new_name, new_is_removed, new_file_id, new_size):
        new_change = Change(file_metadata=new_file_metadata, session_id=new_session_id, file_ref=new_file_ref,
                            parent_id=new_parent_id, name=new_name, is_removed=new_is_removed,
                            file_id=new_file_id, size=new_size)
        with self.db_session_factory() as db_session:
            db_session.add(new_change)
            db_session.commit()

    def select_changes(self):
        with self.db_session_factory() as db_session:
            query = (
                select(Change)
            )
            result = db_session.execute(query).scalars().all()
            return result

    def insert_session(self, new_timestamp, new_page_token, new_backup_type):
        new_session = Session(timestamp=new_timestamp, page_token=new_page_token, backup_type=new_backup_type)
        with self.db_session_factory() as db_session:
            db_session.add(new_session)
            db_session.commit()

    def select_session(self):
        with self.db_session_factory() as db_session:
            query = (
                select(Session)
                .options(selectinload(Session.changes))
            )
            result = db_session.execute(query).scalars().all()
            return result

    def select_last_session(self):
        with self.db_session_factory() as db_session:
            query = (
                select(Session)
                .options(selectinload(Session.changes))
                .order_by(desc(Session.id))
            )
            result = db_session.execute(query).scalars().first()
            return result

    def commit_all(self):
        with self.db_session_factory() as db_session:
            db_session.commit()
    # def connect(self):
    #     try:
    #         url = f"mysql+mysqldb://{self.user}:{self.password}@localhost/tester"

    #         if not database_exists(url):
    #             create_database(url)
    #         else:
    #             print("connect")
    #             engine = create_engine(url)
    #             engine.connect()
    #     except Error as e:
    #         print(e)

# from mysql.connector import connect, Error
# from sqlalchemy import create_engine
#
#
# class DbManager:
#
#     def __init__(self, user, password, user_id):
#         self.user = user
#         self.password = password
#         self.user_id = user_id
#
#     def connect(self):
#         try:
#             with connect(
#                 host="localhost",
#                 user=self.user,
#                 password=self.password,
#             ) as connection:
#                 if not self.database_exists(connection):
#                     create_db_query = f"CREATE DATABASE {self.user_id}"
#                     with connection.cursor() as cursor:
#                         cursor.execute(create_db_query)
#                 else:
#                 url = f"mysql://{self.user}:{self.password}@localhost/{self.user_id}"
#                 engine = create_engine(url)
#                 engine.connect()
#                 connection = engine.raw_connection()
#         cursor = connection.cursor()
#         show_db_query = "SHOW DATABASES"
#
#         cursor.execute(show_db_query)
#         for db in cursor:
#             print(db)
#
# except Error as e:
#     print(e)
#
# def database_exists(self, connection):
#     show_db_query = "SHOW DATABASES"
#     with connection.cursor() as cursor:
#         cursor.execute(show_db_query)
#         for db in cursor:
#             if self.user_id == db[0]:
#                 return True
#         return False
