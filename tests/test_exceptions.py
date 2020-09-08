import pytest

from oarepo_oai_pmh_harvester.exceptions import EndPointNotFoundError, \
    PrefixNotFoundError, \
    ProviderNotFoundError, RuleRequiredError, ParserNotFoundError, HandlerNotFoundError


def test_exceptions():
    with pytest.raises(EndPointNotFoundError):
        raise EndPointNotFoundError

    with pytest.raises(PrefixNotFoundError):
        raise PrefixNotFoundError

    with pytest.raises(ProviderNotFoundError):
        raise ProviderNotFoundError

    with pytest.raises(ParserNotFoundError):
        raise ParserNotFoundError

    with pytest.raises(HandlerNotFoundError):
        raise HandlerNotFoundError

    with pytest.raises(RuleRequiredError):
        raise RuleRequiredError
