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
    id = Column(UUID(as_uuid=True),primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),)
    symbol = sa.Column(sa.VARCHAR(50))
    headline = sa.Column(sa.TEXT())
    related = sa.Column(sa.TEXT())
    source = sa.Column(sa.VARCHAR(50))
    summary = sa.Column(sa.TEXT())
    datetime = sa.Column(sa.TIMESTAMP())


# class to model the fellow object
class tweet(Base):
    __tablename__ = "raw_tweet_data"

    """

	id						uuid DEFAULT uuid_generate_v4(),
	searched_name 			varchar(50) NOT NULL,
	timestamp				TIMESTAMPTZ NOT NULL, 
	retweet_count			INTEGER,
	favorite_count			INTEGER,
	text					text,
	retweeted				INTEGER,
	favorited				INTEGER,
	user_following			INTEGER,
	user_friends_count		INTEGER,
	user_location			varchar(50),
	user_favourites_count	INTEGER,					
	user_name				varchar(50),
	user_followers_count	INTEGER,
	user_listed_count		INTEGER,
	hashtags				text,
	sentiment_score			NUMERIC
	

    """
    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=sa.text("uuid_generate_v4()"), )

    searched_name = sa.Column(sa.VARCHAR(50))
    timestamp = sa.Column(sa.TIMESTAMP())
    retweet_count = sa.Column(sa.INTEGER())
    favorite_count = sa.Column(sa.INTEGER())
    text = sa.Column(sa.TEXT())
    retweeted = sa.Column(sa.BOOLEAN())
    favorited = sa.Column(sa.BOOLEAN())
    user_following = sa.Column(sa.INTEGER())
    user_listed_count = sa.Column(sa.INTEGER())
    user_followers_count = sa.Column(sa.INTEGER())
    user_friends_count = sa.Column(sa.INTEGER())
    user_favourites_count = sa.Column(sa.INTEGER())
    user_location = sa.Column(sa.VARCHAR(50))
    user_name = sa.Column(sa.VARCHAR(50))
    hashtags = sa.Column(sa.TEXT())
    sentiment_score = sa.Column(sa.NUMERIC())


# class to model the fellow object
class trade(Base):
    __tablename__ = "stock_market_data"

    """

	id						uuid DEFAULT uuid_generate_v4(),
	symbol 							varchar(50) NOT NULL,
	companyName						varchar(50)	,
	primaryExchange					varchar(50),
	sector							varchar(50),
	calculationPrice				NUMERIC,
	open						    NUMERIC,
	close							NUMERIC,
	high							NUMERIC,
	low								NUMERIC,
	latestPrice						NUMERIC,
	latestSource					varchar(50),
	latestTime						TIMESTAMPTZ NOT NULL, 
	latestVolume					INTEGER,
	previousClose					NUMERIC,
	change							NUMERIC,
	changePercent					NUMERIC,
	avgTotalVolume					INTEGER,
	marketCap						INTEGER,
	peRatio							NUMERIC,
	week52High						NUMERIC,
	week52Low						NUMERIC,
	ytdChange						NUMERIC,
	movementPrice					NUMERIC,
	movementVolume					NUMERIC

    """
    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=sa.text("uuid_generate_v4()"), )

    symbol = sa.Column(sa.VARCHAR(50))
    companyname = sa.Column(sa.VARCHAR(500))
    primaryexchange =  sa.Column(sa.VARCHAR(50))
    sector = sa.Column(sa.VARCHAR(50))
    # calculationprice = sa.Column(sa.NUMERIC())
    open = sa.Column(sa.NUMERIC())
    close = sa.Column(sa.NUMERIC())
    high = sa.Column(sa.NUMERIC())
    low = sa.Column(sa.NUMERIC())
    latestprice = sa.Column(sa.NUMERIC())
    latestsource = sa.Column(sa.VARCHAR(50))
    latesttime = sa.Column(sa.TIMESTAMP())
    latestvolume = sa.Column(sa.INTEGER())
    previousclose = sa.Column(sa.NUMERIC())
    change = sa.Column(sa.NUMERIC())
    changepercent = sa.Column(sa.NUMERIC())
    avgtotalvolume =  sa.Column(sa.BIGINT())
    marketcap = sa.Column(sa.BIGINT())
    peratio = sa.Column(sa.NUMERIC())
    week52high = sa.Column(sa.NUMERIC())
    week52low = sa.Column(sa.NUMERIC())
    ytdchange = sa.Column(sa.NUMERIC())
    movementprice = sa.Column(sa.NUMERIC())
    movementvolume = sa.Column(sa.NUMERIC())
