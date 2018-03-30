import numpy as np
from recommendations import antitype


class NearestNeighbours(object):
    __object__ = None
    __object_type__ = None
    __k_max__ = None
    __neighbours__ = None

    def __init__(self, data, obj_name, obj_type, k_max):
        self.__object__ = obj_name
        self.__object_type__ = obj_type
        self.__k_max__ = k_max
        self.refresh_neighbours(data)

    def refresh_neighbours(self, data):
        """
        k Nearest Neighbours

        param df: pandas.DataFrame, ratings like ['user', 'movie', 'rating']
        param obj_name: str, object name
        param obj_type: 'user' or 'movie', object type
        """
        neighbours = []

        # only use objects with rating
        evaluated = data[(data[self.__object_type__] == self.__object__)]

        for obj in data[self.__object_type__].unique():
            if obj == self.__object__:
                continue

            matched = evaluated.merge(
                data.loc[data[self.__object_type__] == obj],
                on=antitype[self.__object_type__],
                how='inner',
                suffixes=['', '_nb']
            )

            if len(matched) > 0:
                neighbours.append((obj, cosine(matched['rating'], matched['rating_nb'])))

            neighbours = sorted(neighbours, key=lambda x: x[1])[-self.__k_max__:]

        self.__neighbours__ = neighbours
        del neighbours
        return

    def kNN(self, k):
        return {key: val for key, val in
                self.__neighbours__[-k:]}


def cosine(vector1, vector2):
    """
    Calculates cosine distance

    param vector1: array-like, ratings
    param vector2: array-like, ratings

    return: float, cos(vector1, vector2)
    """
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))