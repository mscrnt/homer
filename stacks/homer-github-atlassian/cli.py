# stacks/homer-github-atlassian/cli.py


import click
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger
from homer.modules.github.github_client import get_repo_markdown_files
from homer.modules.atlassian.confluence import sync_markdown_to_confluence

log = get_module_logger("github-atlassian")

@register_cli("docsync")
@click.group(
    invoke_without_command=True,
    help="Stacked automation: GitHub <-> Confluence sync commands.",
    context_settings=dict(help_option_names=["-h", "--help"])
)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("🧩 HOMER Github + Atlassian Stack CLI")
        click.echo("Use `--help` to view available commands.")
        ctx.exit(0)

@cli.command("sync-docs", help="Sync markdown docs from GitHub repo to Confluence.")
@click.option("--repo", required=True, help="GitHub repo in owner/repo format.")
@click.option("--branch", default="main", help="Branch to sync from.")
def sync_docs(repo, branch):
    log.info(f"🔄 Fetching markdown from {repo}@{branch}")
    files = get_repo_markdown_files(repo, branch)
    if not files:
        log.warning("⚠️ No markdown files found.")
        return
    log.info(f"📤 Syncing {len(files)} markdown files to Confluence...")
    sync_markdown_to_confluence(files)
    log.info("✅ Documentation sync complete.")
