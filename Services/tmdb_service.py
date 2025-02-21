import requests
from pprint import pprint
from datetime import datetime
import os
# from Services import env_loader


class TMDB:
    def __init__(self):
        self.url = "https://api.themoviedb.org/3/search/movie?&language=pt-BR"
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMjliMDNhZDhjNmQ1MTQ2YzcyZjA1MGMzNGVmMzhkMiIsIm5iZiI6MTYxMTA5ODk4My4yMjcsInN1YiI6IjYwMDc2YjY3MTEwOGE4MDAzZjk0ZmEwNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.MH2aKJehGBybS10VgbRuQmgRNk6v1pHsZ2Ar6S18Kw8"
        }

    def search_movie_by_string(self, title, year):
        params = {"query": title, "primary_release_year": year}
        response = requests.get(self.url, headers=self.headers, params=params)
        response_json = response.json()
        if response_json['total_results'] == 0:
            params = {"query": title}
            response = requests.get(self.url, headers=self.headers, params=params)
            response_json = response.json()

            if response_json['total_results'] == 0:
                return [{
                    "tmdb_title": title,
                    "tmdb_year": year
                }]

        tmdb_title = response_json['results'][0]['original_title']
        tmdb_original_language = response_json['results'][0]['original_language']
        tmdb_portuguese_title = response_json['results'][0]['title']
        date = response_json['results'][0]['release_date']
        date = datetime.strptime(date, "%Y-%m-%d") if date != '' else None
        tmdb_year = int(date.year) if date else None

        content = [{
            "tmdb_title": tmdb_title,
            "tmdb_year": tmdb_year,
            "tmdb_original_language": tmdb_original_language if tmdb_original_language else None,
            "tmdb_portuguese_title": tmdb_portuguese_title if tmdb_portuguese_title else None,
        }]
        return content


