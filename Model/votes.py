from pprint import pprint

import pymongo
import pandas as pd
import json
from bson.objectid import ObjectId
from pandas import json_normalize
from Services.tmdb_service import TMDB


class Votes:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["lists_database"];
        self.collection = db["lists"];
        self.tmdb = TMDB()

    def insert(self, voter_name, votes):
        votes_list = []
        for vote in votes:
            title = vote['title']
            year = vote['year']
            rank = vote['rank']
            tmdb_data = self.tmdb.search_movie_by_string(title, year if year not in (0, '') else None)
            print(tmdb_data)
            votes_list.append({
                "rank": int(rank) if rank is not None else 0,
                "title": tmdb_data[0].get('tmdb_title', None),
                "year": tmdb_data[0].get('tmdb_year', None),
                "original_language": tmdb_data[0].get('tmdb_original_language', None),
                "portuguese_title": tmdb_data[0].get('tmdb_portuguese_title', None),
                "original_query": f"{rank}  {title}  {year}"
            })
        document = {
            "voter_name": voter_name,
            "votes": votes_list
        }

        try:
            self.collection.insert_one(document)
            return f"Inserted: {document}"
        except Exception as e:
            return f"Error inserting document: {e}"

    def show_all(self):
        documents = pd.DataFrame(list(self.collection.find()))

        result_list = documents.to_dict(orient="records")

        with open('individuals_lists.json', 'w', encoding='utf-8') as f:
            json.dump(result_list, f, default=str, indent=4, ensure_ascii=False)

        return documents

    def find_by_name(self, value):
        query = {"voter_name": value}
        documents = pd.DataFrame(list(self.collection.find(query)))
        return documents

    def find_by_votes(self, value):
        query = {"votes.title": value}
        documents = pd.DataFrame(list(self.collection.find(query)))

        return documents

    def find_votes_by_year_range(self, start, end=None):
        if end == None:
            end = start + 1
        query = {"votes.year": {"$gt": start, "$lt": end}}

        documents = pd.DataFrame(list(self.collection.find(query)))
        filtered = []
        for document in documents['votes']:
            for film in document:
                if film['year'] != None:
                    year = int(film['year'])
                    if (year > start and year < end):
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

    def edit_list_vote(self, id, vote):

        title = vote['title']
        year = vote['year']
        rank = vote['rank']
        tmdb_data = self.tmdb.search_movie_by_string(title, year if year not in (0, '') else None)
        vote_tmdb = {
            "rank": int(rank) if rank is not None else 0,
            "title": tmdb_data[0].get('tmdb_title', None),
            "year": tmdb_data[0].get('tmdb_year', None),
            "original_language": tmdb_data[0].get('tmdb_original_language', None),
            "portuguese_title": tmdb_data[0].get('tmdb_portuguese_title', None),
            "original_query": f"{rank}  {title}  {year}"
        }
        try:
            self.collection.update_one(
                {"_id": ObjectId(id), "votes.rank": rank},
                {"$set": {"votes.$":
                    {
                    "rank": vote_tmdb['rank'],
                    "title": vote_tmdb['title'],
                    "year": vote_tmdb['year'],
                    "original_language": vote_tmdb['original_language'],
                    "portuguese_title": vote_tmdb["portuguese_title"],
                    "original_query": vote_tmdb["original_query"]
                     }
                 }
                }
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
        documents_final = pd.concat(
            [documents_exploded.reset_index(drop=True), documents_normalized.reset_index(drop=True)], axis=1)
        documents_final.drop(columns='votes', inplace=True)

        print(documents_final.describe())

        # Visualizar as informações gerais do DataFrame
        print(documents_final.info())

        print(documents_exploded)
        # return documents.info()
