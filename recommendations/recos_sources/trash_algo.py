def RandomTrash(data, movies, n):
    """
    Randomly selects non-popular movies from list

    :param data: pandas.DataFrame, data like ['user', 'movie', 'rating']
    :param movies: iterable, list of movies to select trash from
    :param n: int, number of movies to select
    :return: iterable, list of selected movies
    """
    ratings_count = data.groupby("movie").count()
    ratings_count = ratings_count.drop(["user"], axis=1).reset_index()
    reg_number = ratings_count["rating"].mean() / 2

    recs = ratings_count[ratings_count['movie'].isin(movies)][ratings_count['rating'] < reg_number]

    if len(recs) > 0:
        return recs.sample(min(len(recs), n))['movie']
    else:
        return None
