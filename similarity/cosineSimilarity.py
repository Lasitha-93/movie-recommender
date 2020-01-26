from math import sqrt


def getCosineSimilarity (profile_1, profile_2):

    features = ['actionScore', 'actorScore', 'comedyScore', 'dramaScore', 'horrorScore', 'plotScore', 'romanceScore', 'themeScore']
    profile_1_scores = []
    profile_2_scores = []

    for feature in features:
        profile_1_scores.append(float(profile_1[feature]))
        profile_2_scores.append(float(profile_2[feature]))

    # squareroot calculator
    def square_rooted(scores):
        return round(sqrt(sum([score*score for score in scores])),3)

    # calculate cosine similarity
    numerator = sum(a*b for a,b in zip(profile_1_scores,profile_2_scores))
    denominator = square_rooted(profile_1_scores)*square_rooted(profile_2_scores)

    if denominator == 0:
        return 0
    else:
        return numerator / denominator
