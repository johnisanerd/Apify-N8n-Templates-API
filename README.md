# n8n Templates API: Search the n8n Workflow Library as JSON

Query the public n8n workflow template library over an API. Search by keyword, category, app, or node, rank results by views, pull a creator's whole portfolio, and export importable n8n workflow JSON.

Runs on the [n8n Workflow Templates Actor](https://apify.com/johnvc/n8n-workflow-templates-scraper?fpr=9n7kx3) on Apify. This repo shows two ways to call it: a Python quick start, and MCP install steps for five clients.

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/hqdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

## Text walkthrough

Browsing n8n templates by hand is fine for one workflow and useless for research. This n8n templates API turns that library into rows you can sort and filter. It runs in three modes. `search` takes a list of `queries` plus optional `categories`, `apps`, and `nodes` filters, and returns matching templates ordered by `most_viewed`, `newest`, or `relevance`. `creator` takes usernames and returns everything a builder has published, which is how you size up a creator's portfolio. `details` takes template ids or URLs when you already know what you want. Every row carries `name`, `url`, `totalViews`, `createdAt`, `price`, `creatorUsername`, `nodeCount`, and the `nodes` list, so you can answer questions the site will not answer for you: which integrations show up most in popular automations, which creators actually get views, and which of the best n8n workflows are free rather than paid. Set `includeWorkflowJson` and each row also carries the full importable workflow JSON, ready to paste into your own n8n with Import from clipboard.

## Quick start

```bash
uv sync
cp .env.example .env      # paste your Apify token into .env
uv run n8n-templates-api-example.py
```

Get a free Apify API token at https://apify.com?fpr=9n7kx3 (Console, then Settings, then API & Integrations).

The example caps `maxResults` at a handful of templates so your first run costs almost nothing. Set `maxResults` to 0 to pull every template a query matches.

## Recipes

Each of these is a published, ready-to-run example on the Apify Store. Open one, press Start, and read the output before you write any code.

- [Find the most viewed n8n workflows](https://apify.com/johnvc/n8n-workflow-templates-scraper/examples/find-most-viewed-n8n-workflows?fpr=9n7kx3)
- [Find the best n8n AI agent workflows](https://apify.com/johnvc/n8n-workflow-templates-scraper/examples/find-best-n8n-ai-agent-workflows?fpr=9n7kx3)
- [Export importable n8n workflow JSON](https://apify.com/johnvc/n8n-workflow-templates-scraper/examples/export-importable-n8n-workflow-json?fpr=9n7kx3)
- [Analyze an n8n creator's workflow portfolio](https://apify.com/johnvc/n8n-workflow-templates-scraper/examples/analyze-n8n-creator-workflow-portfolio?fpr=9n7kx3)
- [Browse the n8n workflow library by category](https://apify.com/johnvc/n8n-workflow-templates-scraper/examples/browse-n8n-workflow-library-by-category?fpr=9n7kx3)

The first three are implemented as functions in `n8n-templates-api-example.py`, so you can run them locally as well.

**Schedule tip:** save a search as a task and schedule it monthly. Because `totalViews` is captured per run, a repeating schedule turns the template library into a trend series showing which workflows are actually gaining traction.

## Input parameters

| Parameter | Type | What it does |
|---|---|---|
| `mode` | string | `search`, `creator`, or `details`. Picks which surface to read. |
| `queries` | array | Search terms, used in `search` mode. |
| `sortBy` | string | `most_viewed`, `newest`, or `relevance`. |
| `categories` | array | Restrict to given template categories. |
| `apps` | array | Restrict to templates using given apps. |
| `nodes` | array | Restrict to templates containing given n8n nodes. |
| `usernames` | array | Creator usernames or profile URLs, used in `creator` mode. |
| `workflowIds` | array | Template ids or URLs, used in `details` mode. |
| `includeWorkflowJson` | boolean | Also return the importable workflow JSON and full detail. |
| `maxResults` | integer | Cap the rows returned. 0 means no cap. |

## Output fields

One row per template.

| Field | What it holds |
|---|---|
| `result_type` | Row kind. Template rows carry `template`. |
| `id`, `url` | Template id and its page on n8n.io. |
| `name`, `description` | Template title and summary. |
| `totalViews`, `recentViews` | View counts, the ranking signal. |
| `createdAt` | When the template was published. |
| `price`, `purchaseUrl` | 0 for free templates, otherwise the paid price. |
| `creatorUsername`, `creatorName`, `creatorVerified` | Who built it. |
| `workflowsCount`, `avatar`, `links` | Creator profile detail in `creator` mode. |
| `categories`, `nodes`, `nodeCount` | Classification and the node list. |
| `workflowJson` | Importable workflow definition, when requested. |
| `query` | Which of your queries produced this row. |
| `error_message` | Why a query or id could not be read. |

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the n8n templates API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings > Connectors** (or **Settings > Developer > Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/n8n-workflow-templates-scraper"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the n8n templates API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

---

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/n8n-workflow-templates-scraper"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/n8n-workflow-templates-scraper" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the n8n templates API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

---

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings > Connectors > Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/n8n-workflow-templates-scraper`.
3. In any chat, open **+ > Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/n8n-workflow-templates-scraper`, using OAuth when prompted.
5. Ask Claude to run the n8n templates API.

Open Claude on the web: https://claude.ai

---

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/n8n-workflow-templates-scraper"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/n8n-workflow-templates-scraper",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor > Settings > MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the n8n templates API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

---

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/n8n-workflow-templates-scraper`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

<!-- ask-ai:start -->
## 🤖 Ask an AI assistant about this Actor

Open a ready-to-send prompt about the n8n Workflow Templates API in the AI of your choice:

- 💬 [ChatGPT](https://chatgpt.com/?q=Using%20the%20n8n%20Workflow%20Templates%20API%20on%20Apify%20%28https://apify.com/johnvc/n8n-workflow-templates-scraper?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Find%20the%20best%20n8n%20AI%20agent%20workflows%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
- 🧠 [Claude](https://claude.ai/new?q=Using%20the%20n8n%20Workflow%20Templates%20API%20on%20Apify%20%28https://apify.com/johnvc/n8n-workflow-templates-scraper?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Find%20the%20best%20n8n%20AI%20agent%20workflows%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
- 🔍 [Perplexity](https://www.perplexity.ai/search?q=Using%20the%20n8n%20Workflow%20Templates%20API%20on%20Apify%20%28https://apify.com/johnvc/n8n-workflow-templates-scraper?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Find%20the%20best%20n8n%20AI%20agent%20workflows%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
- 🅒 [Copilot](https://copilot.microsoft.com/?q=Using%20the%20n8n%20Workflow%20Templates%20API%20on%20Apify%20%28https://apify.com/johnvc/n8n-workflow-templates-scraper?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Find%20the%20best%20n8n%20AI%20agent%20workflows%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
<!-- ask-ai:end -->

## FAQ

**Is there an official n8n templates API?**
n8n publishes the template library as a website rather than a documented public API you can sign up for. This Actor reads that public library and hands back the same structure an API would, so you can query the n8n workflow library programmatically.

**Can I get importable n8n workflow JSON?**
Yes. Set `includeWorkflowJson` to true and each row carries the full workflow definition. Paste it into n8n with Import from clipboard and the nodes appear wired as the creator built them. Paid templates do not expose their JSON.

**How do I find the best n8n workflows?**
Search with `sortBy` set to `most_viewed`. Views are the only public popularity signal the library exposes, and `totalViews` is returned on every row so you can rank or threshold yourself. Filter on `price` of 0 if you only want free n8n workflows.

**Can I search by node or app?**
Yes. `nodes` filters to templates containing specific n8n nodes, and `apps` filters by integration. That is the quickest way to answer "what do people actually build with this integration" before you build it yourself.

**How do I analyze one creator's templates?**
Use `creator` mode with their username or profile URL. You get every template they have published plus profile fields such as `workflowsCount` and `creatorVerified`.

**Does this work from Claude Code or an MCP client?**
Yes. The Actor is exposed through the Apify MCP server, so Claude Code, Claude Cowork, Claude on the web, Cursor, and ChatGPT can all call it as a tool. The five install sections above cover each client.

**How much does a run cost?**
Pricing is on the [Actor page](https://apify.com/johnvc/n8n-workflow-templates-scraper?fpr=9n7kx3) and bills per delivered template row, so a five-result search costs five rows. Check the live pricing there rather than a number copied into a README.

## People also search for

n8n templates, n8n workflow templates, n8n mcp, n8n workflow examples, n8n automation templates, best n8n workflows, n8n workflow library, free n8n workflows, n8n template library, n8n workflow json, n8n claude code, n8n claude skill, n8n templates api

## More

- Actor on the Apify Store: https://apify.com/johnvc/n8n-workflow-templates-scraper?fpr=9n7kx3
- Free Apify account: https://apify.com?fpr=9n7kx3
- Apify Python client docs: https://docs.apify.com/api/client/python/
- Apify MCP docs: https://docs.apify.com/platform/integrations/mcp
- uv: https://docs.astral.sh/uv/

Last Updated: 2026.09.22
