class ChatException(Exception):
    """Base exception for chat operations."""
    pass


class ChatValidationException(ChatException):
    """Exception raised when chat request validation fails."""
    pass


class ChatProcessingException(ChatException):
    """Exception raised when chat processing fails."""
    pass


class ChatServiceException(ChatException):
    """Exception raised when chat service fails."""
    pass 