# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import serialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class RecordingList(ListResource):

    def __init__(self, version, account_sid, conference_sid):
        """
        Initialize the RecordingList

        :param Version version: Version that contains the resource
        :param account_sid: The SID of the Account that created the resource
        :param conference_sid: The Conference SID that identifies the conference associated with the recording

        :returns: twilio.rest.api.v2010.account.conference.recording.RecordingList
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingList
        """
        super(RecordingList, self).__init__(version)

        # Path Solution
        self._solution = {'account_sid': account_sid, 'conference_sid': conference_sid, }
        self._uri = '/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings.json'.format(**self._solution)

    def stream(self, date_created_before=values.unset, date_created=values.unset,
               date_created_after=values.unset, limit=None, page_size=None):
        """
        Streams RecordingInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param date date_created_before: The `YYYY-MM-DD` value of the resources to read
        :param date date_created: The `YYYY-MM-DD` value of the resources to read
        :param date date_created_after: The `YYYY-MM-DD` value of the resources to read
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.conference.recording.RecordingInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            date_created_before=date_created_before,
            date_created=date_created,
            date_created_after=date_created_after,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'])

    def list(self, date_created_before=values.unset, date_created=values.unset,
             date_created_after=values.unset, limit=None, page_size=None):
        """
        Lists RecordingInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param date date_created_before: The `YYYY-MM-DD` value of the resources to read
        :param date date_created: The `YYYY-MM-DD` value of the resources to read
        :param date date_created_after: The `YYYY-MM-DD` value of the resources to read
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.conference.recording.RecordingInstance]
        """
        return list(self.stream(
            date_created_before=date_created_before,
            date_created=date_created,
            date_created_after=date_created_after,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, date_created_before=values.unset, date_created=values.unset,
             date_created_after=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of RecordingInstance records from the API.
        Request is executed immediately

        :param date date_created_before: The `YYYY-MM-DD` value of the resources to read
        :param date date_created: The `YYYY-MM-DD` value of the resources to read
        :param date date_created_after: The `YYYY-MM-DD` value of the resources to read
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of RecordingInstance
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingPage
        """
        data = values.of({
            'DateCreated<': serialize.iso8601_date(date_created_before),
            'DateCreated': serialize.iso8601_date(date_created),
            'DateCreated>': serialize.iso8601_date(date_created_after),
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return RecordingPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of RecordingInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of RecordingInstance
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return RecordingPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a RecordingContext

        :param sid: The unique string that identifies the resource

        :returns: twilio.rest.api.v2010.account.conference.recording.RecordingContext
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingContext
        """
        return RecordingContext(
            self._version,
            account_sid=self._solution['account_sid'],
            conference_sid=self._solution['conference_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a RecordingContext

        :param sid: The unique string that identifies the resource

        :returns: twilio.rest.api.v2010.account.conference.recording.RecordingContext
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingContext
        """
        return RecordingContext(
            self._version,
            account_sid=self._solution['account_sid'],
            conference_sid=self._solution['conference_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.RecordingList>'


class RecordingPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the RecordingPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The SID of the Account that created the resource
        :param conference_sid: The Conference SID that identifies the conference associated with the recording

        :returns: twilio.rest.api.v2010.account.conference.recording.RecordingPage
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingPage
        """
        super(RecordingPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of RecordingInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.api.v2010.account.conference.recording.RecordingInstance
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingInstance
        """
        return RecordingInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            conference_sid=self._solution['conference_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.RecordingPage>'


class RecordingContext(InstanceContext):

    def __init__(self, version, account_sid, conference_sid, sid):
        """
        Initialize the RecordingContext

        :param Version version: Version that contains the resource
        :param account_sid: The SID of the Account that created the resource to fetch
        :param conference_sid: Fetch by unique Conference SID for the recording
        :param sid: The unique string that identifies the resource

        :returns: twilio.rest.api.v2010.account.conference.recording.RecordingContext
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingContext
        """
        super(RecordingContext, self).__init__(version)

        # Path Solution
        self._solution = {'account_sid': account_sid, 'conference_sid': conference_sid, 'sid': sid, }
        self._uri = '/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings/{sid}.json'.format(**self._solution)

    def update(self, status, pause_behavior=values.unset):
        """
        Update the RecordingInstance

        :param RecordingInstance.Status status: The new status of the recording
        :param unicode pause_behavior: Whether to record during a pause

        :returns: The updated RecordingInstance
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingInstance
        """
        data = values.of({'Status': status, 'PauseBehavior': pause_behavior, })

        payload = self._version.update(method='POST', uri=self._uri, data=data, )

        return RecordingInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            conference_sid=self._solution['conference_sid'],
            sid=self._solution['sid'],
        )

    def fetch(self):
        """
        Fetch the RecordingInstance

        :returns: The fetched RecordingInstance
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return RecordingInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            conference_sid=self._solution['conference_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the RecordingInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete(method='DELETE', uri=self._uri, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.RecordingContext {}>'.format(context)


class RecordingInstance(InstanceResource):

    class Status(object):
        IN_PROGRESS = "in-progress"
        PAUSED = "paused"
        STOPPED = "stopped"
        PROCESSING = "processing"
        COMPLETED = "completed"
        ABSENT = "absent"

    class Source(object):
        DIALVERB = "DialVerb"
        CONFERENCE = "Conference"
        OUTBOUNDAPI = "OutboundAPI"
        TRUNKING = "Trunking"
        RECORDVERB = "RecordVerb"
        STARTCALLRECORDINGAPI = "StartCallRecordingAPI"
        STARTCONFERENCERECORDINGAPI = "StartConferenceRecordingAPI"

    def __init__(self, version, payload, account_sid, conference_sid, sid=None):
        """
        Initialize the RecordingInstance

        :returns: twilio.rest.api.v2010.account.conference.recording.RecordingInstance
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingInstance
        """
        super(RecordingInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'api_version': payload.get('api_version'),
            'call_sid': payload.get('call_sid'),
            'conference_sid': payload.get('conference_sid'),
            'date_created': deserialize.rfc2822_datetime(payload.get('date_created')),
            'date_updated': deserialize.rfc2822_datetime(payload.get('date_updated')),
            'start_time': deserialize.rfc2822_datetime(payload.get('start_time')),
            'duration': payload.get('duration'),
            'sid': payload.get('sid'),
            'price': payload.get('price'),
            'price_unit': payload.get('price_unit'),
            'status': payload.get('status'),
            'channels': deserialize.integer(payload.get('channels')),
            'source': payload.get('source'),
            'error_code': deserialize.integer(payload.get('error_code')),
            'encryption_details': payload.get('encryption_details'),
            'uri': payload.get('uri'),
        }

        # Context
        self._context = None
        self._solution = {
            'account_sid': account_sid,
            'conference_sid': conference_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: RecordingContext for this RecordingInstance
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingContext
        """
        if self._context is None:
            self._context = RecordingContext(
                self._version,
                account_sid=self._solution['account_sid'],
                conference_sid=self._solution['conference_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The SID of the Account that created the resource
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def api_version(self):
        """
        :returns: The API version used to create the recording
        :rtype: unicode
        """
        return self._properties['api_version']

    @property
    def call_sid(self):
        """
        :returns: The SID of the Call the resource is associated with
        :rtype: unicode
        """
        return self._properties['call_sid']

    @property
    def conference_sid(self):
        """
        :returns: The Conference SID that identifies the conference associated with the recording
        :rtype: unicode
        """
        return self._properties['conference_sid']

    @property
    def date_created(self):
        """
        :returns: The RFC 2822 date and time in GMT that the resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The RFC 2822 date and time in GMT that the resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def start_time(self):
        """
        :returns: The start time of the recording, given in RFC 2822 format
        :rtype: datetime
        """
        return self._properties['start_time']

    @property
    def duration(self):
        """
        :returns: The length of the recording in seconds
        :rtype: unicode
        """
        return self._properties['duration']

    @property
    def sid(self):
        """
        :returns: The unique string that identifies the resource
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def price(self):
        """
        :returns: The one-time cost of creating the recording.
        :rtype: unicode
        """
        return self._properties['price']

    @property
    def price_unit(self):
        """
        :returns: The currency used in the price property.
        :rtype: unicode
        """
        return self._properties['price_unit']

    @property
    def status(self):
        """
        :returns: The status of the recording
        :rtype: RecordingInstance.Status
        """
        return self._properties['status']

    @property
    def channels(self):
        """
        :returns: The number of channels in the final recording file as an integer
        :rtype: unicode
        """
        return self._properties['channels']

    @property
    def source(self):
        """
        :returns: How the recording was created
        :rtype: RecordingInstance.Source
        """
        return self._properties['source']

    @property
    def error_code(self):
        """
        :returns: More information about why the recording is missing, if status is `absent`.
        :rtype: unicode
        """
        return self._properties['error_code']

    @property
    def encryption_details(self):
        """
        :returns: How to decrypt the recording.
        :rtype: dict
        """
        return self._properties['encryption_details']

    @property
    def uri(self):
        """
        :returns: The URI of the resource, relative to `https://api.twilio.com`
        :rtype: unicode
        """
        return self._properties['uri']

    def update(self, status, pause_behavior=values.unset):
        """
        Update the RecordingInstance

        :param RecordingInstance.Status status: The new status of the recording
        :param unicode pause_behavior: Whether to record during a pause

        :returns: The updated RecordingInstance
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingInstance
        """
        return self._proxy.update(status, pause_behavior=pause_behavior, )

    def fetch(self):
        """
        Fetch the RecordingInstance

        :returns: The fetched RecordingInstance
        :rtype: twilio.rest.api.v2010.account.conference.recording.RecordingInstance
        """
        return self._proxy.fetch()

    def delete(self):
        """
        Deletes the RecordingInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.RecordingInstance {}>'.format(context)