#!/usr/bin/env python3

from cmk.rulesets.v1.form_specs import Dictionary, DictElement, String, DefaultValue
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic, Help, Title

def _formspec_cloudflare_status_api():
    return Dictionary(
        title=Title("Cloudflare Status API"),
        help_text=Help("This agent will query the Cloudflare status API and provide a list of parent services or groups of services."),
        elements={
            "url": DictElement(
                parameter_form=String(
                    title=Title("URL"),
                    help_text=Help("URL for the API Call. Should normally be www.cloudflarestatus.com."),
                    prefill=DefaultValue("www.cloudflarestatus.com")
                ),
                required=True,
            ),
        },
    )

rule_spec_cloudflare_status_api = SpecialAgent(
    topic=Topic.CLOUD,
    name="cloudflare_status_api",
    title=Title("Cloudflare Status API"),
    parameter_form=_formspec_cloudflare_status_api
)