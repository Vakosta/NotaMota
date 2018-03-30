def TopN(data, movies, n, reg):
    """
    Returns top N popular movies

    :param data: pandas.DataFrame, ratings like ['user', 'movie', 'rating']
    :param movies: iterable, list of movies to select TopN from
    :param n: int, number of movies to return
    :param reg: float, regularization parameter
    :return: iterable, n movies ordered by popularity
    """
    ratings_sums = data[data['movie'].isin(movies)].groupby('movie').agg({'rating': ['sum', 'count']})
    ratings_sums.columns = ratings_sums.columns.droplevel()
    ratings_sums.reset_index(inplace=True)

    # regularize mean
    ratings_sums['reg_rating'] = ratings_sums["sum"] / (ratings_sums["count"] + reg)

    candidates = (
        ratings_sums[['movie', 'reg_rating']]
        .sort_values(by=['reg_rating'], ascending=False)
        .values[:n]
    )

    return {movie: rating for movie, rating in candidates}
