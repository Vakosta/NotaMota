def RandomTrash(data, n):
    ratings_count = data.groupby("movie").count()
    ratings_count = ratings_count.drop(["user"], axis=1)
    reg_number = ratings_count["rating"].mean() / 2

    return ratings_count[ratings_count['rating'] < reg_number].sample(n).index