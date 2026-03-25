# Gomboc Code Remediation Skill for Claude Code

**Deterministic code remediation powered by ORL (Open Remediation Language).**

Instead of generating alerts, Gomboc delivers merge-ready pull requests. The perfect complement to agentic coding — scan, fix, and improve code across infrastructure, applications, and configurations with 94%+ accuracy.

## What It Does

- 🔍 **Scan** any codebase for issues (infrastructure, apps, configs)
- 🔧 **Generate** deterministic fixes (same input = same output, always)
- 🤖 **Perfect for agents** — ORL-powered remediation paired with AI
- 📊 **Multiple formats** — JSON, Markdown, SARIF
- 🔐 **Syntax-aware** — Tree-sitter based matching (no brittle regex)

## Quick Start

```bash
# Scan code
@gomboc scan path:./src

# Generate fixes
@gomboc fix path:./src format:pull_request

# Apply fixes
@gomboc remediate path:./src commit:true
```

## Key Features

✅ **Deterministic Remediation** — ORL engine (same input = same output)
✅ **94%+ Accuracy** — Syntax-aware fixes, not brittle patterns
✅ **Agent-Friendly** — Built for agentic coding feedback loops
✅ **Free Forever** — Community Edition (no credit card)
✅ **Production-Ready** — Real API tested, live endpoints verified

## How Gomboc Works (ORL Engine)

Gomboc's **Open Remediation Language** provides deterministic code fixing:

```
Code → Policy Evaluation → Syntax Analysis → Deterministic Fix → PR
```

Unlike generative AI (probabilistic), ORL guarantees:
- Same issue always gets same fix (repeatable)
- Syntax-tree aware (precise, not regex-based)
- Safe for bulk remediation across repos
- Auditable diffs and validation signals

## For Agents

This skill is **the ideal companion to agentic coding**:

**The Agent Loop:**
1. **Agent generates** code for feature/task
2. **Gomboc scans** and identifies issues
3. **ORL generates** deterministic fixes
4. **Agent applies** fixes and iterates
5. **Repeat** with next feature

This creates **continuous improvement** with:
- **Deterministic** fixes (safe for autonomous loops)
- **Trustworthy** results (94%+ merge rate)
- **Autonomous** operation (no human in loop)
- **Continuous** feedback (scan → fix → improve)

## Integration Paths

**VS Code/Cursor:**
- Install Gomboc VSCode extension
- Get token from https://app.gomboc.ai
- Scan on file save, apply fixes

**GitHub:**
- Install GitHub App: https://github.com/apps/gomboc-ai-community
- Automatic scanning and PR generation

**Claude Code:**
```
@gomboc scan path:./src
@gomboc fix path:./src format:pull_request
@gomboc remediate path:./src commit:true
```

**CLI/API:**
```bash
export GOMBOC_PAT="your_token"
python scripts/cli-wrapper.py scan --path ./src
```

## Documentation

- **[Full Docs](https://github.com/andrewpetecoleman-cloud/clawhub-gomboc-security)**
- **[Setup Guide](https://github.com/andrewpetecoleman-cloud/clawhub-gomboc-security/blob/main/references/setup.md)**
- **[ORL Engine Docs](https://docs.gomboc.ai/orl)**
- **[Official Gomboc Docs](https://docs.gomboc.ai)**
- **[Community Edition Guide](https://docs.gomboc.ai/getting-started-ce)**

## Support

- **GitHub:** https://github.com/andrewpetecoleman-cloud/clawhub-gomboc-security
- **Feedback:** https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions
- **Issues:** https://github.com/andrewpitecoleman-cloud/clawhub-gomboc-security/issues

## License

MIT License — Free forever
