import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

db_uri = os.getenv('DB_URI')
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Reminder(Base):
  __tablename__ = 'reminders'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  is_done = Column(Boolean, default=False)
  date = Column(DateTime)
  files = Column(ARRAY(String))

  def __repr__(self) -> str:
    return f'Reminder(id={self.id}, name={self.name}, is_done={self.is_done}, date={self.date}, files={self.files})'

  @classmethod
  def get(cls, id):
    session = Session()
    return session.query(cls).get(id)

  @classmethod
  def get_all(cls):
    session = Session()
    return session.query(cls).all()

  @classmethod
  def get_all_completed(cls):
    session = Session()
    return session.query(cls).filter_by(is_done=True).all()

  @classmethod
  def get_all_uncompleted(cls):
    session = Session()
    return session.query(cls).filter_by(is_done=False).all()

  @classmethod
  def add(cls, reminder):
    session = Session()
    session.add(reminder)
    session.commit()

  @classmethod
  def update(cls, reminder):
    session = Session()
    session.merge(reminder)
    session.commit()

  @classmethod
  def delete(cls, id):
    session = Session()
    reminder = session.query(cls).get(id)
    if reminder is not None:
      session.delete(reminder)
      session.commit()

if __name__ == '__main__':
  reminders = Reminder.get_all()
  print(reminders)
