import pandas as pd
import numpy as np
import json
import apicalls.ontology as onto


def now_showing_rec(user_id):

    with open('../recommender/heat_movies.json') as file:
        new_data = json.load(file)

    user_profile = onto.getUserById(user_id)

    if user_profile is not None:

        feature_n_score = [[user_profile['actionScore'], 'Action'], [user_profile['comedyScore'], 'Comedy'], [user_profile['dramaScore'], 'Drama'], [user_profile['horrorScore'], 'Horror'], [user_profile['romanceScore'], 'Romance']]

        feature_n_score.sort()
        feature_n_score.reverse()
        first_three_features = feature_n_score[:2]
        print("user's",first_three_features)

        theatre_movies = new_data['intheatres']
        upcoming_movies = new_data['upcoming']
        suggesting_movies = {"intheatres": [], "upcoming": []}

        for theatre_movie in theatre_movies:
            print(theatre_movie['genres'])
            if len(np.intersect1d(theatre_movie['genres'], [i[1] for i in first_three_features])) > 0:
                suggesting_movies['intheatres'].append(theatre_movie)

        for upcoming_movie in upcoming_movies:
            print(upcoming_movie['genres'])
            if len(np.intersect1d(upcoming_movie['genres'], [i[1] for i in first_three_features])) > 0:
                suggesting_movies['upcoming'].append(upcoming_movie)

        return suggesting_movies
    else:
        return new_data


# print(now_showing_rec(17))
