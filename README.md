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
4. Perform a Service Discovery on your desired host.
5. Choose which services to ignore or monitor.
6. Commit your changes.

TO DO:  
* Swap to using JSON output on data query (didn't know it support it originally)
* Consolidate yield statements
* More meaningful webui options?
* Is a URL necessary since it defaults and isn't part of the check, only the script to pull data.