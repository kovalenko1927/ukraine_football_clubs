from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def db_connect():
    return create_engine('sqlite:///football_clubs.db')


def create_table(engine):
    Base.metadata.create_all(engine)


class FootballClubsData(Base):
    __tablename__ = "football_clubs"

    clubs_id = Column('club_id', Integer, primary_key=True)
    club_name = Column('club_name', Text())
    league_name = Column('league_name', Text())
    logo_link = Column('logo_link', Text())
    web_site_link = Column('web_site_link', Text())


class PlayersData(Base):
    __tablename__ = "players"

    player_id = Column('player_id', Integer, primary_key=True)
    name = Column('name', Text())
    club = Column('club', Text())
    position = Column('position', Text())
    birthday = Column('birthday', Text(), nullable=True)
    motherland = Column('motherland', Text())
    photo_link = Column('photo_link', Text(), nullable=True)





