#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from collections.abc import Iterator
from pydantic import BaseModel
from cmk.server_side_calls.v1 import (
    HostConfig,
    noop_parser,
    SpecialAgentConfig,
    SpecialAgentCommand
)

class Params(BaseModel):
    url: str | None = "www.cloudflarestatus.com"

def _agent_cloudflare_status_api_arguments(
    params: Params,
    host_config: HostConfig
    ) -> Iterator[SpecialAgentCommand]:
    args = []
    if params['url']:
       args += ['-u', params['url']]
    yield SpecialAgentCommand(command_arguments=args)

#register invoke function for our agent
#key value for this dictionary is name part from register datasource of our agent (name="special_agents:myspecial" remember?)
special_agent_cloudflare_status_api=SpecialAgentConfig(
    name="cloudflare_status_api",
    parameter_parser=noop_parser,
    commands_function=_agent_cloudflare_status_api_arguments
)
