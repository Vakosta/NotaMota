class Normalizer(object):
    __object_type__ = None
    __total_mean__ = None
    __total_std__ = None

    def __init__(self, obj_type):
        self.__object_type__ = obj_type

    def fit(self, data):
        self.__total_mean__ = data['rating'].mean()
        self.__total_std__ = data['rating'].std()

    def transform(self, data):
        data_tmp = data.copy()
        data_tmp['rating'] = (
            data_tmp
            .groupby(self.__object_type__)['rating']
            .transform(
                lambda x: (x - x.mean()) / x.std()
                if x.std() > 0
                else (x - self.__total_mean__) / self.__total_std__
            )
        )

        return data_tmp
