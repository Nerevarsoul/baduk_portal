__all__ = ('EmptyKgsTableError', 'KgsGameCreateError', 'OpponentDoneError',)


class EmptyKgsTableError(Exception):
    pass


class KgsGameCreateError(Exception):
    pass


class OpponentDoneError(Exception):
    pass
