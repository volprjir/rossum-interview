class RossumLoginError(Exception):
    """Raised when there is an error logging into the Rossum API"""
    pass


class RossumExportError(Exception):
    """Raised when there is an error exporting data from the Rossum API"""
    pass


class NoRossumDataError(Exception):
    """Raised when there is no data found in the Rossum XML"""
    pass
