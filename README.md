# Setup (global)
Add Twilio credential in the Add-On's configuration page. Account name can be anything you want.  Username must be the Twilio API SID,  password is the API secret.

# Setup (action)
- Specify the Twilio Studio Flow to invoke
- Specify the Username/API SID (saved in app-level config)
- Specify the result field(s) to send to Twilio (the fields can then be used in the Twilio flow)
- Specify any additional static fields to send.  Format these fields as JSON.

- Optional:  In some cases (Splunk ES searches over notables),  you may want to provide the "original" sid and rid in the search result, so that you can point back to the original correlation search, not the search for the notable/risk event.  In this case,  include sid and rid as fields in your list (to send to Twilio) and include something like this in the action search

| rename orig_* as *
| table sid rid  <OTHER FIELDS>

# Troubleshooting 

Error status and return code of the script

```index=_internal action=execute_flow ```

More granular messages (especially if you crank up to DEBUG log level)

```index=cim_modactions  sourcetype="modular_alerts:execute_flow"  action_name=execute_flow```

High-level descriptions that appear in ES:

```index=summary sourcetype = twiliostudio:execution```
