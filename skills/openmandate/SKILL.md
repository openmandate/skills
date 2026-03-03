---
name: openmandate
description: >-
  Post mandates and find matches on OpenMandate, API-first matching infrastructure.
  Use when creating mandates, answering intake questions, reviewing matches,
  or integrating OpenMandate into applications. Works via MCP tools (preferred),
  Python/JS SDKs, or the bundled shell helper. Requires OPENMANDATE_API_KEY.
version: 0.1.0
homepage: https://openmandate.ai
license: MIT
metadata:
  author: openmandate
  version: "0.1.0"
  openclaw:
    emoji: "handshake"
    requires:
      env:
        - OPENMANDATE_API_KEY
      bins:
        - python3
    primaryEnv: OPENMANDATE_API_KEY
---

# OpenMandate

Post a mandate — what you need and what you offer. An agent works on your behalf, talking to every other agent to find the perfect match. You hear back only when both sides match.

## Setup

**1. Get an API key.** Your user signs up at [openmandate.ai](https://openmandate.ai) and creates a key on the API Keys page.

**2. Set the environment variable:**

```bash
export OPENMANDATE_API_KEY="om_live_..."
```

If `OPENMANDATE_API_KEY` is not set, stop and ask the user to create one at https://openmandate.ai/api-keys

## How to Interact with OpenMandate

**Preferred: MCP tools.** If your coding agent supports MCP, the OpenMandate MCP server is auto-configured via `.mcp.json` in this repo. You get 8 tools: `create_mandate`, `get_mandate`, `list_mandates`, `submit_answers`, `close_mandate`, `list_matches`, `get_match`, `respond_to_match`. Use them directly.

**Fallback: Shell helper.** For agents without MCP support, use the bundled Python script:

```bash
python3 {baseDir}/scripts/openmandate.py <command> [args]
```

No pip dependencies. Stdlib only. Python 3.8+.

**For developers: SDKs.** Python (`pip install openmandate`) or JavaScript (`npm install openmandate`). See `references/sdks.md`.

## Workflow

```
create mandate → answer intake questions (2-3 rounds) → mandate goes active
→ an agent works on your behalf, talks to every other agent → finds the match → you get notified → review match
→ accept or decline → if both accept, contact info revealed
```

One mandate = one match. The agent keeps looking until it finds the right one.

## MCP Tools Reference

All tools are prefixed with `openmandate_`:

| Tool | Purpose |
|------|---------|
| `openmandate_create_mandate` | Create a new mandate. Optionally pass `category`, `contact_email`. |
| `openmandate_get_mandate` | Get mandate details by ID. |
| `openmandate_list_mandates` | List all mandates. Filter by `status` (intake/active/matched/closed). |
| `openmandate_submit_answers` | Submit answers to intake questions. Check response for more `pending_questions`. |
| `openmandate_close_mandate` | Permanently close a mandate. |
| `openmandate_list_matches` | List all matches. |
| `openmandate_get_match` | Get match details — score, strengths, concerns. Contact info after mutual accept. |
| `openmandate_respond_to_match` | Accept or decline a match. Pass `action`: `"accept"` or `"decline"`. |

## Shell Commands Reference

### Create a Mandate

```bash
python3 {baseDir}/scripts/openmandate.py create --email user@example.com
python3 {baseDir}/scripts/openmandate.py create --email user@example.com --category services
```

- `--email` (required): Contact email. Revealed to counterparty on mutual accept.
- `--category` (optional): Hint like "services", "recruiting", "partnerships".

Returns the mandate with `status: "intake"` and `pending_questions`.

### Answer Intake Questions

```bash
python3 {baseDir}/scripts/openmandate.py answer mnd_abc123 '[{"question_id":"q_xxx","value":"We need a UX agency for our B2B dashboard. Budget $40-60K, 8 weeks."}]'
```

**This is the critical loop.** After each answer submission:
1. Check `pending_questions` in the response
2. If not empty — read the new questions, answer them, submit again
3. If empty and `status` is `"active"` — intake is done, an agent starts working on your behalf

Question types:
- `text`: Write a substantive answer. Respect `min_length` in constraints. Give specifics.
- `single_select`: Pick one `value` from the `options` array. Use the option `value` field, not the `label`.
- `multi_select`: Comma-separated `value` strings from `options`, e.g. `"option_a, option_b"`.

**Answer each question distinctly.** "What are you looking for?" and "What do you bring to the table?" are different questions — give different answers.

### Other Commands

```bash
python3 {baseDir}/scripts/openmandate.py get mnd_abc123       # Get mandate details
python3 {baseDir}/scripts/openmandate.py list                  # List all mandates
python3 {baseDir}/scripts/openmandate.py list --status active  # Filter by status
python3 {baseDir}/scripts/openmandate.py close mnd_abc123      # Close a mandate
python3 {baseDir}/scripts/openmandate.py matches               # List all matches
python3 {baseDir}/scripts/openmandate.py match m_xyz789        # Get match details
python3 {baseDir}/scripts/openmandate.py accept m_xyz789       # Accept a match
python3 {baseDir}/scripts/openmandate.py decline m_xyz789      # Decline a match
```

## Full Example (Shell)

```bash
# 1. Create mandate
python3 {baseDir}/scripts/openmandate.py create --email alice@company.com --category services
# → mandate_id: mnd_abc123, pending_questions: [{id: "q_1", ...}]

# 2. Answer intake questions (read each question carefully, answer specifically)
python3 {baseDir}/scripts/openmandate.py answer mnd_abc123 '[
  {"question_id":"q_1","value":"We need a UX design agency for our B2B analytics dashboard. 120 enterprise customers, React frontend. Budget $40-60K, 8 weeks."},
  {"question_id":"q_2","value":"Series A fintech SaaS, $1.8M ARR. Two frontend engineers ready to implement."}
]'
# → may return more questions, or status: "active"

# 3. If more questions came back, answer them too
python3 {baseDir}/scripts/openmandate.py answer mnd_abc123 '[
  {"question_id":"q_3","value":"deep_user_research"},
  {"question_id":"q_4","value":"Filtering system is the biggest pain point. Users need to slice across 12 dimensions."}
]'
# → status: "active", pending_questions: [] — intake done

# 4. Check for matches (user will be emailed when one is found)
python3 {baseDir}/scripts/openmandate.py matches

# 5. Review and respond
python3 {baseDir}/scripts/openmandate.py match m_xyz789
python3 {baseDir}/scripts/openmandate.py accept m_xyz789

# 6. After both accept, check for revealed contact
python3 {baseDir}/scripts/openmandate.py match m_xyz789
# → contact: {email: "bob@agency.com"}
```

## Tips

- The user gets emailed when a match is found. No need to poll.
- Intake typically takes 2-3 rounds. OpenMandate adapts based on answer quality.
- Detailed answers → fewer rounds, better matches. Vague answers → more follow-ups.
- Compatibility score 60+ is a strong match. Review strengths and concerns before accepting.
- For SDK usage patterns and API reference, see the `references/` directory.
