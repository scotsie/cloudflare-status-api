#!/usr/bin/env python3

from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice, CascadingSingleChoiceElement,
    Dictionary, DictElement, DefaultValue, FixedValue, List, String,
)
from cmk.rulesets.v1.rule_specs import (
    SpecialAgent, DiscoveryParameters, Topic, Help, Title
)


def _formspec_cloudflare_status_api():
    return Dictionary(
        title=Title("Cloudflare Status API"),
        help_text=Help(
            "This agent will query the Cloudflare status API and provide "
            "a list of parent services or groups of services."
        ),
        elements={
            "url": DictElement(
                parameter_form=String(
                    title=Title("URL"),
                    help_text=Help(
                        "URL for the API Call. Should normally be "
                        "www.cloudflarestatus.com."
                    ),
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


def _formspec_cloudflare_status_api_discovery():
    name_filter = List(
        element_template=String(title=Title("Name filter")),
        title=Title(
            "Filter by name (case-insensitive substring match against "
            "the API component name; leave empty to discover every "
            "component individually)"
        ),
        help_text=Help(
            "A bare 3-letter airport code can match unrelated words, e.g. "
            "'fra' also matches 'France' and 'Infrastructure'. Include the "
            "parentheses, e.g. '(FRA)', or use the full city name to avoid "
            "unintended matches."
        ),
    )
    grouping_choice = CascadingSingleChoice(
        title=Title("Datacenter grouping"),
        prefill=DefaultValue("enabled"),
        elements=[
            CascadingSingleChoiceElement(
                name="enabled",
                title=Title("Grouping enabled"),
                parameter_form=FixedValue(value=None),
            ),
            CascadingSingleChoiceElement(
                name="disabled",
                title=Title("Grouping disabled"),
                parameter_form=name_filter,
            ),
        ],
    )
    return Dictionary(
        title=Title("Cloudflare datacenter discovery"),
        help_text=Help(
            "Controls whether Cloudflare status components are discovered "
            "as grouped roll-up services (e.g. one 'Europe' service "
            "covering all its datacenters) or as individual services."
        ),
        elements={
            "grouping": DictElement(
                parameter_form=grouping_choice,
                required=True,
            ),
        },
    )


rule_spec_cloudflare_status_api_discovery = DiscoveryParameters(
    name="cloudflare_status_api_discovery",
    title=Title("Cloudflare Status API discovery"),
    topic=Topic.CLOUD,
    parameter_form=_formspec_cloudflare_status_api_discovery,
)
