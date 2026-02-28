#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Example output from special agent:
<<<cloudflare_status_api:sep(0)>>>
[
    {
        "id":"57ctn3f2qsyj",
        "name":"Amsterdam, Netherlands - (AMS)",
        "status":"operational",
        "created_at":"2014-10-27T20:35:05.259Z",
        "updated_at":"2026-01-21T16:28:37.642Z",
        "position":1,
        "description":null,
        "showcase":false,
        "start_date":null,
        "group_id":"zqxhg7y54vy8",
        "page_id":"yh6f0r4529hb",
        "group":false,
        "only_show_if_degraded":false
    },{
        "id":"1km35smx8p41",
        "name":"Cloudflare Sites and Services",
        "status":"operational",
        "created_at":"2014-10-27T21:59:30.264Z",
        "updated_at":"2020-11-11T20:12:30.167Z",
        "position":1,
        "description":"Sites and services that Cloudflare customers use to interact with the Cloudflare Network and its provided services",
        "showcase":false,
        "start_date":null,
        "group_id":null,
        "page_id":"yh6f0r4529hb",
        "group":true,
        "only_show_if_degraded":false,
        "components":[
            "0hs0rl6hzmvx","w4k8yvhfb3vp","0311l882p558","c9mqrzw6nzvg",
            "xm3cq0t85y10","4c231tkdlpcl","g4tb35rs9yw7","g9yx473yjk9t",
            "g9dgngpcdt1x","3zswxmh2g8j9","lmcb8422fw7b","z9w398bsjvnq",
            "2469qcw8rvjp","dp8ppfycqxcs","ll1x88wwz4fq","ct59b581pxt8",
            "4msl4k5wdcbv","q0dfbn0p6hyt","q9p27cmrspf8","s0991jwsqllx",
            "jm1y487rf7p3","3q1jnbdbn845","5wnz34mhfhrk","fbvx0hxhhdj0",
        ]
    }
]
"""
from cmk.agent_based.v2 import AgentSection, CheckPlugin, IgnoreResultsError, Result, Service, State
from cmk.agent_based.v2 import CheckResult, DiscoveryResult
import json


def parse_cloudflare_status_api(string_table):
    return json.loads(string_table[0])


agent_section_cloudflare_status_api = AgentSection(
    name="cloudflare_status_api",
    parse_function=parse_cloudflare_status_api,
)


def discover_cloudflare_status_api(section) -> DiscoveryResult:
    if section is None:
        return
    else:
        for site in section:
            # filter for the group or site and yield name as the item.
            if site["group_id"] == "1km35smx8p41" or site["group"]:
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
                detail = None
                if site.get("components"):
                    detail = f"{output} subcomponent-status:\n"
                    # iterate through the subcomponents of the site and 
                    # add them as details if they exist.
                    for subcomponent in site["components"]:
                        res = list(filter(
                            lambda s: s["id"] == subcomponent,
                            section
                        ))
                        detail += f'{res[0]["name"]}-{res[0]["status"]}\\n'
                # Results if operational            
                if site["status"] == "operational":
                    yield Result(
                       state=State.OK,
                       summary=f"{output} is fully operational.",
                       details=detail,
                    )
                # results if partial outage
                elif site["status"] == "partial_outage":
                    yield Result(
                       state=State.WARN,
                       summary=f"{output} is in a partial outage.",
                       details=detail,
                    )
                # results if degraded
                elif site["status"] == "degraded_performance":
                    yield Result(
                       state=State.WARN,
                       summary=f"{output} is experiencing degraded performance.",
                       details=detail,
                    )
                # anything currently not observed in status
                # outage or other status.
                else:
                    yield Result(
                       state=State.CRIT,
                       summary=f"{output} is in an unidentified or"
                               " critical state.",
                       details=detail,
                    )


check_plugin_cloudflare_status_api = CheckPlugin(
    name="cloudflare_status_api",
    service_name="Cloudflare Service %s",
    discovery_function=discover_cloudflare_status_api,
    check_function=check_cloudflare_status_api,
)
