# This script contains user defined exceptions

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class DfsError(Error):
    """Exception raised for errors in the output of Dfs algorithm."""
    # Do nothing

class BfsError(Error):
    """Exception raised for errors in the output of Bfs algorithm."""
    # Do nothing 

