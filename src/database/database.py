import os
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from bson.binary import Binary

load_dotenv(find_dotenv())


class DatabaseManager:
    def __init__(self):
        self.cluster = MongoClient(os.environ.get('URI'))
        self.db = self.cluster["pastbot"]
        self.pdf_collections = self.db["files"]
        self.pdf_details_collections = self.db["details"]

    def check_query(self, file_name: str, query: str, type: str = 'None'):
        files = self.get_files()
        return

    def get_files(self):
        files = [file for file in os.listdir() if '.py' in file]
        return files
    
    def read_file_by_name(self, file_name):
        try:
            file = ""
            if file_name:
                file = open(file_name, 'rb')

            return file
        except:
            pass
            
    
    def search_in_database(self):
        pass

    def search_with_scapper(self):
        pass
    
    def insert_file(self, file_name, file, year:str = "Not set"):
        try:
            if file:
                encoded = Binary(file.read())
                data = {file: encoded}
                details = {"file_name": file_name, "year": year, }
                self.pdf_collections.insert_one(data)
        except:
            pass
