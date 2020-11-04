# TODO: otestovat celý kód, zde je Mock harvestu
#  https://github.com/mloesch/sickle/blob/master/sickle/tests/test_harvesting.py
import os

from sickle import OAIResponse
from sickle._compat import to_unicode


class MockResponse(object):
    """Mimics the response object returned by HTTP requests."""

    def __init__(self, text):
        # request's response object carry an attribute 'text' which contains
        # the server's response data encoded as unicode.
        self.text = text
        self.content = text.encode('utf-8')


def mock_harvest(*args, **kwargs):
    """Read test data from files instead of from an OAI interface.
    The data is read from the ``xml`` directory by using the provided
    :attr:`verb` as file name. The following returns an OAIResponse created
    from the file ``ListRecords.xml``::
        fake_harvest(verb='ListRecords', metadataPrefix='oai_dc')
    The file names for consecutive resumption responses are expected in the
    resumptionToken parameter::
        fake_harvest(verb='ListRecords', resumptionToken='ListRecords2.xml')
    The parameter :attr:`error` can be used to invoke a specific OAI error
    response. For instance, the following returns a ``badArgument`` error
    response::
        fake_harvest(verb='ListRecords', error='badArgument')
    :param kwargs: OAI arguments that would normally be passed to
                   :meth:`sickle.app.Sickle.harvest`.
    :rtype: :class:`sickle.response.OAIResponse`.
    """
    this_dir, this_filename = os.path.split(__file__)
    verb = kwargs.get('verb')
    resumption_token = kwargs.get('resumptionToken')
    error = kwargs.get('error')
    if resumption_token is not None:
        filename = resumption_token
    elif error is not None:
        filename = '%s.xml' % error
    else:
        filename = '%s.xml' % verb

    with open(os.path.join(this_dir, 'data', filename), 'r') as fp:
        response = MockResponse(to_unicode(fp.read()))
        return OAIResponse(response, kwargs)