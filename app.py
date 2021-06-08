from flask import Flask, jsonify, request
from dfilter import output
from cbfilter import get_recommendations


import csv
all_articles = []

with open('shared_artcles.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]

liked_articles = []
disliked_movies = []

app = Flask(__name__)

@app.route("/all-articles")
def get_movie():
    global all_articles
    articles_data = {
        "title": all_articles[0][19],
        "release_date": all_articles[0][13] or "N/A",
        "duration": all_articles[0][15],
        "rating": all_articles[0][20],
        "overview": all_articles[0][9]
    }
    return jsonify({
        "data": articles_data,
        "status": "success"
    })

@app.route("/liked-articles", methods=["POST"])
def liked_movie():
    global all_articles
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/disliked-articles", methods=["POST"])
def disliked_movie():
    global all_articles
    article = all_articles[0]
    disliked_movies.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
  app.run(debug=True)