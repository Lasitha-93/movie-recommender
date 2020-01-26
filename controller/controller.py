from flask import Flask, jsonify, request
import requests as req
import services.services as svs

app = Flask(__name__)

@app.route('/')
def get_recommendation():
    return "Hello, World!"

# @app.route('/byMovieTypeSearch', methods=['POST'])
# def byMatSearch():


@app.route('/register', methods=['POST'])
def registerUser():

    data = request.form
    response = svs.registerUser(data)

    return jsonify(response)


@app.route('/login', methods=['POST'])
def userLogin():

    return jsonify(svs.checkCredintials(request.form))

@app.route('/autoComplete', methods=['GET'])
def autoComplete():

    return svs.autoComplete()


@app.route('/setNewUserReview', methods=['POST'])
def setNewUserReview():

    return jsonify(svs.setNewUserReview(request.form))

@app.route('/getBasicRecById', methods=['POST'])
def basicRecommendationsById():
    user_id = request.form['user_id']
    # print(user_id)
    # response = req.post("https://a76dc099.ngrok.io/byUserProfileByIdSearch", data={'user_id': user_id})
    return jsonify(svs.userRecommendations(user_id))
    # return jsonify(runQuery.searchByMovieType('ActionMovie'))

@app.route('/whatsNewById', methods=['POST'])
def whatsNew():
    user_id = request.form['user_id']

    return jsonify(svs.whatsNew(user_id))

if __name__ == '__main__':
    app.run(debug=True)
