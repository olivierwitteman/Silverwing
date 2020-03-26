class AbstractMessage(object):
    def __init__(self, data):

        """ A string representation of the raw data.

        Type:
            string
        """
        self._string = str(data)

        """ A list of _parameters derived from the raw data.
        
        Type:
            list<Parameter>
        """
        self._parameters = self._setParameters(data)

    """ Sets the message _parameters based on the data provided.
    
    Each AbstractMessage is initialised with data. This method parses that data and returns a list of
    Parameters, complete with name, unit and value (both mapped and raw).
    
    Returns:
        list<Parameter>: List of _parameters.
    """

    @classmethod
    def _setParameters(cls, data):
        raise NotImplementedError('Subclasses must override __fill()!')

    """ Getter method for the _parameters.
    
    Returns:
        list<Parameter>: The list of _parameters.
    """

    def getParameters(self):
        return self._parameters

    """ Getter method for a single element of _parameters.

    Args:
        index (int): The index within _parameters of the desired parameter.
    Returns:
        Parameter: The list of _parameters.
    """

    def getParameter(self, index):
        return self._parameters[index]

    """ Generates the string representation of itself.
    
    Returns:
        string: The string representation.
    """

    def toString(self):
        string = self.__class__.__name__ + ': ' + self._string.rstrip()
        for parameter in self.getParameters():
            if parameter is not None:
                string += '\n  ' + parameter.toString()
        return string
