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
# a.insert(
#     voter_name="aaaa",
#     votes=[
#         {
#             "title": "sunrise",
#             "year": "1927",
#             "rank": "1"
#         },
#         {
#             "title": "faust",
#             "year": "1926",
#             "rank": 2
#         }
#     ]
# )
# a.edit_list_vote(
#     id="67b7c48cc1f21c787ce5d826",
#     vote={
#             "title": "La Passion de Jeanne d'Arc",
#             "year": 1928,
#             "rank": 1
#         }
#
# )

# a.delete("67b7c48cc1f21c787ce5d826")

# pprint(a.find_votes_by_year_range(1925, 1929))
# pprint(a.find_null_year())

ranked_votes = VotesRanked()
#
# print(ranked_votes.calculate_votes_result())
# print(ranked_votes.show_votes_by_score(100, 200))
# print(ranked_votes.show_score_by_name('Sherlock Jr.'))
# print(ranked_votes.show_vote_quantity())
# print(a.info())
ranked_votes.score_bar_graph()
ranked_votes.quantity_votes_bar_graph()
ranked_votes.score_votes_pie_graph()
ranked_votes.year_pie_graph()
ranked_votes.year_bar_graph()
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
# print(ranked_votes.calculate_votes_result())
# print(ranked_votes.show_votes_by_year())
# print(ranked_votes.show_vote_quantity())
# print(pd.DataFrame(a.show_all()))
