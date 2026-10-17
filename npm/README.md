# LLM Crawler & AI Readiness Audit MCP Server

Production Model Context Protocol (MCP) server for evaluating, diagnosing, and optimizing websites for AI search engines, answer bots, and LLM crawlers (GEO/AEO).

[![PyPI version](https://img.shields.io/pypi/v/llm-crawler-audit.svg)](https://pypi.org/project/llm-crawler-audit/)
[![npm version](https://img.shields.io/npm/v/llm-crawler-audit.svg)](https://www.npmjs.com/package/llm-crawler-audit)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Designed for Claude Code, Cursor, and agentic workflows to diagnose crawler accessibility, validate structured `/llms.txt` knowledge bases, and verify markdown mirror content negotiation.

---

## Capabilities & Tools

1. **`audit_robots_for_ai(url: str)`**: Fetches `/robots.txt` and simulates RFC 9309 crawler permissions across 9 AI user-agents: `GPTBot`, `ChatGPT-User`, `ClaudeBot`, `anthropic-ai`, `PerplexityBot`, `Applebot-Extended`, `Bytespider`, `Google-Extended`, and `CCBot`. Returns allow/disallow/unspecified status per agent, crawl delay, sitemaps, and citation impact.
2. **`validate_llms_txt(url: str)`**: Fetches and verifies `/llms.txt` and `/llms-full.txt` compliance against the [llmstxt.org](https://llmstxt.org) standard (H1 title, summary blockquote, link structure, file size, token estimates, and compliance score).
3. **`audit_markdown_mirror(url: str)`**: Checks for `<link rel="alternate" type="text/markdown">` in HTML `<head>`, parses HTTP `Link` headers, and verifies `Accept: text/markdown` content negotiation with `Vary: Accept` caching.
4. **`audit_full_ai_readiness(url: str)`**: Computes a composite 0-100 GEO/AEO readiness score across robots permissions (35%), llms.txt compliance (35%), and markdown mirror parity (30%) with a prioritized action punchlist.
5. **`doctor()`**: Runs diagnostics on network resolution, environment variables, local skills, and testbeds (`surendranb.com`, `builditwithai.xyz`).
6. **`skills_list()` / `skill_read(name: str)`**: Access dynamic workflow playbooks (`ai-robots-txt-playbook`, `llms-txt-authoring`, `markdown-mirror-setup`) loaded from GitHub raw with bundled local fallback.
7. **`check_for_updates()`**: Verify against PyPI for newer releases.

---

## Installation

### Python (`uvx` - Recommended)

```bash
uvx llm-crawler-audit
```

### Node / npm (`npx`)

```bash
npx llm-crawler-audit
```

### Direct Pip

```bash
pip install llm-crawler-audit
llm-crawler-audit
```

---

## Client Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "llm-crawler-audit": {
      "command": "uvx",
      "args": ["llm-crawler-audit"]
    }
  }
}
```

### Cursor IDE

Add under **Settings > Features > MCP**:

- **Name**: `llm-crawler-audit`
- **Type**: `command`
- **Command**: `uvx llm-crawler-audit`

---

## Error Classification & Absorption

All errors returned by tools are classified into actionable envelopes:
- `[INPUT_FIXABLE]`: Malformed URLs, missing schemes, or empty parameters.
- `[ENVIRONMENT_FIXABLE: STOP & ASK HUMAN]`: Network proxy blocks, blocked outbound ports, or local filesystem permission issues.
- `[TRANSIENT]`: DNS timeouts, SSL handshake failures, or upstream 503/504 errors safe for agent retries.

---

## Telemetry & Privacy

This package includes anonymous usage telemetry (Schema v2) to track tool execution reliability, latency, and error rates. No secret keys, authorization tokens, or private URLs are ever transmitted.

To opt out, set either environment variable:
```bash
export DO_NOT_TRACK=1
# or
export MCP_TELEMETRY_OPT_OUT=1
```

---

## License

MIT © [Surendran B](https://surendranb.com)
