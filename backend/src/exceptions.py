"""Main exception base classes."""

class ApplicationException(Exception):
    """Base application error."""
    
    def __init__(self, message: str, status: int) -> None:
        """Set values.
        
        Parameters
        ----------
         message: str
         status: int
        
        Returns
        -------
         nothing
        
        """
        self.message = message
        self.status = status
    

class GeocodingError(ApplicationException):
    """Error with geocoding address."""
    
    pass