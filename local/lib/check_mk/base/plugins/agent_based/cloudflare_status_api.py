#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Example output from special agent:
<<<cloudflare_status_api>>>
id name status group_id group components(if any)
38w9dn5m8n4p Tianjin,_China_-_(TSN) operational 77867vxkttgw False None

Example of string_table input for parsing
[['38w9dn5m8n4p','Tianjin,_China_-_(TSN)','operational','77867vxkttgw','False','None'],]

Example of data after parsing
[{'components': 'None',
  'group': 'False',
  'group_id': '77867vxkttgw',
  'id': '38w9dn5m8n4p',
  'name': 'Tianjin, China - (TSN)',
  'status': 'operational'}]
"""

from .agent_based_api.v1 import IgnoreResultsError, register, Result, Service, State
from .agent_based_api.v1.type_defs import CheckResult, DiscoveryResult
import pprint

def parse_cloudflare_status_api(string_table):
    parsed = []
    for site in string_table:
        site_dict = {}
        site_dict["id"] = site[0]
        site_dict["name"] = modify_strings(site[1])
        site_dict["status"] = site[2]
        site_dict["group_id"] = site[3]
        site_dict["group"] = site[4]
        site_dict["components"] = site[5]
        parsed.append(site_dict)
    return parsed


register.agent_section(
    name = "cloudflare_status_api",
    parse_function = parse_cloudflare_status_api,
)


def modify_strings(data):
    if isinstance(data, str):
        mod_data = data.replace("!", "’")
        return mod_data.replace("_"," ")
    else:
        return data


def discover_cloudflare_status_api(section) -> DiscoveryResult:
    if section is None:
        return
    else:
        for site in section:
            # filter for the group or site and yield name as the item.
            if site["group_id"] == "1km35smx8p41" or site["group"] == 'True':
                yield Service(item=site["name"])


def check_cloudflare_status_api(item, section) -> CheckResult:
    # Notify if empty section input
    if section is None:
        raise IgnoreResultsError("No API status data returned.")

    # Filter on the item passed and exit_code
    else:
        for site in section:
            if site["name"] == item:
                output = f'{site["name"]}'
                if site["status"] == "operational":
                    yield Result(
                       state = State.OK,
                       summary = f"{output} is fully operational.",
                       details = "detailed\nmultiline\noutput."
                    )
                elif site["status"] == "partial_outage":
                    yield Result(
                       state = State.WARN,
                       summary = f"{output} is in a partial outage.",
                       details = "detailed\nmultiline\noutput."
                    )
                elif site["status"] == "degraded_performance":
                    yield Result(
                       state = State.WARN,
                       summary = f"{output} is experiencing degraded performance.",
                       details = "detailed\nmultiline\noutput."
                    )
                else:
                    yield Result(
                       state = State.CRIT,
                       summary = f"{output} is in an unidentified or critical state.",
                       details = "detailed\nmultiline\noutput."
                    )


register.check_plugin(
    name = "cloudflare_status_api",
    service_name = "Cloudflare Service %s",
    discovery_function = discover_cloudflare_status_api,
    check_function = check_cloudflare_status_api,
)
