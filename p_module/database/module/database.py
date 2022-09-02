import pymongo
from p_modules.utilities import logger
import os


def connect_to_database(uri):
    """
    Connects to the Database
    Returns the Database Client.
    If an Exception raises e.g a Connection failed, the Error will be logged.
    """
    try:
        mongo_client = pymongo.MongoClient(uri)
        return mongo_client
    except Exception as e:
        logger.Log.error('Connecting with MongoDB failed: {}'.format(e))


def get_collection(client, db_name, collection_name):
    # Returns the Database.Collection
    return client[db_name][collection_name]


def create_entry(collection, json_format):
    # Creates an entry in the Database.Collection
    return collection.insert_one(json_format)


def read_entry(collection, key, value):
    """
    Returns the entry from the Database.Collection
    If it fails: Exception will be logged & returned
    """
    try:
        return {'status': 200, 'returnValue': collection.find({key: value})[0]}
    except Exception as e:
        logger.Log.error('Exception occurred in {}.read_entry [{}]'.format(e, os.path.splitext(os.path.basename(__file__))[0]))
        return {'status': 100, 'returnValue': e}


def update_entry(collection, key, value, json_format):
    """

    """
    try:
        update_result = collection.update_one({key: value}, {'$set': json_format}, upsert=False)
        if update_result.matched_count == 0:
            return {'status': 100, 'returnValue': 'Error finding Dataset with Key: {}, Value:{}'.format(key, value)}
        if update_result.modified_count == 0:
            return {'status': 100, 'returnValue': 'Error modifying Dataset with Json: {}'.format(json_format)}
        return {'status': 200, 'returnValue': 'Successfully modified Entry'}
    except Exception as e:
        logger.Log.error('Exception occurred in {}.read_entry [{}]'.format(e, os.path.splitext(os.path.basename(__file__))[0]))
        return {'status': 100, 'returnValue': e}


def delete_entry(collection, key, value):
    try:
        delete_result = collection.delete_one({key: value})
        if delete_result.deleted_count == 0:
            return {'status': 100, 'returnValue': 'Error with Deleting Key: {}, Value: {}\n**Incorrect Data?**'.format(key, value)}
        return {'status': 200, 'returnValue': 'Successfully deleted Entry'}
    except Exception as e:
        logger.Log.error('Exception occurred in {}.read_entry [{}]'.format(e, os.path.splitext(os.path.basename(__file__))[0]))
        return {'status': 100, 'returnValue': e}
