import similarity.cosineSimilarity as cs
import apicalls.mongoDB as mongo
import apicalls.ontology as onto
import time


def getUserFeatureBasedRecommendations(user_id):

    all_users = onto.getAllUserProfiles()

    user_profile = None
    for user in all_users:
        if user['user'] is not None:
            if user['user'] == str(user_id):
                user_profile = user

    print("inGetRec")

    recommendation_list = []
    top_recommendations = []
    user_sims = []

    for current_user in all_users:
        if user_profile['user'] is not None:
            if current_user['user'] == user_profile['user']:
                continue

            else:
                similarity = cs.getCosineSimilarity(user_profile, current_user)
                # print(current_user['user'], similarity)
                user_sims.append([similarity, current_user['user']])

    user_watchlists = mongo.getAllUserWatchLists()
    # time.sleep(100)
    print("user watchlists done!")
    all_movie_profiles = onto.getAllMovieProfiles()
    print("movie profile fetching done!")
    # under user key the values is a two dimentional array of movie id, rating
    user_watchlist = user_watchlists[user_profile['user']]
    print("user_watchlist ", user_watchlist, user_profile['user'])
    user_watchlist_movie_ids = []

    for watched_movie in user_watchlist:
        user_watchlist_movie_ids.append(watched_movie[0])

    unseen_movie_list = []
    for movie_profile in all_movie_profiles:
        for user_watchlist_movie_id in user_watchlist_movie_ids:
            if user_watchlist_movie_id == movie_profile['movie']:
                continue
            else:
                unseen_movie_list.append(movie_profile)

    for unseen_movie in unseen_movie_list:

        # print(unseen_movie['movie'])

        sim_rating_total = 0
        total_sims = 0

        watched_users_list = []
        for user_id, movie_list in user_watchlists.items():
            for movie in movie_list:
                if unseen_movie['movie'] == movie[0]:
                    watched_users_list.append([user_id, movie])
                else:
                    continue

        if len(watched_users_list) > 0:
            for watched_usr in watched_users_list:

                for user_sim in user_sims:

                    if user_sim[1] == watched_usr[0] and user_sim[0] > 0:
                        sim_rating_total += user_sim[0]*watched_usr[1][1]
                        # print(watched_usr[1][1])
                        total_sims += user_sim[0]

                    else:
                        continue

    #     get the rating from available_best_match
        if sim_rating_total > 0:
            predicted_rating = sim_rating_total/total_sims
            # print('movie id: ', unseen_movie, ' predicted rating: ', rating, 'best match user: ', available_best_match, 'best match user sim: ', available_highest_sim)
            if predicted_rating >= 3 and predicted_rating <=4:
                recommendation_list.append([predicted_rating, unseen_movie])

    recommendation_list.sort()
    recommendation_list.reverse()

    top_rec_id_pool = []

    for recommended_movie in recommendation_list:
        if recommended_movie[1]['movie'] in top_rec_id_pool:
            continue
        else:
            top_recommendations.append(recommended_movie[1])
            top_rec_id_pool.append(recommended_movie[1]['movie'])

    return top_recommendations

