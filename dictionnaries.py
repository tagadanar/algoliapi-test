class Vividict(dict):
    """
    autovivified dictionnary, always have a Vividict as value on new keys
    https://stackoverflow.com/questions/635483/
    """
    def __missing__(self, key):
        value = self[key] = type(self)() # retain local pointer to value
        return value

class Counterdict(dict):
    """ dict that always have an int 0 as value """
    def __missing__(self, key):
        value = self[key] = 0
        return value

