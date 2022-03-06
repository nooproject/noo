class NooError(Exception):
    """Base class for all Noo errors."""

    pass


class NoofileError(NooError):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message

        super().__init__(f"Error in noofile field {field}: {message}")


class ResolutionError(NooError):
    pass


class RunnerError(NooError):
    pass
