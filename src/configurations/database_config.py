from functools import lru_cache

from bson.codec_options import TypeRegistry, CodecOptions
from bson.decimal128 import DecimalEncoder, DecimalDecoder
from pymongo import MongoClient
from pymongo.synchronous.database import Database

from configurations.settings import get_settings

client: MongoClient = None
db: Database = None


def connect_to_mongo():
	"""a function to connect to mongo db"""
	global client, db
	client = MongoClient(get_settings().DATABASE_URI)
	print("Connected to Mongo Client")
	db = client[get_settings().DATABASE_NAME]
	print("Connected to Mongo Database")


def get_db():
	"""a function that provides the database instance"""
	if db is None:
		raise RuntimeError("Database connection failed")
	return db


@lru_cache
def get_decimal_codec():
	"""a function that allows mongodb properly  serialise decimal.Decimal instances. not required"""
	type_registry = TypeRegistry([DecimalEncoder(), DecimalDecoder()])
	codec_options = CodecOptions(type_registry=type_registry)
	return codec_options