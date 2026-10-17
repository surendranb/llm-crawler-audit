# SPDX-License-Identifier: MIT
"""Unit and contract tests for llm-crawler-audit server tools."""
import json
import pytest
from unittest.mock import patch

from llm_crawler_audit.server import (
    audit_robots_for_ai,
    validate_llms_txt,
    audit_markdown_mirror,
    audit_full_ai_readiness,
    doctor,
    skills_list,
    skill_read,
    check_for_updates,
)
from tests.conftest import (
    MOCK_SURENDRANB_ROBOTS,
    MOCK_SURENDRANB_LLMS,
    MOCK_FREEINFERENCE_ROBOTS,
    MOCK_BUILDITWITHAI_HTML,
    MOCK_BUILDITWITHAI_MARKDOWN,
)


def test_audit_robots_surendranb():
    with patch("llm_crawler_audit.server._fetch_url") as mock_fetch:
        mock_fetch.return_value = (200, {"content-type": "text/plain"}, MOCK_SURENDRANB_ROBOTS.encode("utf-8"))
        res_raw = audit_robots_for_ai("https://surendranb.com")
        res = json.loads(res_raw)

        assert res["exists"] is True
        assert res["allowed_count"] == 9
        assert res["disallowed_count"] == 0
        assert "https://surendranb.com/sitemap.xml" in res["sitemaps"]
        assert res["ai_readiness_score"] == 100


def test_audit_robots_freeinference_explicit():
    with patch("llm_crawler_audit.server._fetch_url") as mock_fetch:
        mock_fetch.return_value = (200, {"content-type": "text/plain"}, MOCK_FREEINFERENCE_ROBOTS.encode("utf-8"))
        res_raw = audit_robots_for_ai("https://freeinference.dev")
        res = json.loads(res_raw)

        assert res["exists"] is True
        assert res["allowed_count"] == 9
        assert len(res["llm_comments"]) > 0
        assert "https://freeinference.dev/sitemap.xml" in res["sitemaps"]


def test_audit_robots_blocked_agent():
    blocked_txt = """User-agent: GPTBot
Disallow: /

User-agent: *
Allow: /
"""
    with patch("llm_crawler_audit.server._fetch_url") as mock_fetch:
        mock_fetch.return_value = (200, {"content-type": "text/plain"}, blocked_txt.encode("utf-8"))
        res_raw = audit_robots_for_ai("https://example.com")
        res = json.loads(res_raw)

        assert res["disallowed_count"] == 1
        assert "GPTBot" in res["search_bots_blocked"]
        assert any("Unblock search indexers" in rec for rec in res["recommendations"])


def test_audit_robots_missing_404():
    with patch("llm_crawler_audit.server._fetch_url") as mock_fetch:
        mock_fetch.return_value = (404, {}, b"Not Found")
        res_raw = audit_robots_for_ai("https://ga4mcp.com")
        res = json.loads(res_raw)

        assert res["exists"] is False
        assert res["http_status"] == 404
        assert res["rfc_9309_default"] == "allow_all"
        assert res["allowed_count"] == 9


def test_audit_robots_invalid_url():
    res_raw = audit_robots_for_ai("")
    res = json.loads(res_raw)
    assert res.get("classification") == "[INPUT_FIXABLE]"


def test_validate_llms_txt_valid():
    def mock_fetch(url, *args, **kwargs):
        if "llms.txt" in url:
            return (200, {"content-type": "text/markdown"}, MOCK_SURENDRANB_LLMS.encode("utf-8"))
        return (404, {}, b"")

    with patch("llm_crawler_audit.server._fetch_url", side_effect=mock_fetch):
        res_raw = validate_llms_txt("https://surendranb.com")
        res = json.loads(res_raw)

        assert res["compliance_score"] >= 80
        llms_data = res["llms_txt"]
        assert llms_data["valid"] is True
        assert "Surendran B." in llms_data["title"]
        assert "VP of AI-Led Growth" in llms_data["summary"]
        assert llms_data["links_count"] >= 3


def test_validate_llms_txt_missing():
    with patch("llm_crawler_audit.server._fetch_url", return_value=(404, {}, b"")):
        res_raw = validate_llms_txt("https://example.com")
        res = json.loads(res_raw)

        assert res["compliance_score"] == 0
        assert res["llms_txt"]["valid"] is False


def test_audit_markdown_mirror():
    def mock_fetch(url, headers=None, *args, **kwargs):
        headers = headers or {}
        accept = headers.get("Accept", "")
        if "text/markdown" in accept:
            return (200, {"content-type": "text/markdown; charset=utf-8"}, MOCK_BUILDITWITHAI_MARKDOWN.encode("utf-8"))
        if url == "https://builditwithai.xyz/home.md":
            return (200, {"content-type": "text/markdown"}, MOCK_BUILDITWITHAI_MARKDOWN.encode("utf-8"))
        return (200, {"content-type": "text/html", "vary": "Accept"}, MOCK_BUILDITWITHAI_HTML.encode("utf-8"))

    with patch("llm_crawler_audit.server._fetch_url", side_effect=mock_fetch):
        res_raw = audit_markdown_mirror("https://builditwithai.xyz")
        res = json.loads(res_raw)

        assert res["link_tag_discovered"] is True
        assert res["content_negotiation_supported"] is True
        assert res["markdown_score"] == 100
        assert res["mirror_verified"] is True


def test_audit_full_ai_readiness():
    def mock_fetch(url, headers=None, *args, **kwargs):
        headers = headers or {}
        accept = headers.get("Accept", "")
        if "robots.txt" in url:
            return (200, {}, MOCK_SURENDRANB_ROBOTS.encode("utf-8"))
        if "llms.txt" in url:
            return (200, {}, MOCK_SURENDRANB_LLMS.encode("utf-8"))
        if "text/markdown" in accept or "home.md" in url:
            return (200, {"content-type": "text/markdown"}, MOCK_BUILDITWITHAI_MARKDOWN.encode("utf-8"))
        return (200, {"content-type": "text/html"}, MOCK_BUILDITWITHAI_HTML.encode("utf-8"))

    with patch("llm_crawler_audit.server._fetch_url", side_effect=mock_fetch):
        res_raw = audit_full_ai_readiness("https://builditwithai.xyz")
        res = json.loads(res_raw)

        assert res["composite_score"] > 80
        assert "breakdown" in res
        assert "robots_ai_accessibility" in res["breakdown"]
        assert "llms_txt_compliance" in res["breakdown"]
        assert "markdown_mirror_parity" in res["breakdown"]


def test_doctor():
    with patch("llm_crawler_audit.server._fetch_url", return_value=(200, {}, b"ok")):
        res_raw = doctor()
        res = json.loads(res_raw)

        assert res["server"] == "llm-crawler-audit"
        assert res["status"] in ("healthy", "degraded")
        assert "connectivity_tests" in res
        assert len(res["skills_discovered"]) >= 3


def test_skills():
    res_list_raw = skills_list()
    res_list = json.loads(res_list_raw)
    assert "ai-robots-txt-playbook" in res_list["skills"]
    assert "llms-txt-authoring" in res_list["skills"]
    assert "markdown-mirror-setup" in res_list["skills"]

    content = skill_read("ai-robots-txt-playbook")
    assert "# AI Search & LLM Crawler robots.txt Playbook" in content

    empty_res = skill_read("")
    assert "[INPUT_FIXABLE]" in empty_res

    unknown_res = skill_read("nonexistent-skill")
    assert "[INPUT_FIXABLE] Unknown skill" in unknown_res


def test_check_for_updates():
    res_raw = check_for_updates()
    res = json.loads(res_raw)
    assert res["package"] == "llm-crawler-audit"
    assert "current_version" in res
