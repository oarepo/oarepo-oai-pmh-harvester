class EndPointNotFoundError(Exception):
    pass


class PrefixNotFoundError(Exception):
    pass


class ProviderNotFoundError(Exception):
    pass


class RuleRequiredError(Exception):
    pass


class ParserNotFoundError(Exception):
    pass


class HandlerNotFoundError(Exception):
    pass


class NoMigrationError(Exception):
    pass
