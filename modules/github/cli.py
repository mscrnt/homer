#!/usr/bin/env python3

# github cli



import click
import os
from homer.utils.logger import get_module_logger
from homer.cli_registry import register_cli
from .github_client import (
    get_repo_markdown_files,
    get_repo_info,
    list_branches,
    list_pull_requests,
    create_issue
)

logger = get_module_logger("github-cli")

@register_cli("github")
@click.group(
    invoke_without_command=True,
    help="Github: GitHub automation module for repository metadata, PRs, issues, and workflows.",
    context_settings=dict(help_option_names=["-h", "--help"])
)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("👻 HOMER Github Module — GitHub automation tools")
        click.echo("Use `--help` to see available commands.")
        ctx.exit(0)

# ──────────────────────────────────────────────────────────────────────────────
# GITHUB REPO TOOLS
# ──────────────────────────────────────────────────────────────────────────────

@cli.command("info", help="Get basic repository information.")
@click.option("--repo", required=True, help="GitHub repo in owner/repo format.")
def repo_info(repo):
    data = get_repo_info(repo)
    logger.info(f"📘 Repo: {data.full_name}")
    logger.info(f"🔖 Default Branch: {data.default_branch}")
    logger.info(f"📝 Description: {data.description}")
    logger.info(f"⭐ Stars: {data.stargazers_count} | 👁 Watchers: {data.watchers_count}")

@cli.command("branches", help="List all branches in the given GitHub repo.")
@click.option("--repo", required=True, help="GitHub repo in owner/repo format.")
def branches(repo):
    for branch in list_branches(repo):
        logger.info(f"🌿 {branch.name}")

@cli.command("pulls", help="List open pull requests.")
@click.option("--repo", required=True, help="GitHub repo in owner/repo format.")
def pulls(repo):
    for pr in list_pull_requests(repo):
        logger.info(f"🔃 #{pr.number} {pr.title} by {pr.user.login} (state: {pr.state})")

@cli.command("new-issue", help="Create a new issue in a repository.")
@click.option("--repo", required=True, help="GitHub repo in owner/repo format.")
@click.option("--title", required=True, help="Issue title.")
@click.option("--body", default="", help="Optional body text for the issue.")
def new_issue(repo, title, body):
    issue = create_issue(repo, title=title, body=body)
    logger.info(f"✅ Created issue #{issue.number}: {issue.title}")

# ──────────────────────────────────────────────────────────────────────────────
# MARKDOWN FETCHER
# ──────────────────────────────────────────────────────────────────────────────

@cli.command("fetch-md", help="List all Markdown files in the given GitHub repo.")
@click.option("--repo", required=True, help="GitHub repo in owner/repo format.")
@click.option("--branch", default="main", help="Branch to fetch from.")
def fetch_markdown(repo, branch):
    logger.info(f"📦 Fetching markdown from {repo}@{branch}")
    md_files = get_repo_markdown_files(repo, branch)
    for f in md_files:
        logger.info(f"📝 {f.path} ({f.size} bytes)")

# ──────────────────────────────────────────────────────────────────────────────
# WORKFLOW TOOLS
# ──────────────────────────────────────────────────────────────────────────────

@cli.command("run-workflow", help="Trigger a GitHub Actions workflow using the `gh` CLI.")
@click.option("--workflow", required=True, help="Workflow file name (e.g. `deploy.yml`).")
@click.option("--repo", required=True, help="GitHub repo in owner/repo format.")
@click.option("--ref", default="main", help="Branch or tag to run the workflow against.")
def trigger_workflow(workflow, repo, ref):
    logger.info(f"🚀 Triggering workflow {workflow} on {repo}@{ref}")
    exit_code = os.system(f"gh workflow run {workflow} --repo {repo} --ref {ref}")
    if exit_code != 0:
        logger.warning("⚠️ Workflow trigger failed.")
    else:
        logger.info("✅ Workflow triggered successfully")
