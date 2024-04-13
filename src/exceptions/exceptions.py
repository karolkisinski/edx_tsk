class RateForDateNotFound(Exception):
    """Raised when the rate doesn't exists."""
    pass


class RatesFileNotFound(Exception):
    """Raised when rates file doesn't exist."""
    pass


class RatesDataInvalid(Exception):
    """Raised when rates file is invalid"""
    pass


class RatesReadError(Exception):
    """Raised when error occured while reading rates file"""
    pass


class NBPAPIError(Exception):
    """Raised when error occured while trying to retrieve data from NBPAPI"""


class InvalidAmountError(ValueError):
    """Raised when provided amount is invalid"""
    pass


class InvalidModeError(Exception):
    """Raised when mode is invalid"""
    pass
