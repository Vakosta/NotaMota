import pandas as pd
from recommendations import K_NEAREST_NEIGHBOURS, N_RECS
from recommendations.recos_sources import TopN, RandomTrash, CollaborativeFilter
from recommendations.transformer import Normalizer


def candidates_mixed(topn, trash, cf):
    """
    Mixes candidates together
    :param topn: dict, {movie: rating}, TopN recommendations
    :param trash: iterable, trash recommendations
    :param cf: dict, {movie: rating}, CF recommendations
    :return: dict, {movie: rating}, all recommendations combined together
    """
    # normalize weights
    topn = {key: value / sum(topn.values()) for key, value in topn}
    cf = {key: 3*value / sum(cf.values()) for key, value in cf}
    recs = {**topn, **cf}

    trash_new = {}
    for movie in trash:
        if movie not in recs.keys():
            # trash takes
            trash_new[movie] = 1
    trash_new = {key: value / sum(trash_new.values()) for key, value in trash_new}
    recs = {**trash_new, **recs}

    return recs


def get_candidates(data, user):
    """
    Returns recommendation for a given user

    :param data: dict, {(user, movie): rating}
    :param user: str or int, chat id
    :return: {movie: rating}
    """
    # transform cache data into pandas.DataFrame
    records = []
    for key, value in data.items():
        records.append((key[0], key[1], value))
    df = pd.DataFrame.from_records(records, columns=('user', 'movie', 'rating'))
    not_watched = set(df['movies'].unique()) - set(df[df['user'] == user]['movies'].unique())

    # normalize ratings
    transformer = Normalizer('user')
    transformer.fit(df)
    df_scaled = transformer.transform(df)

    # regularization parameter
    reg_number = min(df_scaled.groupby('movie').count().mean() / 3, 10)

    # calculate recs
    topn_recos = TopN(df_scaled, not_watched, N_RECS, reg_number)
    trash_recos = RandomTrash(df_scaled, not_watched, N_RECS)
    cf_recos = CollaborativeFilter(df_scaled, user, not_watched, N_RECS, K_NEAREST_NEIGHBOURS, reg_number)

    # mix candidates
    return candidates_mixed(topn=topn_recos, trash=trash_recos, cf=cf_recos)
