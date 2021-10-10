class FastLRUCache(object):
    __slots__ = ['__key2value', '__max_size', '__weights']

    def __init__(self, max_size: int):
        self.__max_size = max_size
        self.__key2value = {}  # key->value
        self.__weights = []  # keys ordered in LRU

    def __update_weight(self, key):
        try:
            self.__weights.remove(key)
        except ValueError:
            pass
        self.__weights.append(key)  # add key to end
        if len(self.__weights) > self.__max_size:
            _key = self.__weights.pop(0)  # remove first key
            self.__key2value.pop(_key)

    def __getitem__(self, key):
        try:
            value = self.__key2value[key]
            self.__update_weight(key)
            return value
        except KeyError:
            raise KeyError("key %s not found" % key)

    def get(self, key, default=None):
        try:
            value = self.__key2value[key]
            self.__update_weight(key)
            return value
        except KeyError:
            return default

    def __setitem__(self, key, value):
        self.__key2value[key] = value
        self.__update_weight(key)

    def __str__(self):
        return str(self.__key2value)

    def size(self):
        return len(self.__key2value)

