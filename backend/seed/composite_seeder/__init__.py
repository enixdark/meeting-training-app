from abc import abstractmethod, ABC

from seed.seeder import Seeder
from src.database import DBConnector


class SeederComposite(ABC):
    def __init__(self, db: DBConnector):
        self.__db = db
        self.__seeder_types = self._create_seeder_list()

    def run(self):
        session = self.__db.get_session()
        for seeder_type in self.__seeder_types:
            if isinstance(seeder_type, type(Seeder)):
                db_seeder = seeder_type(session)
                db_seeder.run()
        session.close()

    def append_seeder(self, seeder_type: type(Seeder)):
        self.__seeder_types.append(seeder_type)

    @abstractmethod
    def _create_seeder_list(self) -> list:
        pass
