from collections import defaultdict

import pandas as pd
import pprint as pprint
import pymongo
import re
import json
from tqdm import tqdm
from Services.tmdb_service import TMDB




class DataExtactor:
    def __init__(self, file):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["lists_database"];
        self.collection = db["lists"];
        self.file = file
        self.tmdb = TMDB()

    def reset_database(self):
        self.collection.delete_many({})

    def clean_csv(self):
        csv = pd.read_csv(self.file, skip_blank_lines=True)["Bota"]
        for vote in tqdm(csv, desc="Processing Votes", unit="vote"):
            votes = []
            name = ''
            lines = vote.split("\n")
            movies_count = 0
            for line in lines:
                match = re.match(r"(\d+)?\s*[-]?[)]?[.]?\s*(.*?)\s*[-]?\s*\(?(\d{4})\)?$", line.strip())
                rank = ''
                title = ''
                year = ''
                if match:
                    movies_count+=1
                    rank = movies_count
                    title = match.group(2)
                    year = match.group(3)
                    tmdb_data = self.tmdb.search_movie_by_string(title, year if year not in (0, '') else None)
                    print(title, year, rank)
                    print(tmdb_data)

                    votes.append(
                        {
                            "rank": int(rank) if rank is not None else 0,
                            "title": tmdb_data[0].get('tmdb_title', None),
                            "year": tmdb_data[0].get('tmdb_year', None),
                            "original_language": tmdb_data[0].get('tmdb_original_language', None),
                            "portuguese_title": tmdb_data[0].get('tmdb_portuguese_title', None),
                            "original_query": f"{rank}  {title}  {year}"
                        }
                    )
                else:
                    name_ensure = re.match(r"^[^0-9]*$", line.strip())
                    if name_ensure:
                        name = name_ensure.group()
                    else:
                        name = 'sem nome'
            document = {"voter_name": name, "votes": votes}
            self.collection.insert_one(document)

    def votes_to_json(self):
        collection = list(self.collection.find())
        with open('../arquivo.json', 'w', encoding='utf-8') as f:
            json.dump(collection, f, default=str, indent=4, ensure_ascii=False)

a = DataExtactor('../data/20s-formated.csv');

a.reset_database()
a.clean_csv()
print(a.votes_to_json())
