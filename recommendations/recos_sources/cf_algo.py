import pandas as pd
from recommendations import NearestNeighbours


def CollaborativeFilter(data, user, movies, n, k, reg):
    """
    Predicts ratings for a user's not rated movies by collaborative filtering

    param df: pandas.DataFrame
    param user: str or int, chat id
    param movies: iterable, list of movies to select recommendations from
    param n: int, number of recommendations to return
    param k: int, number of nearest neighbours to use
    param reg: float, regularization number
    return: pandas.DataFrame
    """
    ratings = {'movie': [], 'uu': [], 'ii': []}
    not_watched = set(data['movie'].unique()) - set(data[data['user'] == user]['movie'].unique())

    # for similar users
    user_nn = NearestNeighbours(data, user, 'user', k)
    similar_users = user_nn.kNN(k)
    data_users = data[data['user'].isin(similar_users.keys())]

    # for similar movies
    data_movies = data[data['user'] == user]

    for movie in not_watched:
        ratings['movie'].append(movie)

        # USER-USER CF
        knn_ratings = data_users[data['movie'] == movie]

        ratings_sum, weights_sum = 0.0, 0.0
        for row in knn_ratings.itertuples():
            ratings_sum += row[3] * similar_users[row[1]]
            weights_sum += similar_users[row[1]]

        if reg + weights_sum > 0:
            ratings['uu'].append(ratings_sum / (reg + weights_sum))
        else:
            ratings['uu'].append(0)

        # ITEM-ITEM CF
        movie_nns = NearestNeighbours(data, movie, 'movie', k)
        similar_movies = movie_nns.kNN(k)
        knn_ratings = data_movies[data_movies['movie'].isin(similar_movies.keys())]

        ratings_sum, weights_sum = 0.0, 0.0
        for row in knn_ratings.itertuples():
            ratings_sum += row[3] * similar_movies[row[2]]
            weights_sum += similar_movies[row[2]]

        if reg + weights_sum > 0:
            ratings['ii'].append(ratings_sum / (reg + weights_sum))
        else:
            ratings['ii'].append(0)

    predictors = pd.DataFrame(ratings)
    predictors = predictors[predictors['movie'].isin(movies)]
    predictors['rating'] = predictors['uu'] + predictors['ii']

    candidates = (
        predictors[['movie', 'rating']]
        .sort_values(by='rating', ascending=False)
        .values[:n]
    )

    return {movie: rating for movie, rating in candidates}
