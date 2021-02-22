# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Index, String(100)
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, LONGTEXT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata



class Chapter(Base):
    __tablename__ = 'search_chapter'

    id = Column(INTEGER(11), primary_key=True)
    chapter = Column(INTEGER(11), nullable=False)
    note = Column(LONGTEXT, nullable=False)
    additional_note = Column(LONGTEXT, nullable=False)


class Heading(Base):
    __tablename__ = 'search_headings'

    id = Column(INTEGER(11), primary_key=True)
    heading = Column(String(100), nullable=False)
    description = Column(LONGTEXT, nullable=False)


class Tarriff(Base):
    __tablename__ = 'search_tarriff'

    id = Column(INTEGER(11), primary_key=True)
    chapter = Column(INTEGER(11), nullable=False)
    heading = Column(String(100), nullable=False)
    sub_heading = Column(String(100), nullable=False)
    sub_sub_heading = Column(String(100), nullable=False)
    cd = Column(INTEGER(11), nullable=False)
    description = Column(LONGTEXT, nullable=False)
    statistical_unit = Column(LONGTEXT, nullable=False)
    general_rate_of_duty = Column(String(100), nullable=False)
    eu_rate_of_duty = Column(String(100), nullable=False)
    efta_rate_of_duty = Column(String(100), nullable=False)
    sadc_rate_of_duty = Column(String(100), nullable=False)
    mercosur_rate_of_duty = Column(String(100), nullable=False)


