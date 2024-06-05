

# Indicates the AI made a mistake, possibly retriable.
class ThoughtCrime(Exception):
    '''
    Thrown when the AI makes a mistake. Execution may be automatically retried, 
    if all retries fail, this will be raised to the caller.

    This will typically be thrown from unweaves, for example:

    .. code-block:: python

        try:
            name = name_axiomic.value()
        except axiomic.errors.ThoughtCrime:
            name = 'Unknown'
    '''
    pass


# Indicates the user built an incorrect weave, not retriable.
class RuntimeError(Exception):
    '''
    Thrown when there is an error in the way a weave was built.
    For example, if assinging an invalid name.
    '''
    def __init__(self, text=None, panel=None):
        self.panel = panel
        self.text = text

    def __str__(self):
        if self.panel:
            return str(self.panel)
        return self.text


# Indicates the user built an incorrect weave, not retriable.
class GraphError(Exception):
    '''
    Thrown when there is an error in the way a weave was built.
    For example, if assinging an invalid name.
    '''
    def __init__(self, text=None, panel=None):
        self.panel = panel
        self.text = text

    def __str__(self):
        if self.panel:
            return str(self.panel)
        return self.text


class ProviderErrorRetriable(Exception):
    '''
    Thrown when an error when calling an API which is re-triable.
    This includes, rate limit. 
    '''
    def __init__(self, message):
        self.message = message


class ProviderErrorNoRetry(Exception):
    '''
    An error with the API that should be retried.
    '''
    def __init__(self, message):
        self.message = message

