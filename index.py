from Model.votes import Votes
from Model.votes_ranked import VotesRanked

import pandas as pd
import json
from pprint import pprint

a = Votes()
# print(a.find_by_votes('Sherlock Jr.'))
# print(a.in_how_many_list('Sherlock Jr.'))
# print(a.edit_list_name(
# "677fb09af66ace7d105aa786",
#     "votes",
# ))
#
# a.edit_list_vote(
#     "677fd1ebc6675622cab71720",
#     1,
#     'sob o signo de capricórnio',
#     1924
# )

# pprint(a.find_votes_by_year_range(1929, 2024))
# pprint(a.find_null_year())

ranked_votes = VotesRanked()
#
# print(ranked_votes.calculate_votes_result())
# print(ranked_votes.show_votes_by_score(100, 200))
# print(ranked_votes.show_score_by_name('Sunrise'))
# print(ranked_votes.show_vote_quantity())
# print(ranked_votes.info())
# print(a.info())

# df = pd.DataFrame({
#     'idade': [25, 30, 22, 35, 40],
#     'salario': [3000, 4000, 3500, 5000, 6000]
# })
#
# # Visão geral dos tipos de dados
# print(df.info())
#
# # Estatísticas descritivas
# print(df.describe())

# b = a.show_all()
#
# print(b)

# ranked_votes.quantity_votes_graph()
# print(ranked_votes.year_pie_graph())

# pprint(a.find_votes_by_year_range(1920, 1929))

# ranked_votes.year_pie_graph()
print(ranked_votes.calculate_votes_result())
print(a.show_all())
with open('individuals_lists.json', 'w', encoding='utf-8') as f:
    json.dump(a.show_all(), f, default=str, indent=4, ensure_ascii=False)

