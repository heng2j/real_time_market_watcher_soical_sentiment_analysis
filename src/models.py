#!/usr/bin/env python3
# models.py
# ---------------
# Author: Zhongheng Li
# Start Date: 1-19-19
# Last Modified Date: 1-21-19


"""
This is the models module that store the schema for the objects that we are using in this project


"""


# System modules


# 3rd party modules
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column

# Setting for sqlalchemy
Base = declarative_base()

# class to model the fellow object
class news(Base):
    __tablename__ = "raw_news_data"

    """
    id     uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol 							varchar(50) NOT NULL,
	headline						text,
	related							text,
	source						    varchar(50),
	summary							text,
	datetime						TIMESTAMPTZ NOT NULL
    
    """
    id = Column(UUID(as_uuid=True),
        server_default=sa.text("uuid_generate_v4()"),)
    symbol = sa.Column(sa.VARCHAR(50))
    headline = sa.Column(sa.TEXT())
    related = sa.Column(sa.TEXT())
    source = sa.Column(sa.VARCHAR(50))
    summary = sa.Column(sa.TEXT())
    datetime = sa.Column(sa.TIMESTAMP(), primary_key=True)
