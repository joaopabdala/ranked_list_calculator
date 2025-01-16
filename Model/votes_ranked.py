import json
from collections import defaultdict
from pprint import pprint

import pymongo
import pandas as pd
import plotly.express as px



class VotesRanked:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["lists_database"];
        self.collection = db["lists"];

    def calculate_votes_result(self):
        result = self.collection.aggregate([
            {"$addFields": {"totalVotes": {"$size": "$votes"}}},
            {"$unwind": "$votes"},
            {"$addFields": {
                "votes.score": {
                    "$subtract": [
                        {"$add": ["$totalVotes", 1]},
                        "$votes.rank"
                    ]
                }
            }},
            {"$group": {
                "_id": "$votes.title",
                "totalScore": {"$sum": "$votes.score"}
            }},
            {"$sort": {"totalScore": -1}}
        ])

        result_list = list(result)
        with open('result2.json', 'w', encoding='utf-8') as f:
            json.dump(result_list, f, default=str, indent=4, ensure_ascii=False)

        return pd.DataFrame(result_list)

    def show_score_by_name(self, name):
        result = self.collection.aggregate([
            {"$addFields": {"totalVotes": {"$size": "$votes"}}},
            {"$unwind": "$votes"},
            {"$match": {"votes.title": name}},
            {"$addFields": {
                "votes.score": {
                     "$subtract": [
                        {"$add": ["$totalVotes", 1]},
                        "$votes.rank"
                    ]
                }
            }},
            {"$group": {
                "_id": "$votes.title",
                "totalScore": {"$sum": "$votes.score"}
            }},
            {"$sort": {"totalScore": -1}}
        ])

        return pd.DataFrame(list(result))

    def show_votes_by_score(self, min_score, max_score=None):
        result = self.collection.aggregate([
            {"$addFields": {"totalVotes": {"$size": "$votes"}}},
            {"$unwind": "$votes"},
            {"$addFields": {
                "votes.score": {
                     "$subtract": [
                        {"$add": ["$totalVotes", 1]},
                        "$votes.rank"
                    ]
                }
            }},
            {"$group": {
                "_id": "$votes.title",
                "totalScore": {"$sum": "$votes.score"},
            }},
            {"$match": {
                "totalScore": {
                    "$gte": min_score,
                    "$lte": max_score if max_score is not None else float('inf')
                }
            }},
            {"$sort": {"totalScore": -1}}
        ])
        return pd.DataFrame(list(result))

    def show_vote_quantity(self):
        result = self.collection.aggregate([
            {"$unwind": "$votes"},
            {"$group": {
                "_id": "$votes.title",
                "totalVotes": {"$sum": 1}
            }},
            {"$sort": {"totalVotes": -1}}
        ])
        return pd.DataFrame(list(result))

    def show_votes_by_year(self):
        result = self.collection.aggregate([
            {"$unwind": "$votes"},
            {"$group": {
                "_id": "$votes.year",
                "yearSum": {"$sum": 1}
            }},
            {"$sort": {"yearSum": -1}}
        ])
        return pd.DataFrame(list(result))

    def info(self):
        result = self.collection.aggregate([
            {"$addFields": {"totalVotes": {"$size": "$votes"}}},
            {"$unwind": "$votes"},
            {"$addFields": {
                "votes.score": {
                     "$subtract": [
                        {"$add": ["$totalVotes", 1]},
                        "$votes.rank"
                    ]
                }
            }},
            {"$group": {
                "_id": "$votes.title",
                "totalScore": {"$sum": "$votes.score"}
            }},
            {"$sort": {"totalScore": -1}}
        ])

        df= pd.DataFrame(list(result))

        # Visão geral dos tipos de dados
        print(df.info())

        # Estatísticas descritivas
        print(df.describe())

        if 'votes.title' in df.columns:
            print(df['votes.title'].value_counts())

        print(df['_id'].value_counts())


    def score_bar_graph(self):
        data = self.calculate_votes_result()
        fig_histogram = px.bar(data, x="_id", y="totalScore", title="Total Score por Filme",labels={"_id": "Filme", "totalScore": "Total Score"})
        fig_histogram.update_layout(xaxis_title='Pontuação', yaxis_title='Frequência')
        fig_histogram.show()

    def quantity_votes_bar_graph(self):
        data = self.show_vote_quantity()
        fig_histogram = px.bar(data, x="_id", y="totalVotes", title="Total Score por Filme",
                               labels={"_id": "Filme", "totalScore": "Total Score"})
        fig_histogram.update_layout(xaxis_title='Pontuação', yaxis_title='Frequência')
        fig_histogram.show()

    def year_bar_graph(self):
        data = self.show_votes_by_year()
        fig_histogram = px.bar(data, x="_id", y="yearSum", labels={"_id": "Ano", "yearSum": "filmes"})
        fig_histogram.update_layout(xaxis_title='Pontuação', yaxis_title='Frequência')
        fig_histogram.show()

    def year_pie_graph(self):
        data = self.show_votes_by_year()
        fig_histogram = px.pie(data, names="_id", values="yearSum", labels={"_id": "Ano", "yearSum": "filmes"})
        fig_histogram.update_traces(textposition='inside', textinfo='percent+label')
        fig_histogram.show()

    def score_votes_pie_graph(self):
        data = self.show_votes_by_score(10)
        fig_histogram = px.pie(data, names="_id", values="totalScore", title="Total Score por Filme",
                               labels={"_id": "Filme", "totalScore": "Total Score"})
        fig_histogram.update_traces(textposition='inside', textinfo='percent+label')
        fig_histogram.show()





