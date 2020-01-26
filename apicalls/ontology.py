import requests as req
import apicalls.apitunnels as t


def getAllUserProfiles():

    response = req.post("http://"+t.onto+".ngrok.io/byUserProfileSearch")
    all_users = response.json()
    print("total user count: ", len(all_users))

    return all_users


def getAllMovieProfiles():

    response = req.post("http://"+t.onto+".ngrok.io/byMovieProfileSearch")
    all_movies = response.json()
    print("total movie count: ", len(all_movies))

    return all_movies

# print(getAllMovieProfiles())


def initiateAutoComplete():

    response = req.get("http://"+t.onto+".ngrok.io/byMovieIdwtNameSearch")

    return response.content


def myMood(data):

    mood = data['mood']
    userid = data['user_id']
    print(mood, userid)
    response = req.post("http://"+t.onto+".ngrok.io/byMoodSearch", data={'user_id': userid, 'mood': mood})
    print(response.content)

    return response.content


def getUserById(userid):

    response = req.post("http://"+t.onto+".ngrok.io/byUserProfileByIdSearch", data={'user_id': userid})
    data = response.json()

    if len(data) > 0:
        return data[0]

    else:
        return None



