import json
from pymongo import MongoClient
from swarm import Agent
import logging
from swarm.types import AgentFunction
from typing import Any, List
from datetime import datetime


class MongoAssistant(Agent):
    mongo_host: str = ''
    mongo_port: str = ''
    mongo_user: str = ''
    mongo_pass: str = ''
    client: Any = {}  

    def __init__(self):
        super().__init__()
        self.name: str = "Mongo Assistant"
        self.model: str = "gpt-4o"
        # Read instructions from the Markdown file
        with open('tools/mongo_assistant.md', 'r') as file:
            self.instructions = file.read()
        self.functions: List[AgentFunction] = [self.query_mongo, self.list_collections, self.list_databases, self.aggregate_mongo, self.get_current_date]

        with open('parameters.json', 'r') as file:
            params = json.load(file)

        self.mongo_host = params.get('mongo_host', 'localhost')
        self.mongo_port = params.get('mongo_port', 27017)
        self.mongo_user = params.get('mongo_user', None)
        self.mongo_pass = params.get('mongo_pass', None)

        # Establish connection
        if self.mongo_user and self.mongo_pass:
            self.client = MongoClient(
                self.mongo_host,
                self.mongo_port,
                username=self.mongo_user,
                password=self.mongo_pass
            )
        else:
            self.client = MongoClient(self.mongo_host, self.mongo_port, directConnection=True)


    def query_mongo(self, db_name, collection_name, filter_query=None):
        """
        Execute a read-only query on the specified collection and print the query.

        :param db_name: Name of the database to query.
        :param collection_name: Name of the collection within the database.
        :param filter_query: Optional filter to apply to the query.
        :return: Cursor object with query results or error message.
        """
        try:
            db = self.client[db_name]
            collection = db[collection_name]

            if filter_query is None:
                filter_query = {}

            logging.info(f"Executing query on {db_name}.{collection_name}: {filter_query}")
            cursor = collection.find(filter_query).limit(3)  # Limit results to 3 documents if no filter is specified

            documents = []
            for document in cursor:
                documents.append(document)

            return documents

        except Exception as e:
            error_message = f"An error occurred in query_mongo: {str(e)}"
            logging.info(error_message)
            return error_message

    def list_collections(self, db_name):
        """
        List all collections in the specified database.

        :param db_name: Name of the database.
        :return: List of collection names or error message.
        """
        try:
            db = self.client[db_name]
            collections = db.list_collection_names()
            logging.info(f"Collections in {db_name}: {collections}")
            return collections
        except Exception as e:
            error_message = f"An error occurred in list_collections: {str(e)}"
            logging.info(error_message)
            return error_message

    def list_databases(self):
        """
        List all databases in the MongoDB instance.

        :return: List of database names or error message.
        """
        try:
            databases = self.client.list_database_names()
            logging.info(f"Databases available: {databases}")
            return databases
        except Exception as e:
            error_message = f"An error occurred in list_databases: {str(e)}"
            logging.info(error_message)
            return error_message

    def aggregate_mongo(self, db_name, collection_name, pipeline):
        """
        Execute an aggregation pipeline on the specified collection.

        :param db_name: Name of the database to query.
        :param collection_name: Name of the collection within the database.
        :param pipeline: A list representing the aggregation pipeline.
        :return: List of documents resulting from the aggregation or error message.
        """
        try:
            db = self.client[db_name]
            collection = db[collection_name]

            logging.info(f"Executing aggregation on {db_name}.{collection_name}: {pipeline}")
            results = collection.aggregate(pipeline)

            documents = []
            for document in results:
                documents.append(document)

            return documents

        except Exception as e:
            error_message = f"An error occurred in aggregate_mongo: {str(e)}"
            logging.info(error_message)
            return error_message

    def get_current_date(self):
        """
        Get the current date in UTC format.

        :return: Current date as a datetime object.
        """
        return datetime.utcnow()
