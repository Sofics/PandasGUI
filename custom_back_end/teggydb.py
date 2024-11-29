import datetime as dt

import sqlalchemy
from sqlalchemy import create_engine, Column, DATE, VARCHAR
from sqlalchemy.dialects.mysql import MEDIUMINT, INTEGER, SMALLINT
from sqlalchemy.orm import declarative_base, Session

import cfg

TEGGY_ENGINE = create_engine(
    f"mysql+pymysql://{cfg.TeggyDB.username}:{cfg.TeggyDB.password}@{cfg.TeggyDB.host}/{cfg.TeggyDB.name}",
    pool_recycle=3600,
    # echo=True,  # to see sql execution
)

# Describing Databases with MetaData / Declarative Mapping
Base = declarative_base()


class WaferVolume(Base):
    """Class that represents a certain user's uncommitted change to a certain view."""

    __tablename__ = "WaferVolume"
    __table_args__ = {"mysql_charset": "utf8"}

    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)  # note: corresponds to svnrepository
    date = Column(DATE, nullable=False)
    ip_name = Column(VARCHAR, nullable=False)
    ip_version = Column(VARCHAR, nullable=False)
    tapeouts = Column(SMALLINT(unsigned=True), nullable=False)
    wafers = Column(MEDIUMINT(unsigned=True), nullable=False)

    def __init__(self, date: dt.date, ip_name: str, ip_version:str, tapeouts: int, wafers: int):
        """Create a new SavedCommand and immediately adds SavedCommand to the DB."""
        # assert len(date_str) == 8  # YYYYMMDD
        # dt.datetime.strptime(date_str, "%Y%m%d").date()
        self.date = date
        self.ip_name = ip_name  # equivalent to "product" in delivered cells
        self.ip_version = ip_version  # equivalent to "tag" in delivered cells
        self.tapeouts = tapeouts
        self.wafers = wafers

    def __hash__(self):
        return hash(self.ip_name + self.ip_version + str(self.date))

    def __eq__(self, other):
        if isinstance(self, WaferVolume) and isinstance(other, WaferVolume):
            return self.__hash__() == other.__hash__()
        else:
            return False

    def save_to_db_if_not_present(self):
        with Session(bind=TEGGY_ENGINE, expire_on_commit=False) as session:
            wafer_volume = session.query(WaferVolume).filter(
                WaferVolume.date == self.date,
                WaferVolume.ip_name == self.ip_name,
                WaferVolume.ip_version == self.ip_version
            ).first()

            if wafer_volume:
                print("Specific WaferVolume already in database => skipping")
            else:
                # Not in database yet? Add it
                session.add(self)
                session.commit()

    def delete_from_db(self) -> None:
        with Session(bind=TEGGY_ENGINE, expire_on_commit=False) as session:
            session.delete(self)
            session.commit()


if __name__ == "__main__":
    pass
    # entry = WaferVolume(dt.datetime.strptime("20241128", "%Y%m%d").date(),  "test ip name", "test ip version", 1, 100)

