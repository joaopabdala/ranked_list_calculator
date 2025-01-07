from collections import defaultdict

import pymongo
import pandas as pd

class VotesRanked:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["lists_database"];
        self.collection = db["lists"];
        self.ranked_collection = db["ranked_collection"]

    def calculate_votes_result(self) -> None:

        scores = defaultdict(int)
        votes = self.collection.find()

        for vote in votes:
            votes = vote['votes']
            max_score = len(votes)

        for position, (key, value) in enumerate(sorted(enumerate(votes))):
            scores[value] = max_score - position + 1

        ranked_list = [{"item": key, "score": value} for key, value in scores.items()]
        ranked_list = sorted(ranked_list, key=lambda x: x['score'], reverse=True)


        self.ranked_collection.delete_many({})
        self.ranked_collection.insert_many(ranked_list)


    def show_ranked_list(self) -> pd.DataFrame:
        return pd.DataFrame(list(self.ranked_collection.find()))

raked_votes = VotesRanked()

raked_votes.calculate_votes_result()
print(raked_votes.show_ranked_list())