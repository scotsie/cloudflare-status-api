#!/usr/bin/env python3

from cmk.server_side_calls.v1 import noop_parser, SpecialAgentConfig, SpecialAgentCommand


#Function get params (in this case is URL, passed via WATO rule cunfiguration, hostname and ip addres of host,
#for which agent will be invoked
def agent_cloudflare_status_api_arguments(params):
    args = []
    _url = params['url']
    if _url:
       args += ['-u',_url]
    yield SpecialAgentCommand(command_arguments=args)

#register invoke function for our agent
#key value for this dictionary is name part from register datasource of our agent (name="special_agents:myspecial" remember?)
special_agent_cloudflare_status_api= SpecialAgentConfig(
    name="cloudflare_status_api",
    parameter_parser=noop_parser,
    commands_function=agent_cloudflare_status_api_arguments
)
