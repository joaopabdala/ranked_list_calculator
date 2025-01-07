from pprint import pprint

import pymongo
import pandas as pd
from bson.objectid import ObjectId

class Votes:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["lists_database"];
        self.collection = db["lists"];


    def insert(self, name, votes):
        new_list = {
            "name": name,
            "votes": votes,
        }
        try:
            self.collection.insert_one(new_list)
            return f"Inserted: {new_list}"
        except Exception as e:
            return f"Error inserting document: {e}"


    def show_all(self):
        documents = pd.DataFrame(list(self.collection.find()))
        return documents


    def find_by_name(self, value):
        query = {"name": value}
        documents = pd.DataFrame(list(self.collection.find(query)))
        return documents

    def find_by_votes(self, value):
        query = {"votes": "a"}
        documents = self.collection.find()
        filtered_documents = [doc for doc in documents if value in doc["votes"].values()]

        return list(filtered_documents)

    def edit(self, id, option, value):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {option: value}}
            )
            if result.modified_count > 0:
                return f"Document with id {id} updated successfully."
            else:
                return f"No changes made to the document with id {id}."
        except Exception as e:
            return f"Error updating document: {e}"


    def delete(self, id):
        try:
            self.collection.delete_one({"_id": ObjectId(id)})
        except Exception as e:
            return f"Error inserting document: {e}"


