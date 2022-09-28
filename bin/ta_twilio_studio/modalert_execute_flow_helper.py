import base64
import json

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

#from urllib.parse import urlparse, urlencode
#from urllib.request import urlopen, Request

# encoding = utf-8

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets and sets the log level
    helper.set_log_level(helper.log_level)

    # The following example gets account information
    user_account = helper.get_user_credential("<account_name>")

    # The following example gets the setup parameters and prints them to the log
    splunk_api_callback_host = helper.get_global_setting("splunk_api_callback_host")
    helper.log_info("splunk_api_callback_host={}".format(splunk_api_callback_host))

    # The following example gets the alert action parameters and prints them to the log
    studio_flow_id = helper.get_param("studio_flow_id")
    helper.log_info("studio_flow_id={}".format(studio_flow_id))

    twilio_api_key_sid = helper.get_param("twilio_api_key_sid")
    helper.log_info("twilio_api_key_sid={}".format(twilio_api_key_sid))

    search_result_fields = helper.get_param("search_result_fields")
    helper.log_info("search_result_fields={}".format(search_result_fields))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="twiliostudio:execution")
    helper.addevent("world", sourcetype="twiliostudio:execution")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """
    helper.set_log_level(helper.log_level)
    helper.log_debug("Alert action execute_flow started with log_level: {}".format(helper.log_level))

    #  Sourcetype for messages presented in ARF views, e.g. in ES notables
    arf_msg_sourcetype="twiliostudio:execution"

    splunk_api_callback_host = helper.get_global_setting("splunk_api_callback_host")
    helper.log_debug("API callback host: {}".format(splunk_api_callback_host))
    
    studio_flow_id = helper.get_param("studio_flow_id")
    helper.log_debug("studio_flow_id={}".format(studio_flow_id))

    twilio_api_key_sid = helper.get_param("twilio_api_key_sid")
    helper.log_debug("twilio_api_key_sid={}".format(twilio_api_key_sid))
    
    twilio_creds = helper.get_user_credential(twilio_api_key_sid)

    twilio_client = Client(twilio_creds["username"], twilio_creds["password"])    


    """   Old HTTP REQ Way
    
    # HTTP prep for Twilio
    url = "https://studio.twilio.com/v2/Flows/{}/Executions".format(studio_flow_id)
    
    auth_header_val = base64.b64encode("{}:{}".format(twilio_creds["username"],twilio_creds["password"]).encode('ascii')).decode('ascii')
    
    headers = {}
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Authorization"] = "Basic {}".format(auth_header_val)

    result_field_name = "Parameters"
    """

    mandatory_field_prefix = "@"
    mandatory_field_names  = ["@To","@From"]
    search_result_fields = helper.get_param("search_result_fields").split(',')

    for search_result in helper.get_events():

        body = {}
        flow_parameters = {}

        # Set the Twilio mandatory "envelope" fields
        for field_name in mandatory_field_names:
            body_field_name = field_name.lstrip(mandatory_field_prefix)        
            if search_result.get(field_name):
                body[body_field_name] = search_result.get(field_name)
            else:
                err_msg = "Mandatory field {} not found".format(field_name)
                raise Exception(err_msg)

        ## Add properties to the flow's parameters argument
        # Server name (in case a callback is needed)
        flow_parameters["splunk_api_base"] = splunk_api_callback_host
        
        # from the search context.  
        for field_name in ["search_name","sid","rid","server_uri"]:
            # Allow the search result to override the native  (helps with testing, if nothing else....)
            if search_result.get(field_name):
                flow_parameters[field_name] = search_result.get(field_name)
            else:
                flow_parameters[field_name] = helper.settings[field_name]
        
        # From the action config's list of fields
        for field_name in search_result_fields:
            field_name = field_name.strip()
            if search_result.get(field_name):
                flow_parameters[field_name] = search_result.get(field_name)
            else:
                err_msg = "Configured field {} not found".format(field_name)
                raise Exception(err_msg)

        """   Old HTTP REQ Way
        # Put the "data" fields into the <result_field_name> field as a string-ified JSON
        body[result_field_name] = json.dumps(flow_parameters)
        
        encoded_data = urlencode(body).encode("utf-8")

        req = Request(url, encoded_data, headers)
        urlopen(req).read()
        """

        try:
            execution = twilio_client.studio.v2.flows(studio_flow_id).executions \
                        .create(to=body["To"], \
                                from_=body["From"], \
                                parameters=flow_parameters)

            em = "Message queued for delivery to {}.  Execution {}" \
                        .format(execution.contact_channel_address,execution.sid)

        except TwilioRestException as tre:
            if(tre.status == 409 and tre.details["conflicting_execution_sid"]):    
                # Handle duplicate executions gracefully
                em = "Existing flow active.  No new flow execution created.  See existing execution {}" \
                            .format(tre.details["conflicting_execution_sid"])
                helper.addevent(sourcetype=arf_msg_sourcetype, event_message=em)
            else:
                # Try to instrument the others a bit better
                em = "Unexpected REST exception from Twilio.   See index=cim_modactions for additional details."
                helper.log_error(vars(tre))
                raise tre

        except:
            em = "Exception raised by action.   See index=cim_modactions for additional details."
            raise

        finally:
            helper.addevent(em, sourcetype=arf_msg_sourcetype)
            helper.writeevents(index="summary", host="localhost", source="localhost")
            
    return 0
