from pprint import pprint

import pymongo
import pandas as pd
from bson.objectid import ObjectId
from pandas import json_normalize


class Votes:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["lists_database"];
        self.collection = db["lists"];


    def insert(self, name, votes):
        new_list = {
            "voter_name": name,
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
        query = {"voter_name": value}
        documents = pd.DataFrame(list(self.collection.find(query)))
        return documents

    def find_by_votes(self, value):
        query = {"votes.title": value}
        documents = pd.DataFrame(list(self.collection.find(query)))

        return documents

    def find_votes_by_year_range(self, star, end= None):
        if end == None:
            end = star + 1
        query ={ "votes.year": {"$gt": star, "$lt": end}}

        documents = pd.DataFrame(list(self.collection.find(query)))
        filtered = []
        for document in documents['votes']:
            for film in document:
                if film['year'] != None:
                    year = int(film['year'])
                    if(year  > star and year < end):
                        filtered.append(film)

        return filtered

    def find_null_year(self):
        query = {"votes.year": None}
        documents = (list(self.collection.find(query)))
        filtered = []
        if not documents:
            return 'Nenhum ano nulo'
        for document in documents:
            print(documents)
            if 'votes' in document:  # Verifica se a chave 'votes' existe no documento
                for film in document['votes']:  # Itera sobre a lista de votos
                    if film['year'] is None:  # Verifica se 'year' é None
                        filtered.append(film)

        return filtered

    def in_how_many_list(self, value):
        query = {"votes.title": value}
        documents = self.collection.count_documents(query)


        return documents

    def edit_list_name(self, id, value):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"voter_name": value}}
            )
            if result.modified_count > 0:
                return f"Document with id {id} updated successfully."
            else:
                return f"No changes made to the document with id {id}."
        except Exception as e:
            return f"Error updating document: {e}"

    def edit_list_vote(self, id, rank, title, year):
        try:
            self.collection.update_one(
                {"_id": ObjectId(id), "votes.rank": rank},
                {"$set": {"votes.$": {"rank": rank, "title": title, "year": year}}}
            )
        except Exception as e:
            print(e)


    def delete(self, id):
        try:
            self.collection.delete_one({"_id": ObjectId(id)})
        except Exception as e:
            return f"Error inserting document: {e}"

    def info(self):
        documents = pd.DataFrame(list(self.collection.find()))
        documents_exploded = documents.explode('votes')
        documents_normalized = json_normalize(documents_exploded['votes'])
        documents_final = pd.concat([documents_exploded.reset_index(drop=True), documents_normalized.reset_index(drop=True)], axis=1)
        documents_final.drop(columns='votes', inplace=True)

        print(documents_final.describe())

        # Visualizar as informações gerais do DataFrame
        print(documents_final.info())

        print(documents_exploded)
        # return documents.info()



