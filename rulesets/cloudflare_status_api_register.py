#!/usr/bin/env python3

from cmk.rulesets.v1.form_specs import Dictionary, DictElement, String, Prefill
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic, Help, Title

#import required to register agent
#import cmk.gui.watolib as watolib
#from cmk.gui.i18n import _
#from cmk.gui.plugins.wato import (
#    rulespec_registry,
#    HostRulespec,
#)
#from cmk.gui.valuespec import (
#    TextAscii,
#)

#import structure where special agent will be registered
#from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourcePrograms

#Some WATO form definition, to ask user for port number
def _valuespec_cloudflare_status_api():
    return Dictionary(
        title=Title("Cloudflare API Component Checks"),
        help_text=Help("This agent will query the Cloudflare status API and provide a list of parent services or groups of services."),
        #optional_keys=["url"],
        elements={
            "url": DictElement(
                required=False,
                parameter_form=String(
                    title=Title("URL"),
                    help_text=Help("URL for the API Call. Defaults to www.cloudflarestatus.com."),
                    prefill=Prefill("www.cloudflarestatus.com"),
                )
            ),
        },
    )


#In that piece of code we registering Special Agent
rule_spec_cloudflare_status_api = SpecialAgent(
    topic=Topic.CLOUD,
    name="cloudflare_status_api",
    title=Title("Cloudflare Status API"),
    parameter_form=_valuespec_cloudflare_status_api
)