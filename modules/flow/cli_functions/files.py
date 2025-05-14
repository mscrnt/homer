

import click
from pathlib import Path
from homer.utils.logger import get_module_logger
import modules.flow.logic.files as files_logic

log = get_module_logger("flow.cli.files")

@click.group(
    name="files",
    help="📎 File commands — Upload, download, and share files or thumbnails."
)
def files_cmd():
    pass

@files_cmd.command("upload", help="Upload a file to a ShotGrid entity.")
@click.option("--entity-type", required=True, help="Entity type (e.g., Shot, Version)")
@click.option("--entity-id", required=True, type=int, help="Entity ID to attach file to")
@click.option("--file", "file_path", required=True, type=click.Path(exists=True), help="Path to the file to upload")
@click.option("--field-name", default=None, help="Optional file field on the entity")
@click.option("--display-name", default=None, help="Optional display name for the file")
@click.option("--tag-list", default=None, help="Comma-separated tags for the file")
def cli_upload_file(entity_type, entity_id, file_path, field_name, display_name, tag_list):
    from fastapi import UploadFile
    with open(file_path, "rb") as f:
        upload = UploadFile(filename=Path(file_path).name, file=f)
        result = files_logic.upload_file(entity_type, entity_id, upload, field_name, display_name, tag_list)
        click.echo(f"✅ Uploaded: Attachment ID = {result}")

@files_cmd.command("thumbnail", help="Upload a thumbnail image to an entity.")
@click.option("--entity-type", required=True, help="Entity type")
@click.option("--entity-id", required=True, type=int, help="Entity ID")
@click.option("--file", "file_path", required=True, type=click.Path(exists=True), help="Path to image file")
def cli_upload_thumbnail(entity_type, entity_id, file_path):
    from fastapi import UploadFile
    with open(file_path, "rb") as f:
        upload = UploadFile(filename=Path(file_path).name, file=f)
        result = files_logic.upload_thumbnail(entity_type, entity_id, upload)
        click.echo(f"✅ Thumbnail uploaded: Attachment ID = {result}")

@files_cmd.command("filmstrip", help="Upload a filmstrip thumbnail to an entity.")
@click.option("--entity-type", required=True, help="Entity type")
@click.option("--entity-id", required=True, type=int, help="Entity ID")
@click.option("--file", "file_path", required=True, type=click.Path(exists=True), help="Path to filmstrip image")
def cli_upload_filmstrip(entity_type, entity_id, file_path):
    from fastapi import UploadFile
    with open(file_path, "rb") as f:
        upload = UploadFile(filename=Path(file_path).name, file=f)
        result = files_logic.upload_filmstrip_thumbnail(entity_type, entity_id, upload)
        click.echo(f"✅ Filmstrip thumbnail uploaded: Attachment ID = {result}")

@files_cmd.command("download-url", help="Get direct download URL for an attachment.")
@click.option("--attachment-id", required=True, type=int, help="Attachment ID")
def cli_download_url(attachment_id):
    url = files_logic.get_download_url(attachment_id)
    click.echo(f"📥 Download URL: {url}")

@files_cmd.command("share-thumbnail", help="Share a thumbnail or filmstrip with other entities.")
@click.option("--entity-type", required=True, help="Entity type to share from or to")
@click.option("--entity-ids", required=True, help="Comma-separated list of entity IDs to share to")
@click.option("--file", "file_path", type=click.Path(exists=True), help="Optional file path to upload and share")
@click.option("--source-id", type=int, help="Optional source entity ID to copy thumbnail from")
@click.option("--filmstrip", is_flag=True, help="Share filmstrip thumbnail instead of default image")
def cli_share_thumbnail(entity_type, entity_ids, file_path, source_id, filmstrip):
    from fastapi import UploadFile
    entities = [{"type": entity_type, "id": int(eid.strip())} for eid in entity_ids.split(",")]

    if file_path:
        with open(file_path, "rb") as f:
            upload = UploadFile(filename=Path(file_path).name, file=f)
            result = files_logic.share_thumbnail(entities, file=upload, filmstrip_thumbnail=filmstrip)
    elif source_id:
        source_entity = {"type": entity_type, "id": source_id}
        result = files_logic.share_thumbnail(entities, source_entity=source_entity, filmstrip_thumbnail=filmstrip)
    else:
        raise click.UsageError("Either --file or --source-id must be provided.")

    click.echo(f"✅ Shared thumbnail: Attachment ID = {result}")
