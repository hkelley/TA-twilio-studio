# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page
from twilio.rest.studio.v1.flow.engagement.step.step_context import StepContextList


class StepList(ListResource):

    def __init__(self, version, flow_sid, engagement_sid):
        """
        Initialize the StepList

        :param Version version: Version that contains the resource
        :param flow_sid: The SID of the Flow
        :param engagement_sid: The SID of the Engagement

        :returns: twilio.rest.studio.v1.flow.engagement.step.StepList
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepList
        """
        super(StepList, self).__init__(version)

        # Path Solution
        self._solution = {'flow_sid': flow_sid, 'engagement_sid': engagement_sid, }
        self._uri = '/Flows/{flow_sid}/Engagements/{engagement_sid}/Steps'.format(**self._solution)

    def stream(self, limit=None, page_size=None):
        """
        Streams StepInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.studio.v1.flow.engagement.step.StepInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(page_size=limits['page_size'], )

        return self._version.stream(page, limits['limit'])

    def list(self, limit=None, page_size=None):
        """
        Lists StepInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.studio.v1.flow.engagement.step.StepInstance]
        """
        return list(self.stream(limit=limit, page_size=page_size, ))

    def page(self, page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of StepInstance records from the API.
        Request is executed immediately

        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of StepInstance
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepPage
        """
        data = values.of({'PageToken': page_token, 'Page': page_number, 'PageSize': page_size, })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return StepPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of StepInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of StepInstance
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return StepPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a StepContext

        :param sid: The SID that identifies the resource to fetch

        :returns: twilio.rest.studio.v1.flow.engagement.step.StepContext
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepContext
        """
        return StepContext(
            self._version,
            flow_sid=self._solution['flow_sid'],
            engagement_sid=self._solution['engagement_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a StepContext

        :param sid: The SID that identifies the resource to fetch

        :returns: twilio.rest.studio.v1.flow.engagement.step.StepContext
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepContext
        """
        return StepContext(
            self._version,
            flow_sid=self._solution['flow_sid'],
            engagement_sid=self._solution['engagement_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Studio.V1.StepList>'


class StepPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the StepPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param flow_sid: The SID of the Flow
        :param engagement_sid: The SID of the Engagement

        :returns: twilio.rest.studio.v1.flow.engagement.step.StepPage
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepPage
        """
        super(StepPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of StepInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.studio.v1.flow.engagement.step.StepInstance
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepInstance
        """
        return StepInstance(
            self._version,
            payload,
            flow_sid=self._solution['flow_sid'],
            engagement_sid=self._solution['engagement_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Studio.V1.StepPage>'


class StepContext(InstanceContext):

    def __init__(self, version, flow_sid, engagement_sid, sid):
        """
        Initialize the StepContext

        :param Version version: Version that contains the resource
        :param flow_sid: The SID of the Flow
        :param engagement_sid: The SID of the Engagement
        :param sid: The SID that identifies the resource to fetch

        :returns: twilio.rest.studio.v1.flow.engagement.step.StepContext
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepContext
        """
        super(StepContext, self).__init__(version)

        # Path Solution
        self._solution = {'flow_sid': flow_sid, 'engagement_sid': engagement_sid, 'sid': sid, }
        self._uri = '/Flows/{flow_sid}/Engagements/{engagement_sid}/Steps/{sid}'.format(**self._solution)

        # Dependents
        self._step_context = None

    def fetch(self):
        """
        Fetch the StepInstance

        :returns: The fetched StepInstance
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return StepInstance(
            self._version,
            payload,
            flow_sid=self._solution['flow_sid'],
            engagement_sid=self._solution['engagement_sid'],
            sid=self._solution['sid'],
        )

    @property
    def step_context(self):
        """
        Access the step_context

        :returns: twilio.rest.studio.v1.flow.engagement.step.step_context.StepContextList
        :rtype: twilio.rest.studio.v1.flow.engagement.step.step_context.StepContextList
        """
        if self._step_context is None:
            self._step_context = StepContextList(
                self._version,
                flow_sid=self._solution['flow_sid'],
                engagement_sid=self._solution['engagement_sid'],
                step_sid=self._solution['sid'],
            )
        return self._step_context

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Studio.V1.StepContext {}>'.format(context)


class StepInstance(InstanceResource):

    def __init__(self, version, payload, flow_sid, engagement_sid, sid=None):
        """
        Initialize the StepInstance

        :returns: twilio.rest.studio.v1.flow.engagement.step.StepInstance
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepInstance
        """
        super(StepInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'sid': payload.get('sid'),
            'account_sid': payload.get('account_sid'),
            'flow_sid': payload.get('flow_sid'),
            'engagement_sid': payload.get('engagement_sid'),
            'name': payload.get('name'),
            'context': payload.get('context'),
            'transitioned_from': payload.get('transitioned_from'),
            'transitioned_to': payload.get('transitioned_to'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'url': payload.get('url'),
            'links': payload.get('links'),
        }

        # Context
        self._context = None
        self._solution = {
            'flow_sid': flow_sid,
            'engagement_sid': engagement_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: StepContext for this StepInstance
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepContext
        """
        if self._context is None:
            self._context = StepContext(
                self._version,
                flow_sid=self._solution['flow_sid'],
                engagement_sid=self._solution['engagement_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def sid(self):
        """
        :returns: The unique string that identifies the resource
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def account_sid(self):
        """
        :returns: The SID of the Account that created the resource
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def flow_sid(self):
        """
        :returns: The SID of the Flow
        :rtype: unicode
        """
        return self._properties['flow_sid']

    @property
    def engagement_sid(self):
        """
        :returns: The SID of the Engagement
        :rtype: unicode
        """
        return self._properties['engagement_sid']

    @property
    def name(self):
        """
        :returns: The event that caused the Flow to transition to the Step
        :rtype: unicode
        """
        return self._properties['name']

    @property
    def context(self):
        """
        :returns: The current state of the flow
        :rtype: dict
        """
        return self._properties['context']

    @property
    def transitioned_from(self):
        """
        :returns: The Widget that preceded the Widget for the Step
        :rtype: unicode
        """
        return self._properties['transitioned_from']

    @property
    def transitioned_to(self):
        """
        :returns: The Widget that will follow the Widget for the Step
        :rtype: unicode
        """
        return self._properties['transitioned_to']

    @property
    def date_created(self):
        """
        :returns: The ISO 8601 date and time in GMT when the resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The ISO 8601 date and time in GMT when the resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def url(self):
        """
        :returns: The absolute URL of the resource
        :rtype: unicode
        """
        return self._properties['url']

    @property
    def links(self):
        """
        :returns: The URLs of related resources
        :rtype: unicode
        """
        return self._properties['links']

    def fetch(self):
        """
        Fetch the StepInstance

        :returns: The fetched StepInstance
        :rtype: twilio.rest.studio.v1.flow.engagement.step.StepInstance
        """
        return self._proxy.fetch()

    @property
    def step_context(self):
        """
        Access the step_context

        :returns: twilio.rest.studio.v1.flow.engagement.step.step_context.StepContextList
        :rtype: twilio.rest.studio.v1.flow.engagement.step.step_context.StepContextList
        """
        return self._proxy.step_context

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Studio.V1.StepInstance {}>'.format(context)