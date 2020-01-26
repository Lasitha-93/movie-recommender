import requests as req
import recommender.collobarativeFitering as rc
import recommender.whats_new as wn
import apicalls.ontology as onto
import apicalls.mongoDB as mongo


def userRecommendations(user_id):

    return rc.getUserFeatureBasedRecommendations(user_id)
    # rec = [{'actionScore': '3.0', 'actor': 'Keanu Reeves', 'actorScore': '1.0', 'comedyScore': '2.0', 'country': 'China', 'director': 'Chad Stahelski', 'dramaScore': '2.0', 'horrorScore': '2.5', 'movie': '2911666', 'name': 'John Wick', 'plotScore': '4', 'popularity': '202', 'romanceScore': '4.0', 'runtime': '101', 'source': 'IMDb', 'themeScore': 0, 'thumbnail': 'MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@. V1 UX182 CR0,0,182,268 AL .jpg', 'videoId': '2273816345', 'year': '2014'}, {'actionScore': '3.0', 'actor': 'Jason Clarke', 'actorScore': 0, 'comedyScore': '1.0', 'country': 'UK', 'director': 'Baltasar KormÃ¡kur', 'dramaScore': '1.0', 'horrorScore': '2.5', 'movie': '2719848', 'name': 'Everest', 'plotScore': 0, 'popularity': '1,116', 'romanceScore': '4.0', 'runtime': '121', 'source': 'IMDb', 'themeScore': '1', 'thumbnail': 'MV5BMTNmMzM0ZTktZWY3Yy00ODViLTllZDgtODcwM2QyM2E2YTU2L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@. V1 UX182 CR0,0,182,268 AL .jpg', 'videoId': '1946006297', 'year': '2015'}, {'actionScore': '3.0', 'actor': 'Keanu Reeves', 'actorScore': '1.0', 'comedyScore': '2.0', 'country': 'China', 'director': 'Chad Stahelski', 'dramaScore': '2.0', 'horrorScore': '2.5', 'movie': '2911666', 'name': 'John Wick', 'plotScore': '50.0', 'popularity': '202', 'romanceScore': '4.0', 'runtime': '101', 'source': 'IMDb', 'themeScore': 0, 'thumbnail': 'MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@. V1 UX182 CR0,0,182,268 AL .jpg', 'videoId': '2273816345', 'year': '2014'}]
    # return rec

# print(userRecommendations(10))

def registerUser(data):

    details_json = data
    granted_id = mongo.getLasestId()

    return mongo.insertUser(details_json, granted_id)


def checkCredintials(credintials):

    username = credintials['username']
    password = credintials['password']

    return mongo.validateUsernamePassword(username, password)


def autoComplete():

    return onto.initiateAutoComplete()


def whatsNew(user_id):

    return wn.now_showing_rec(user_id)

# whatsNew(11)

def setNewUserReview(form_data):

    return mongo.setNewUserReview(form_data)


