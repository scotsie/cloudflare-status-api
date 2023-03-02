#!/usr/bin/python

#import required to register agent
import cmk.gui.watolib as watolib
from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
)
from cmk.gui.valuespec import (
    TextAscii,
)

#import structure where special agent will be registered
from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourcePrograms

#Some WATO form definition, to ask user for port number
def _valuespec_cloudflare_status_api():
    return Dictionary(
        title=_("Cloudflare API Component Checks"),
        help=_("This agent will query the Cloudflare status API and provide a list of parent services or groups of services."),
        optional_keys=["url"],
        elements=[
            ("url",
            TextAscii(
                title=_("URL"),
                help=_("URL for the API Call. Defaults to www.cloudflarestatus.com."),
                allow_empty=False,
                default_value="www.cloudflarestatus.com",
                )
            ),
        ],
    )


#In that piece of code we registering Special Agent
rulespec_registry.register(
    (
        HostRulespec(
            group=RulespecGroupDatasourcePrograms,
            name="special_agents:cloudflare_status_api",
            valuespec=_valuespec_cloudflare_status_api,
        )
    )
)
