from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from scrapy.exceptions import DropItem
import datetime as dt

Base = declarative_base()

class MondayPost(Base):
    __tablename__ = 'mondaypost'
    id = Column(Integer, primary_key=True)
    author = Column(String)
    date = Column(Date)
    text = Column(Text)

class MondayPipeline:

    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine) 

    def process_item(self, item, spider):
        new_date = dt.datetime.strptime(item['date'], '%d.%m.%Y')
        if new_date.weekday() == 0:
            post = MondayPost(
                author = item['author'],
                date=new_date,
                text=item['text'],
            )
            self.session.add(post)
            self.session.commit()
            return item
        else:
            raise DropItem('Этотъ постъ написанъ не въ понедѣльникъ')
        

    def close_spider(self, spider):
        self.session.close() 

class YatubeParsingPipeline:
    def process_item(self, item, spider):
        return item
