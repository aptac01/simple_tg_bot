from sqlalchemy import create_engine


class Database:

    sqlalchemy_engine = None

    def __init__(self, addr, passw, db_port='3050'):
        self.user    = 'tg_bot'
        self.addr    = addr
        self.passw   = passw
        self.db_port = db_port

    def init_engine(self):
        uri = f'firebird+fdb://{self.user}:{self.passw}@{self.addr}:{self.db_port}/simple_tg_bot?'\
              + 'role=ROLE_ADMIN&'\
              + 'charset=UTF8'

        try:
            self.sqlalchemy_engine = create_engine(uri)
            self.sqlalchemy_engine.connect()
            self.sqlalchemy_engine.begin(
                '[isc_tpb_version3,isc_tpb_write,isc_tpb_nowait,isc_tpb_read_committed,isc_tpb_rec_version]'
            )
        except Exception as e:
            raise Exception('Не удалось установить соединение с базой данных: ' + repr(e))

    def connection(self):

        return self.sqlalchemy_engine

    def close_connection(self):

        self.sqlalchemy_engine.dispose()
