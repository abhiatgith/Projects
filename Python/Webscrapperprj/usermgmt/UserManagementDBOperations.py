import pymongo
from pymongo.errors import ConnectionFailure, InvalidOperation, InvalidName, CollectionInvalid, DuplicateKeyError, ExecutionTimeout, OperationFailure, PyMongoError


class DBUserManagement:

    def __init__(self, url):
        # To create a database in MongoDB, start by creating a MongoClient object
        # then specify a connection URL with the correct ip address and the name of the database you want to create.
        try:
            self.myclient = pymongo.MongoClient(url)
            print("Db Connection is established on {}".format(url))
        except ConnectionFailure as con:
            print(con)
        except PyMongoError as err:
            print(err)

    def checfIfDBExists(self, comparableDBName):

        try:
            dbList = self.myclient.list_database_names()
            if comparableDBName.strip() in dbList:
                return True
            else:
                return False
        except InvalidOperation as inValOps:
            print(inValOps)
        except ConnectionFailure as con:
            print(con)
        except PyMongoError as err:
            print(err)

    def createDatabse(self, dbName):

        # MongoDB will create the database if it does not exist, and make a connection to it.
        # Important: In MongoDB, a database is not created until it gets content!
        # MongoDB waits until you have created a collection (table), with at least one document (record)
        # before it actually creates the database (and collection).
        try:
            dbInstance = self.myclient[dbName]
            return dbInstance
        except InvalidName as name:
            print(name)
        except ConnectionFailure as con:
            print(con)
        except PyMongoError as err:
            print(err)
        return None

    # Creating a Collection
    def checkIfCollectionExist(self, dbInstance, collectionName):
        try:
            colList = dbInstance.list_collection_names()
            if collectionName.strip() in colList:
                return True
            else:
                return False
        except InvalidName as name:
            print(name)
        except ConnectionFailure as con:
            print(con)
        except PyMongoError as err:
            print(err)

    # Creating a Collection
    def createCollection(self, dbInstance, collectionName):
        try:
            dbCollection = dbInstance[collectionName]
            return dbCollection
        except InvalidName as name:
            print(name)
        except ConnectionFailure as con:
            print(con)
        except PyMongoError as err:
            print(err)
        return None
