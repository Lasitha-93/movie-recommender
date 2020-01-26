from pymongo import MongoClient
import time
import requests as req
import apicalls.apitunnels as t
# from bson.json_util import dumps
import numpy as np

client = MongoClient(t.mongo)


def getAllUserWatchLists():

    db = client.movie_system_db
    users = db.user_profile.find({})
    watch_lists_by_users = {}
    # print("total: ", users.count())
    for user in users:
        movie_n_rating = []
        movie_ids = []
        posts = user['posts']
        for post in posts:
            movie_ids.append(post['movie_Url'])
            # print(post['movie_Url'])
        # print(movie_ids)
        # count = 0
        for i in range(0, len(movie_ids), 1):
            feature_scores = []
            # print(movie_ids[i])
            # print(user['userid'])
            label = db.labeled_score.find_one({'user_id': user['userid'], 'movie_id': 'tt'+str(movie_ids[i])})
            genres = db.genre_level.find({'user_id': user['userid'], 'movie_id': 'tt'+str(movie_ids[i])})

            if bool(label) > 0:
                feature_scores.append(label['positive']*5)
                # print("plot score", label['positive']*5)

            if genres is not None:
                for genre in genres:
                    feature_scores.append(genre['action'])
                    feature_scores.append(genre['drama'])
                    feature_scores.append(genre['horror'])
                    feature_scores.append(genre['romance'])
                    feature_scores.append(genre['comedy'])

            # print(feature_scores)
            final_rating = np.sum(feature_scores)/6
            movie_n_rating.append([movie_ids[i], final_rating])

        watch_lists_by_users[user['userid']] = movie_n_rating
        # print(user['userid'], movie_n_rating)

    return watch_lists_by_users

# print(getAllUserWatchLists())
def setNewUserReview(form_data):

    movieid = form_data['movie']
    userid = form_data['user_id']

    labels = ['actor', 'theme', 'plot']
    max_label_score = 1
    max_label = 'plot'
    for label in labels:
        if max_label_score < int(form_data[label]):
            max_label_score = int(form_data[label])/5
            max_label = label

    action = int(form_data['action'])
    comedy = int(form_data['comedy'])
    drama = int(form_data['drama'])
    horror = int(form_data['horror'])
    romance = int(form_data['romance'])

    db = client.movie_system_db

    obj_user_profile = insertPost(userid, movieid)
    obj_genre_level = db.genre_level.insert_one({'user_id': userid, 'movie_id': movieid, 'drama': drama, 'action': action, 'comedy': comedy, 'horror': horror, 'romance': romance})
    obj_labeled_score = db.labeled_score.insert_one({'user_id': userid, 'movie_id': movieid, 'label': max_label, 'positive': max_label_score})

    if obj_user_profile and obj_genre_level is not None and obj_labeled_score is not None:

        return {'response': True}
    else:
        return {'response': False}



def getLasestId():

    db = client.movie_system_db
    users = db.user_profile.find({})

    max_id = 0

    for user in users:
        if max_id< int(user['userid']):
            max_id = int(user['userid'])

    return str(max_id+1)


def insertUser(user_profile, userid):

    db = client.movie_system_db

    username = user_profile['username']
    password = user_profile['password']

    gender = user_profile['gender']
    birthday = user_profile['birthday']
    location = user_profile['location']
    name = user_profile['name']
    #not sending to ontology
    hometown = user_profile['hometown']
    obj_id_login = db.login_details.insert_one({'userid': userid, 'username': username, 'password': password})
    obj_id_full = db.user_profile.insert_one({'userid': userid, 'name': name, 'birthday': birthday, 'location': location, 'gender': gender, 'hometown': hometown, 'posts': []})
    onto_response = req.post('http://'+t.onto+'.ngrok.io/byAddNewUser', data = {'userid': userid, 'name': name, 'birthday': birthday, 'location': location, 'gender': gender})

    if obj_id_login is not None and obj_id_full is not None and onto_response.status_code == req.codes.ok:
        return True
    else:
        return False

def validateUsernamePassword(username, password):

    db = client.movie_system_db
    obj_id_login = db.login_details.find_one({'username': username, 'password': password})

    if obj_id_login is not None:

        userid = obj_id_login['userid']
        reviews = getReviewCount(userid)

        return_data = {'success': True, 'userid': userid, 'name': obj_id_login['username'], 'reviews': reviews}

        return return_data
    else:
        return {'success': False}


def getReviewCount(userid):

    db = client.movie_system_db
    user = db.user_profile.find_one({'userid': str(userid)})
    watch_lists_by_users = {}
    # print("total: ", users.count())
    posts = user['posts']
    return len(posts)


def insertPost(user_id, movie_id):

    db = client.movie_system_db
    user_profile = db.user_profile.find_one({"userid": user_id})

    new_post = [{'movie_Url': movie_id}]

    old_posts = user_profile['posts']
    for old_post in old_posts:
        new_post.append(old_post)

    user_profile['posts'] = new_post
    print(new_post)

    obj_id_user_profile = db.user_profile.update_one({'userid': user_id}, {"$set": user_profile}, upsert=False)

    if obj_id_user_profile is not None:
        return True

    else:
        return False



# def test():
#     db = client.movie_system_db
# #     # users = dumps(db.user_profile.find({}))
# #     # for user in users:
#     user = db.user_profile.find_one({'userid': 53})
# #     # users = db.user_profile.find({})
#     posts = user['posts']
#     print(len(posts))
#
# #     for genre in genres:
# #         print(genre['positive'])
# #
# test()
