import abc


class JSONifiable(object):
    @abc.abstractmethod
    def json_rep(self):
        """
           Return an object that can be jsonencoded.
        """
