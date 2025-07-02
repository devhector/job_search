class InvalidCookieException(Exception):
    """Raised when the session cookie is invalid or expired."""

    def __init__(self, message, platform_name=None):
        super().__init__(message)
        self.platform_name = platform_name
