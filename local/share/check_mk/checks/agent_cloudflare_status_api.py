#!/usr/bin/env python3

#Function get params (in this case is URL, passed via WATO rule cunfiguration, hostname and ip addres of host,
#for which agent will be invoked
def agent_cloudflare_status_api_arguments(params, hostname, ipaddress):
    args = []
    _url = params['url']
    if _url:
       args += ['-u',_url]
    return args

#register invoke function for our agent
#key value for this dictionary is name part from register datasource of our agent (name="special_agents:myspecial" remember?)
special_agent_info["cloudflare_status_api"] = agent_cloudflare_status_api_arguments
