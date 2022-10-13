import base64
import json

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from splunk.clilib import cli_common as cli


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

    static_fields_json = helper.get_param("static_fields_json")
    helper.log_info("static_fields_json={}".format(static_fields_json))


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

    #  Sourcetype for messages presented in ARF views, e.g. in ES notables
    arf_msg_sourcetype="twiliostudio:execution"

    helper.set_log_level(helper.log_level)
    helper.log_debug("Alert action execute_flow started with log_level: {}".format(helper.log_level))
    

    #  Get the Splunk server name for use in Twilio callbacks
    alert_actions_config = cli.getMergedConf("alert_actions")
    alert_actions_hostname = alert_actions_config.get("email", {}).get("hostname", None)
    if alert_actions_hostname:
        helper.log_debug("Retrieved alert action hostname from server config: {}".format(alert_actions_hostname))

    if helper.get_global_setting("splunk_api_callback_host"):
        splunk_api_callback_host = helper.get_global_setting("splunk_api_callback_host")
    else:
        splunk_api_callback_host = "{}:8089".format(alert_actions_hostname)
        
    helper.log_debug("API callback host: {}".format(splunk_api_callback_host))
    
    studio_flow_id = helper.get_param("studio_flow_id")
    helper.log_debug("studio_flow_id={}".format(studio_flow_id))

    twilio_api_key_sid = helper.get_param("twilio_api_key_sid")
    helper.log_debug("twilio_api_key_sid={}".format(twilio_api_key_sid))
    
    twilio_creds = helper.get_user_credential(twilio_api_key_sid)
    twilio_client = Client(twilio_creds["username"], twilio_creds["password"])    

    mandatory_field_prefix = "@"
    mandatory_field_names  = ["@To","@From"]
    
    search_result_fields = []
    if helper.get_param("search_result_fields"):
        search_result_fields = helper.get_param("search_result_fields").split(',')
    
    static_vals = {}
    if helper.get_param("static_fields_json"):
        try:
            static_vals = json.loads(helper.get_param("static_fields_json"))
        except Exception as e:
            helper.log_error("Error parsing static JSON: {}".format(e))
            raise e

    for search_result in helper.get_events():

        body = {}
        flow_parameters = {}

        ## Add properties to the flow's parameters argument

        # Add server name (in case a callback is needed)
        flow_parameters["splunk_api_base"] = splunk_api_callback_host
        
        # Add the search context.  
        for field_name in ["search_name","sid","rid"]:
            # Allow the search result to override the native  (helps with testing, if nothing else....)
            if search_result.get(field_name):
                flow_parameters[field_name] = search_result.get(field_name)
            else:
                flow_parameters[field_name] = helper.settings[field_name]


        # Add the search result fields listed in the action config
        for field_name in search_result_fields:
            field_name = field_name.strip()
            if search_result.get(field_name):
                flow_parameters[field_name] = search_result.get(field_name)
            else:
                err_msg = "Configured field \"{}\" not found".format(field_name)
                helper.log_error(err_msg)
                raise Exception(err_msg)

        # Add the user-specified static fields+values 
        for k in static_vals.keys():
            # Will add the body/envelope further down if this is a mandatory param
            if k not in mandatory_field_names:
                flow_parameters[k] = static_vals.get(k)
            
        helper.log_debug("Parameters to send: {}".format(flow_parameters))

        ## Add the Twilio mandatory "envelope" fields
        for field_name in mandatory_field_names:
            body_field_name = field_name.lstrip(mandatory_field_prefix)        
            if static_vals.get(field_name):
                body[body_field_name] = static_vals.get(field_name)
            elif search_result.get(field_name):
                body[body_field_name] = search_result.get(field_name)
            else:
                err_msg = "Mandatory field {} not found".format(field_name)
                raise Exception(err_msg)

        ## Send the request to Twilio
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
                helper.log_info(em)
                helper.addevent(em, sourcetype=arf_msg_sourcetype)
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

