# SPDX-License-Identifier: MIT
"""Deterministic fixtures and testbed mocks for llm-crawler-audit test suite."""
import pytest

MOCK_SURENDRANB_ROBOTS = """User-agent: *
Allow: /

Sitemap: https://surendranb.com/sitemap.xml
"""

MOCK_SURENDRANB_LLMS = """# Surendran B. — AI Systems & Growth

> VP of AI-Led Growth at Atlan. Building AI-native systems in public.

## Overview

This site documents the work, thinking, and experiments of Surendran Balachandran.

- [Site Illustrated Room](https://surendranb.com/): Cutaway portfolio.
- [Studio Systems Lab](https://builditwithai.xyz): Live experiments and MCP servers.
- [Sitemap](https://surendranb.com/sitemap.xml): Full site index.
"""

MOCK_FREEINFERENCE_ROBOTS = """User-agent: *
Allow: /
User-agent: GPTBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bytespider
Allow: /
User-agent: CCBot
Allow: /
# LLMs: https://freeinference.dev/llms.txt
Sitemap: https://freeinference.dev/sitemap.xml
"""

MOCK_BUILDITWITHAI_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>BuildItWithAI</title>
  <link rel="alternate" type="text/markdown" href="https://builditwithai.xyz/home.md">
</head>
<body>
  <h1>BuildItWithAI Studio</h1>
</body>
</html>
"""

MOCK_BUILDITWITHAI_MARKDOWN = """---
title: "BuildItWithAI Studio"
description: "Public systems lab by Surendran B."
---

# BuildItWithAI Studio

Public systems lab by Surendran B. Explore maintained tools and agent systems.
"""

@pytest.fixture(autouse=True)
def disable_telemetry_for_tests(monkeypatch):
    monkeypatch.setenv("MCP_TELEMETRY_OPT_OUT", "1")
    monkeypatch.setenv("DO_NOT_TRACK", "1")
