class FreshdeskBaseException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message


class AuthenticationException(FreshdeskBaseException):
    pass


class RateLimitException(FreshdeskBaseException):
    def __init__(self, message: str, retry_after: int = 60):
        super().__init__(message)
        self.retry_after = retry_after


class ResourceNotFoundException(FreshdeskBaseException):
    pass


class FreshdeskAPIException(FreshdeskBaseException):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code
