# Cloudflare Status API

A custom plugin 'Special Agent' for CheckMK to query the publicly available www.cloudflarestatus.com API and retrieve services and report on their state.

For usage
1. Create a dummy host (or skip to #3 if you want these checks to show under an existing host).
2. Set the host configuration as:
    * IP address family - No IP
    * Checkmk agent / API integrations - Configured API Integrations, no Checkmk agent
    * SNMP - No SNMP
3. Setup a rule under "VM, cloud, container > Cloudflare Status API" associated to the dummy host.
    * The URL should be pre-filled but can be overriden (in case of future changes)
    * Add your dummy host to the explicit hosts list.
4. (Optional) Setup a rule under "VM, cloud, container > Cloudflare Status API discovery" to control how services are discovered:
    * **Grouping enabled** (the default) - regional groups (Europe, Asia, Africa, North America, etc.) are discovered as one service each, with their individual datacenters listed only in that service's details. Members of the flat "Cloudflare Sites and Services" catch-all group (Access, API, Analytics, etc.) are discovered individually since there's no further grouping for them.
    * **Grouping disabled** - every component is discovered individually. Optionally add name filters (case-insensitive substring match against the component name) to limit discovery to only matching components; leave the filter list empty to discover everything individually.
5. Perform a Service Discovery on your desired host.
6. Choose which services to ignore or monitor.
7. Activate your changes.

## How it works

The special agent (`libexec/agent_cloudflare_status_api`) queries `https://<url>/api/v2/components.json` and outputs the components list as compact JSON under the `<<<cloudflare_status_api:sep(0)>>>` section header.

The check plugin (`agent_based/cloudflare_status_api.py`) parses the JSON and, per the "Cloudflare Status API discovery" ruleset, discovers services either as:
- **Grouping enabled** (default): one service per top-level regional group, plus one service per direct member of the "Cloudflare Sites and Services" catch-all group (group ID `1km35smx8p41`) - since that group has no further logical sub-grouping.
- **Grouping disabled**: one service per component, optionally restricted to components matching a configured name filter.

A group service's details list only its non-operational subcomponents (plus an "N/M operational" count), to avoid exceeding Checkmk's long-output size limit.

TO DO:  
* Consolidate yield statements
* Is a URL necessary since it defaults and isn't part of the check, only the script to pull data.