class CasinoError(Exception):
    pass



class InsufficientBalance(CasinoError):

    def __init__(self):

        super().__init__(
            "Insufficient balance."
        )



class InvalidAmount(CasinoError):

    def __init__(self):

        super().__init__(
            "Invalid amount."
        )



class PermissionDenied(CasinoError):

    def __init__(self):

        super().__init__(
            "You don't have permission to use this command."
        )



class CooldownError(CasinoError):

    def __init__(self, time):

        super().__init__(
            f"Please wait `{time}` before using this again."
        )
