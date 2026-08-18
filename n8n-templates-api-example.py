"""
n8n templates API on Apify: search the n8n workflow library, rank templates by
views, and export importable workflow JSON.

Actor:  https://apify.com/johnvc/n8n-workflow-templates-scraper?fpr=9n7kx3
Token:  get a free Apify API key at https://apify.com?fpr=9n7kx3

Setup:
    uv sync
    cp .env.example .env      # then paste your token into .env
    uv run n8n-templates-api-example.py

Every run input below caps maxResults at a handful of templates so your first
run costs almost nothing. Set maxResults to 0 to pull everything a query
matches once you have seen the output shape.
"""

import json
import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR = "johnvc/n8n-workflow-templates-scraper"

TOKEN = os.getenv("APIFY_TOKEN")
if not TOKEN:
    raise SystemExit(
        "Set APIFY_TOKEN in .env first. Free key: https://apify.com?fpr=9n7kx3"
    )

client = ApifyClient(TOKEN)


def run_actor(run_input: dict) -> list[dict]:
    """Start the Actor, wait for it to finish, return the dataset rows."""
    run = client.actor(ACTOR).call(run_input=run_input)
    dataset_id = run.default_dataset_id
    return list(client.dataset(dataset_id).iterate_items())


def show(rows: list[dict], limit: int = 5) -> None:
    """Print a short, readable summary of what came back."""
    templates = [r for r in rows if r.get("result_type") == "template"]
    others = [r for r in rows if r.get("result_type") != "template"]

    print(f"  {len(templates)} templates, {len(others)} other rows")

    for row in templates[:limit]:
        nodes = row.get("nodes") or []
        price = row.get("price")
        price_text = "free" if not price else str(price)
        print(f"  - {row.get('name')}")
        print(f"      url:        {row.get('url')}")
        print(f"      creator:    {row.get('creatorUsername')} (verified: {row.get('creatorVerified')})")
        print(f"      views:      {row.get('totalViews')} total, {row.get('recentViews')} recent")
        print(f"      created:    {row.get('createdAt')}")
        print(f"      price:      {price_text}")
        print(f"      nodes:      {row.get('nodeCount')} ({', '.join(str(n) for n in nodes[:4])})")
        print(f"      categories: {', '.join(str(c) for c in (row.get('categories') or [])[:4])}")

    for row in others[:2]:
        if row.get("error_message"):
            print(f"  ! {row.get('query') or row.get('id')}: {row.get('error_message')}")


def find_most_viewed_n8n_workflows() -> list[dict]:
    """Recipe: rank the n8n workflow library by total views.

    Mirrors the published task "Find the most viewed n8n workflows".
    """
    return run_actor(
        {
            "mode": "search",
            "queries": ["automation"],
            "sortBy": "most_viewed",
            "maxResults": 5,
        }
    )


def find_best_n8n_ai_agent_workflows() -> list[dict]:
    """Recipe: find the most viewed AI agent templates.

    Mirrors the published task "Find the best n8n AI agent workflows".
    """
    return run_actor(
        {
            "mode": "search",
            "queries": ["ai agent"],
            "sortBy": "most_viewed",
            "maxResults": 5,
        }
    )


def export_importable_workflow_json() -> list[dict]:
    """Recipe: pull the importable workflow JSON for a template.

    Mirrors the published task "Export importable n8n workflow JSON". Setting
    includeWorkflowJson returns the full definition you can paste into n8n,
    so this one is kept to a single template to stay cheap.
    """
    return run_actor(
        {
            "mode": "search",
            "queries": ["slack"],
            "sortBy": "most_viewed",
            "includeWorkflowJson": True,
            "maxResults": 1,
        }
    )


if __name__ == "__main__":
    print("1. Most viewed n8n workflows")
    show(find_most_viewed_n8n_workflows())

    print("\n2. Best n8n AI agent workflows")
    show(find_best_n8n_ai_agent_workflows())

    print("\n3. Export importable workflow JSON")
    rows = export_importable_workflow_json()
    show(rows)

    workflow_json = next(
        (r.get("workflowJson") for r in rows if r.get("workflowJson")), None
    )
    if workflow_json:
        text = json.dumps(workflow_json) if isinstance(workflow_json, dict) else str(workflow_json)
        print(f"\n  workflowJson present, {len(text)} chars. Paste it into n8n with Import from clipboard.")
    else:
        print("\n  No workflowJson on this row. Some templates are paid and do not expose it.")
