from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from football_clubs.const import Spiders

Base = declarative_base()

DB_URL = 'sqlite:///football_clubs.db'


class FootballClub(Base):
    __tablename__ = "clubs"

    club_id = Column('club_id', Integer, primary_key=True)
    club_name = Column('club_name', Text())
    league_name = Column('league_name', Text())
    logo_link = Column('logo_link', Text())
    web_site_link = Column('web_site_link', Text())


class FootballPlayer(Base):
    __tablename__ = "players"

    player_id = Column('player_id', Integer, primary_key=True)
    name = Column('name', Text())
    club = Column('club', Text())
    position = Column('position', Text())
    birthday = Column('birthday', Text(), nullable=True)
    motherland = Column('motherland', Text())
    photo_link = Column('photo_link', Text(), nullable=True)


class DBClient:
    def __init__(self, table_name):
        engine = create_engine(url=DB_URL)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.table_name = table_name

    def save_data(self, items):
        session = self.Session()
        for item in items:
            if self.table_name == Spiders.clubs.value:
                self._create_club(club=item, session=session)
            elif self.table_name == Spiders.players.value:
                self._create_player(player=item, session=session)
            else:
                raise ValueError(f"Unknown table name: {self.table_name}")

    @staticmethod
    def _create_club(club, session):
        try:
            session.add(FootballClub(**club))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def _create_player(player, session):
        try:
            session.add(FootballPlayer(**player))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
