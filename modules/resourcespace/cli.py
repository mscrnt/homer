#!/usr/bin/env python3



import click
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger

# API function imports
from modules.resourcespace.api_functions import (
    resource, collection, metadata, system, user, message, search
)

log = get_module_logger("resourcespace")

@register_cli("resourcespace")
@click.group(
    help="📁 HOMER ResourceSpace CLI — Digital Asset Management Tools",
    context_settings={"help_option_names": ["-h", "--help"]}
)
def cli():
    pass

# ──────────────────────────────────────────────────────────────────────────────
# RESOURCE COMMANDS
# ──────────────────────────────────────────────────────────────────────────────

@cli.group(
    name="resource",
    help=(
        "📦 Resource commands — Create, update, upload, and manage individual resources.\n\n"
        "Includes:\n"
        "• Create or delete a resource\n"
        "• Upload files or preview images\n"
        "• Fetch metadata or logs\n"
        "• Replace files or manage relationships"
    )
)
def resource_cmd():
    """Grouped commands for managing ResourceSpace resources."""
    pass

@resource_cmd.command("get-resource-info", help="Get top-level property data for a resource.")
@click.option("--id", required=True, type=int, help="Resource ID")
def get_resource_info(id):
    log.info(resource.get_resource_data(id))

@resource_cmd.command("get-resource-metadata", help="Get full metadata (field data) for a resource.")
@click.option("--id", required=True, type=int, help="Resource ID")
def get_resource_metadata(id):
    log.info(resource.get_resource_field_data(id))

@resource_cmd.command("create-resource", help="Create a new resource of the specified type.")
@click.option("--type", "resource_type", required=True, type=int, help="Resource type ID")
@click.option("--archive", default=999, type=int, help="Archive state (e.g. 0=Live, 1=Pending Archive, 2=Archived)")
def create_resource(resource_type, archive):
    log.info(resource.create_resource(resource_type=resource_type, archive=archive))

@resource_cmd.command("delete-resource", help="Delete a resource by ID.")
@click.option("--id", required=True, type=int, help="Resource ID")
def delete_resource(id):
    log.info(resource.delete_resource(id))

@resource_cmd.command("upload-resource-by-url", help="Upload a resource file using a remote URL.")
@click.option("--id", required=True, type=int, help="Resource ID")
@click.option("--url", required=True, help="Remote file URL to upload")
def upload_resource_by_url(id, url):
    log.info(resource.upload_file_by_url(id, url))

@resource_cmd.command("upload-resource-file", help="Upload a local file to the resource.")
@click.option("--id", required=True, type=int, help="Resource ID")
@click.option("--file", "file_path", required=True, type=click.Path(exists=True), help="Path to local file")
def upload_resource_file(id, file_path):
    log.info(resource.upload_file(id, file_path))

@resource_cmd.command("upload-resource-preview", help="Upload a JPG preview image for a resource.")
@click.option("--id", required=True, type=int, help="Resource ID")
@click.option("--file", "file_path", required=True, type=click.Path(exists=True), help="Path to JPG preview image")
def upload_resource_preview(id, file_path):
    log.info(resource.upload_multipart(id, file_path=file_path, previewonly=True))

# ──────────────────────────────────────────────────────────────────────────────
# COLLECTION COMMANDS
# ──────────────────────────────────────────────────────────────────────────────

@cli.group(
    name="collection",
    help=(
        "📚 Collection commands — Manage ResourceSpace collections and resources within them.\n\n"
        "Includes:\n"
        "• Create, delete, and list collections\n"
        "• Add/remove resources from collections\n"
        "• Search public or featured collections"
    )
)
def collection_cmd():
    """Grouped commands for managing collections in ResourceSpace."""
    pass

@collection_cmd.command("get-user-collections", help="List all collections for the current user.")
def get_user_collections():
    log.info(collection.get_user_collections())

@collection_cmd.command("create-collection", help="Create a new collection for the current user.")
@click.option("--name", required=True, help="Name of the new collection")
@click.option("--forupload", is_flag=True, default=False, help="Mark collection for upload context")
def create_collection(name, forupload):
    log.info(collection.create_collection(name, int(forupload)))

@collection_cmd.command("delete-collection", help="Delete a collection by ID.")
@click.option("--id", "collection_id", required=True, type=int, help="Collection ID")
def delete_collection(collection_id):
    log.info(collection.delete_collection(collection_id))

@collection_cmd.command("add-resource-to-collection", help="Add a resource to a specific collection.")
@click.option("--resource-id", required=True, type=int, help="Resource ID to add")
@click.option("--collection-id", required=True, type=int, help="Collection ID to add the resource to")
def add_resource_to_collection(resource_id, collection_id):
    log.info(collection.add_resource_to_collection(resource_id, collection_id))

@collection_cmd.command("remove-resource-from-collection", help="Remove a resource from a specific collection.")
@click.option("--resource-id", required=True, type=int, help="Resource ID to remove")
@click.option("--collection-id", required=True, type=int, help="Collection ID to remove from")
def remove_resource_from_collection(resource_id, collection_id):
    log.info(collection.remove_resource_from_collection(resource_id, collection_id))

@collection_cmd.command("search-public-collections", help="Search public and featured collections.")
@click.option("--query", default="", help="Search string")
@click.option("--order-by", default="name", help="Order results by field (default: name)")
@click.option("--sort", default="ASC", type=click.Choice(["ASC", "DESC"], case_sensitive=False), help="Sort direction")
@click.option("--exclude-themes", is_flag=True, default=True, help="Exclude featured themes (default: true)")
def search_public_collections(query, order_by, sort, exclude_themes):
    log.info(collection.search_public_collections(query, order_by, sort, int(exclude_themes)))

@collection_cmd.command("get-collection", help="Get details for a specific collection (admin only).")
@click.option("--id", "collection_id", required=True, type=int, help="Collection ID")
def get_collection_details(collection_id):
    log.info(collection.get_collection(collection_id))

@collection_cmd.command("save-collection", help="Save metadata or settings for a collection.")
@click.option("--id", "collection_id", required=True, type=int, help="Collection ID")
@click.option("--data", required=True, help="JSON string of collection metadata to update")
def save_collection(collection_id, data):
    import json
    log.info(collection.save_collection(collection_id, json.loads(data)))

@collection_cmd.command("send-to-admin", help="Send a collection to admin for review.")
@click.option("--id", "collection_id", required=True, type=int, help="Collection ID")
def send_to_admin(collection_id):
    log.info(collection.send_collection_to_admin(collection_id))

@collection_cmd.command("get-featured", help="Get featured collections under a parent category.")
@click.option("--parent-id", default=0, type=int, help="Parent collection ID (default: 0)")
def get_featured_collections(parent_id):
    log.info(collection.get_featured_collections(parent_id))

@collection_cmd.command("delete-all-resources", help="Delete all resources in a collection.")
@click.option("--id", "collection_id", required=True, type=int, help="Collection ID")
def delete_all_resources(collection_id):
    log.info(collection.delete_resources_in_collection(collection_id))

@collection_cmd.command("hide-from-user", help="Hide or show a collection from the user's dropdown.")
@click.option("--id", "collection_id", required=True, type=int, help="Collection ID")
@click.option("--user-id", required=True, type=int, help="User ID to affect")
@click.option("--show", default=1, type=int, help="1 = Show (default), 0 = Hide")
def hide_from_user(collection_id, user_id, show):
    log.info(collection.show_hide_collection(collection_id, show, user_id))



# ──────────────────────────────────────────────────────────────────────────────
# METADATA COMMANDS
# ──────────────────────────────────────────────────────────────────────────────

@cli.group(
    name="metadata",
    help="🏷️ Metadata commands — Manage field options, values, and nodes for resources."
)
def metadata_cmd():
    """Grouped commands for working with metadata fields and values."""
    pass

@metadata_cmd.command("get-field-options", help="Get selectable options for a fixed-list metadata field.")
@click.option("--field-id", required=True, type=int, help="Field ID or shortname")
@click.option("--nodeinfo", is_flag=True, help="Include extended node info (ref, parent, order)")
def get_field_options(field_id, nodeinfo):
    log.info(metadata.get_field_options(field_id, nodeinfo=nodeinfo))

@metadata_cmd.command("get-field-nodes", help="Get all nodes (tags/options) for a field.")
@click.option("--field-id", required=True, type=int, help="Metadata field ID")
def get_field_nodes(field_id):
    log.info(metadata.get_nodes(field_id))

@metadata_cmd.command("get-node-id", help="Look up a node ID by its name and field.")
@click.option("--value", required=True, help="The node label (e.g. 'United States')")
@click.option("--field-id", required=True, type=int, help="Metadata field ID")
def get_node_id(value, field_id):
    log.info(metadata.get_node_id(value, field_id))

@metadata_cmd.command("add-resource-nodes", help="Add fixed-list nodes to a single resource.")
@click.option("--resource-id", required=True, type=int, help="Resource ID")
@click.option("--node-ids", required=True, help="Comma-separated list of node IDs")
def add_resource_nodes(resource_id, node_ids):
    parsed = [int(n.strip()) for n in node_ids.split(",") if n.strip()]
    log.info(metadata.add_resource_nodes(resource_id, parsed))

@metadata_cmd.command("add-resource-nodes-multi", help="Add nodes to multiple resources.")
@click.option("--resource-ids", required=True, help="Comma-separated list of resource IDs")
@click.option("--node-ids", required=True, help="Comma-separated list of node IDs")
def add_resource_nodes_multi(resource_ids, node_ids):
    rids = [int(r.strip()) for r in resource_ids.split(",") if r.strip()]
    nids = [int(n.strip()) for n in node_ids.split(",") if n.strip()]
    log.info(metadata.add_resource_nodes_multi(rids, nids))

@metadata_cmd.command("update-field", help="Set or update a metadata field value for a resource.")
@click.option("--resource-id", required=True, type=int, help="Resource ID")
@click.option("--field-id", required=True, type=int, help="Metadata field ID")
@click.option("--value", required=True, help="Value or node ID(s) for the field")
@click.option("--node-values", is_flag=True, help="Pass node IDs instead of raw string values")
def update_field(resource_id, field_id, value, node_values):
    log.info(metadata.update_field(resource_id, field_id, value, nodevalues=node_values))

@metadata_cmd.command("set-node", help="Create or update a metadata node.")
@click.option("--ref", default="NULL", help="Node ID (or NULL to create new)")
@click.option("--field-id", required=True, type=int, help="Metadata field ID")
@click.option("--name", required=True, help="Node name")
@click.option("--parent", type=int, help="Parent node ID (for category trees)")
@click.option("--order", default=0, type=int, help="Ordering index")
@click.option("--return-existing", is_flag=True, help="Return existing node ID if it already exists")
def set_node(ref, field_id, name, parent, order, return_existing):
    ref_val = None if ref == "NULL" else int(ref)
    log.info(metadata.set_node(ref_val, field_id, name, parent, order_by=order, returnexisting=return_existing))

@metadata_cmd.command("get-resource-type-fields", help="List metadata fields for resource types (admin only).")
@click.option("--types", default="", help="Comma-separated resource type IDs")
@click.option("--filter", default="", help="Fuzzy filter by name, title, help, etc.")
@click.option("--field-types", default="", help="Filter by field types (CSV of FIELD_TYPE_* values)")
def get_resource_type_fields(types, filter, field_types):
    log.info(metadata.get_resource_type_fields(types, filter, field_types))

@metadata_cmd.command("create-field", help="Create a new metadata field (admin only).")
@click.option("--name", required=True, help="Field internal name")
@click.option("--resource-types", default="0", help="CSV of resource types or 0 for global")
@click.option("--type", "field_type", required=True, type=int, help="Field type ID (e.g. 1 = text)")
def create_field(name, resource_types, field_type):
    log.info(metadata.create_resource_type_field(name, resource_types, field_type))

@metadata_cmd.command("toggle-node-active", help="Toggle visibility state of nodes (enable/disable).")
@click.option("--node-ids", required=True, help="Comma-separated list of node IDs to toggle")
def toggle_node_active(node_ids):
    parsed = [int(n.strip()) for n in node_ids.split(",") if n.strip()]
    log.info(metadata.toggle_active_state_for_nodes(parsed))


# ──────────────────────────────────────────────────────────────────────────────
# SYSTEM COMMANDS
# ──────────────────────────────────────────────────────────────────────────────

@cli.group(
    name="system",
    help="🖥️ System commands — Diagnostics, status checks, and usage statistics."
)
def system_cmd():
    """System monitoring, health status, and daily usage summaries."""
    pass

@system_cmd.command("get-system-status", help="Check ResourceSpace system health (e.g. quota, cron, plugins).")
def get_system_status():
    """Show high-level system status and alerts."""
    log.info(system.get_system_status())

@system_cmd.command("get-daily-stats", help="Get summary of activity stats over the last N days (max 365).")
@click.option("--days", default=30, show_default=True, type=int, help="Number of days to summarize")
def get_daily_stats(days):
    """Return summary stats for views, uploads, deletions, etc."""
    log.info(system.get_daily_stat_summary(days))


# ──────────────────────────────────────────────────────────────────────────────
# USER COMMANDS
# ──────────────────────────────────────────────────────────────────────────────

@cli.group(
    name="user",
    help="👤 User commands — Query, authenticate, and check permissions."
)
def user_cmd():
    """User-related operations such as login, lookup, and permission checks."""
    pass

@user_cmd.command("get-users", help="List users (optionally filter by username).")
@click.option("--find", default="", help="Search string for partial username match.")
@click.option("--exact", is_flag=True, help="Match exact username.")
def get_users(find, exact):
    log.info(user.get_users(find=find, exact_username_match=exact))

@user_cmd.command("get-users-by-permission", help="List users who have a specific permission.")
@click.option("--perm", "perms", multiple=True, required=True, help="Permission string (use multiple for AND match).")
def get_users_by_permission(perms):
    log.info(user.get_users_by_permission(list(perms)))

@user_cmd.command("check-permission", help="Check if current user has the specified permission.")
@click.option("--perm", required=True, help="Permission string to check (e.g. 'a', 'c', etc.)")
def check_permission(perm):
    log.info(user.checkperm(perm))

@user_cmd.command("login", help="Authenticate with username and password.")
@click.option("--username", required=True, help="Username for login.")
@click.option("--password", required=True, help="Password for login.")
def user_login(username, password):
    log.info(user.login(username, password))

@user_cmd.command("mark-email-invalid", help="Mark an email address as invalid to prevent sending.")
@click.option("--email", required=True, help="Email address to flag.")
def mark_email_invalid(email):
    log.info(user.mark_email_as_invalid(email))

# ──────────────────────────────────────────────────────────────────────────────
# MESSAGE COMMANDS
# ──────────────────────────────────────────────────────────────────────────────

@cli.group(
    name="message",
    help="📨 Message commands — View ResourceSpace messages."
)
def message_cmd():
    """Commands for viewing messages addressed to the current user."""
    pass

@message_cmd.command("get-user-message", help="Retrieve a message by ID (if accessible).")
@click.option("--id", "message_id", required=True, type=int, help="Message ID to retrieve.")
def get_user_message(message_id):
    log.info(message.get_user_message(message_id))


# ──────────────────────────────────────────────────────────────────────────────
# SEARCH COMMANDS
# ──────────────────────────────────────────────────────────────────────────────

@cli.group(
    name="search",
    help="🔍 Search commands — Query and preview resources."
)
def search_cmd():
    """Perform resource searches and retrieve result previews."""
    pass

@search_cmd.command("search-resources", help="Perform a resource search using the given query.")
@click.option("--query", required=True, help="Search string in standard ResourceSpace format.")
@click.option("--restypes", default="", help="Comma-separated list of resource type IDs.")
@click.option("--order-by", default="relevance", help="Sort field (e.g. relevance, date, title).")
@click.option("--archive", default="0", help="Archive status to filter (e.g. 0 = live).")
@click.option("--fetchrows", default="-1", help="Number of rows to return or offset,limit.")
@click.option("--sort", default="desc", help="Sort direction: asc or desc.")
@click.option("--offset", default=0, type=int, help="Offset for paginated search results.")
def search_resources(query, restypes, order_by, archive, fetchrows, sort, offset):
    log.info(search.do_search(query, restypes, order_by, archive, fetchrows, sort, offset))

@search_cmd.command("search-resources-with-previews", help="Search resources and include preview image URLs.")
@click.option("--query", required=True, help="Search string in standard ResourceSpace format.")
@click.option("--sizes", default="scr", help="Comma-separated preview sizes (e.g. thm,scr,pre).")
@click.option("--restypes", default="", help="Comma-separated list of resource type IDs.")
@click.option("--order-by", default="relevance", help="Sort field (e.g. relevance, date).")
@click.option("--archive", default=0, type=int, help="Archive status to filter.")
@click.option("--fetchrows", default="-1", help="Number of rows to return or offset,limit.")
@click.option("--sort", default="desc", help="Sort direction: asc or desc.")
@click.option("--recent-days", default="", help="Limit to resources from the last N days.")
@click.option("--ext", default="jpg", help="Preview file extension to return (e.g. jpg, mp4).")
def search_resources_with_previews(query, sizes, restypes, order_by, archive, fetchrows, sort, recent_days, ext):
    log.info(search.search_get_previews(
        search=query,
        restypes=restypes,
        order_by=order_by,
        archive=archive,
        fetchrows=fetchrows,
        sort=sort,
        recent_search_daylimit=recent_days,
        getsizes=sizes,
        previewext=ext
    ))

# ──────────────────────────────────────────────────────────────────────────────
# MISC WORKFLOWS
# ──────────────────────────────────────────────────────────────────────────────

@cli.group(
    name="misc",
    help="🧪 Misc workflows — High-level tools combining multiple operations."
)
def misc_cmd():
    """Combined CLI routines built from multiple API calls."""
    pass

@misc_cmd.command("quick-import-resource", help="Create a resource, set metadata, and upload a file.")
@click.option("--type", "resource_type", required=True, type=int, help="Resource type ID")
@click.option("--archive", default=0, type=int, help="Archive status (0 = live, 1 = pending archive, etc.)")
@click.option("--metadata", required=True, help="JSON string of metadata key-value pairs")
@click.option("--file", "file_path", required=True, type=click.Path(exists=True), help="Path to local file to upload")
def quick_import_resource(resource_type, archive, metadata, file_path):
    """Convenient shortcut to create + tag + upload a new resource."""
    import json
    log.info("📦 Creating resource...")
    res = resource.create_resource(resource_type, archive)
    ref = res.get("resource", res.get("ref"))

    if not ref:
        log.error("❌ Failed to create resource.")
        return

    meta_dict = json.loads(metadata)
    for field_id, value in meta_dict.items():
        log.info(f"🏷️ Setting field {field_id} = {value}")
        metadata.update_field(ref, field_id, value)

    log.info("📤 Uploading file...")
    log.info(resource.upload_file(ref, file_path))

    log.info(f"✅ Resource {ref} created and populated.")

@misc_cmd.command("auto-tag-and-relate", help="Search, tag, and relate a group of resources.")
@click.option("--query", required=True, help="Search string to find target resources.")
@click.option("--field-id", required=True, type=int, help="Field ID to apply tags to.")
@click.option("--value", required=True, help="Value to apply to all found resources.")
@click.option("--relate", is_flag=True, help="Also relate all resources together.")
def auto_tag_and_relate(query, field_id, value, relate):
    """Search for resources, apply metadata, and optionally relate them."""
    log.info(f"🔍 Searching for: {query}")
    result = search.do_search(query)
    if isinstance(result, dict) and "data" in result:
        resources = result["data"]
    else:
        resources = result

    refs = [r["ref"] for r in resources]
    log.info(f"🏷️ Tagging {len(refs)} resources with field {field_id} = {value}")
    for ref in refs:
        metadata.update_field(ref, field_id, value)

    if relate:
        log.info("🔗 Relating resources...")
        csv_ids = ",".join(str(r) for r in refs)
        log.info(resource.relate_all_resources(csv_ids))

    log.info(f"✅ Completed: {len(refs)} resources updated.")

@misc_cmd.command("collection-import-dir", help="Create collection and upload all files from a directory.")
@click.option("--name", required=True, help="Collection name")
@click.option("--dir", "directory", required=True, type=click.Path(exists=True, file_okay=False), help="Path to directory")
@click.option("--type", "resource_type", required=True, type=int, help="Resource type for all new resources")
def collection_import_dir(name, directory, resource_type):
    """Create a collection and import all files in a directory into it."""
    import os

    log.info(f"📚 Creating collection: {name}")
    col = collection.create_collection(name)
    col_id = col.get("collection")

    if not col_id:
        log.error("❌ Collection creation failed.")
        return

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if not os.path.isfile(file_path):
            continue

        log.info(f"📦 Importing file: {filename}")
        res = resource.create_resource(resource_type)
        ref = res.get("resource", res.get("ref"))

        if not ref:
            log.error(f"❌ Failed to create resource for: {filename}")
            continue

        resource.upload_file(ref, file_path)
        collection.add_resource_to_collection(ref, col_id)

    log.info(f"✅ All files in '{directory}' imported into collection {col_id}.")
