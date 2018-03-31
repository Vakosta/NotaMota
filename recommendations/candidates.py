import pandas as pd

from recommendations import K_NEAREST_NEIGHBOURS, N_RECS
from recommendations.recos_sources import TopN, RandomTrash, CollaborativeFilter
from recommendations.transformer import Normalizer


def candidates_mixed(topn, cf, trash=None):
    """
    Mixes candidates together
    :param topn: dict, {movie: rating}, TopN recommendations
    :param trash: iterable, trash recommendations
    :param cf: dict, {movie: rating}, CF recommendations
    :return: dict, {movie: rating}, all recommendations combined together
    """
    # normalize weights
    topn = {key: value / (1+sum(topn.values())) for key, value in topn.items()}
    topn_message = {key: 'Этот фильм очень популярен' for key in topn.keys()}
    cf = {key:  2*value / (1+sum(cf.values())) for key, value in cf.items()}
    cf_message = {key: 'Возможно, тебе понравится этот фильм' for key in cf.keys()}
    recs = {**topn, **cf}
    messages = {**topn_message, **cf_message}

    if trash is not None:
        trash_new = {}
        for movie in trash:
            if movie not in recs.keys():
                # trash takes
                trash_new[movie] = 1
        trash_new = {key: 2*value / (1+sum(trash_new.values())) for key, value in trash_new.items()}
        trash_message = {key: 'А вдруг...' for key in trash_new.keys()}
        recs = {**trash_new, **recs}
        messages = {**trash_message, **messages}

    return recs, messages


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
    not_watched = set(df['movie'].unique()) - set(df[df['user'] == user]['movie'].unique())

    # normalize ratings
    transformer = Normalizer('user')
    transformer.fit(df)
    df_scaled = transformer.transform(df)

    # regularization parameter
    counts = df_scaled.groupby('movie')['rating'].count()
    reg_number = min(counts.mean() / 3, 10)

    # calculate recs
    topn_recos = TopN(df_scaled, not_watched, N_RECS, reg_number)
    trash_recos = RandomTrash(df_scaled, not_watched, N_RECS)
    cf_recos = CollaborativeFilter(df_scaled, user, not_watched, N_RECS, K_NEAREST_NEIGHBOURS, reg_number)

    # mix candidates
    return candidates_mixed(topn=topn_recos, cf=cf_recos, trash=trash_recos)
