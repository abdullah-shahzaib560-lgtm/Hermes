class NormalizationError(Exception):
    """Failed to normalize data."""


class ConversionError(NormalizationError):
    """Type conversion failed."""
