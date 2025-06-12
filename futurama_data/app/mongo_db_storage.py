from pymongo import MongoClient

def store_characters_in_mongodb(character_data):
    mongo_client = MongoClient("mongodb://localhost:1337")
    mongo_db = mongo_client["futurama"]
    mongo_col = mongo_db["characters"]
    mongo_col.delete_many({})
    mongo_col.insert_many(character_data)

    print("Saved characters to mongodb")

def store_episodes_in_mongodb(episode_data):
    mongo_client = MongoClient("mongodb://localhost:1337")
    mongo_db = mongo_client["futurama"]
    mongo_col = mongo_db["episodes"]
    mongo_col.delete_many({})
    mongo_col.insert_many(episode_data)

    print("Saved episodes in mongodb")