class ParseError(Exception):
    """Failed to parse source data."""


class UnsupportedFormatError(ParseError):
    """Source format is not supported."""


class MalformedRecordError(ParseError):
    """Source record is malformed."""
