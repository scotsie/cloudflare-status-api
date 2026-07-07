#!/bin/bash
# Checkmk >= 2.5 snapshots local/ on every config activation and, for any
# symlink pointing outside the site, copies the target in place with
# shutil.copy2() (see cmk/base/core/interface/_snapshot_local_dir.py). That
# only supports files, so a symlink straight to one of this repo's
# directories (which live outside the site, under $WORKSPACE) crashes
# activation with "IsADirectoryError: Is a directory". Mirror the workspace
# as real local directories containing per-file symlinks instead, so every
# leaf symlink Checkmk touches resolves to a file.
link_tree() {
    local src="$1" dst="$2"
    rm -rf "$dst"
    [ -d "$src" ] || return 0
    mkdir -p "$dst"
    (cd "$src" && find . -type f -not -path '*/__pycache__/*') | while read -r rel; do
        mkdir -p "$dst/$(dirname "$rel")"
        ln -sfv "$src/$rel" "$dst/$rel"
    done
}

PKGNAME=$(python3 -c 'print(eval(open("package.manifest").read())["name"])')
PLUGIN_DIR=$OMD_ROOT/local/lib/python3/cmk_addons/plugins/$PKGNAME

rm -rf $PLUGIN_DIR
mkdir -p $PLUGIN_DIR
for DIR in 'agent_based' 'bakery' 'checkman' 'graphing' 'inventory_ui' 'libexec' 'rulesets' 'server_side_calls'; do
    link_tree "$WORKSPACE/$DIR" "$PLUGIN_DIR/$DIR"
done

link_tree "$WORKSPACE/nagios_plugins" "$OMD_ROOT/local/lib/nagios/plugins"

# Third-party bakery plug-ins written against the stable v1 API
# (cmk.base.plugins.bakery.bakery_api.v1) are loaded from this legacy
# namespace, not from cmk_addons/plugins/<pkg>/bakery — that path is only
# scanned for the newer, still-unstable v2 bakery API. See
# cmk/base/api/bakery/register.py:get_bakery_plugins().
link_tree "$WORKSPACE/bakery" "$OMD_ROOT/local/lib/python3/cmk/base/cee/plugins/bakery"

# Legacy plug-in dirs (pre cmk_addons_plugins packaging), still read from
# cmk.utils.paths: pre agent_based check plug-ins, raw agent scripts,
# notification/inventory scripts, PNP graph templates, and legacy GUI
# extensions (web/plugins/...). Only relevant for repos that still ship
# these; harmless no-op via link_tree if the source dir doesn't exist.
for DIR in 'agents' 'checks' 'inventory' 'notifications' 'pnp-templates' 'web'; do
    link_tree "$WORKSPACE/$DIR" "$OMD_ROOT/local/share/check_mk/$DIR"
done

# cmk.utils.paths.doc_dir is "share/doc/check_mk", not "share/check_mk/doc".
link_tree "$WORKSPACE/doc" "$OMD_ROOT/local/share/doc/check_mk"
