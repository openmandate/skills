#!/usr/bin/env python3
"""OpenMandate CLI helper for OpenClaw agents.

Stdlib-only (no pip dependencies). Agents call:
    python3 openmandate.py <command> [args]

Requires OPENMANDATE_API_KEY env var. Optionally override
OPENMANDATE_BASE_URL (default: https://api.openmandate.ai).
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

VERSION = "0.1.0"
USER_AGENT = f"openmandate-openclaw/{VERSION}"
DEFAULT_BASE_URL = "https://api.openmandate.ai"
API_KEY_ENV = "OPENMANDATE_API_KEY"
BASE_URL_ENV = "OPENMANDATE_BASE_URL"


# ── Helpers ──────────────────────────────────────────────────────────


def _get_api_key() -> str:
    key = os.environ.get(API_KEY_ENV, "")
    if not key:
        _die(f"Missing {API_KEY_ENV} environment variable.")
    return key


def _get_base_url() -> str:
    return os.environ.get(BASE_URL_ENV, DEFAULT_BASE_URL).rstrip("/")


def _die(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def _request(method: str, path: str, body: dict | None = None, params: dict | None = None) -> dict:
    """Make an HTTP request to the OpenMandate API and return parsed JSON."""
    base = _get_base_url()
    url = f"{base}{path}"

    if params:
        query = "&".join(f"{k}={urllib.request.quote(str(v))}" for k, v in params.items() if v is not None)
        if query:
            url = f"{url}?{query}"

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {_get_api_key()}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", USER_AGENT)

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp_body = resp.read().decode("utf-8")
            if not resp_body:
                return {}
            return json.loads(resp_body)
    except urllib.error.HTTPError as exc:
        try:
            err_body = json.loads(exc.read().decode("utf-8"))
            err = err_body.get("error", {})
            code = err.get("code", "UNKNOWN")
            message = err.get("message", exc.reason)
            _die(f"[{exc.code}] {code}: {message}")
        except (json.JSONDecodeError, ValueError):
            _die(f"[{exc.code}] {exc.reason}")
    except urllib.error.URLError as exc:
        _die(f"Connection failed: {exc.reason}")

    return {}  # unreachable, but keeps linters happy


def _print_json(data: dict | list) -> None:
    print(json.dumps(data, indent=2))


# ── Commands ─────────────────────────────────────────────────────────


def cmd_create(args: argparse.Namespace) -> None:
    body: dict = {}
    if args.category:
        body["category"] = args.category
    body["contact"] = {"email": args.email}
    result = _request("POST", "/v1/mandates", body=body)
    _print_json(result)


def cmd_get(args: argparse.Namespace) -> None:
    result = _request("GET", f"/v1/mandates/{args.mandate_id}")
    _print_json(result)


def cmd_list(args: argparse.Namespace) -> None:
    params: dict = {}
    if args.status:
        params["status"] = args.status
    if args.limit:
        params["limit"] = args.limit
    result = _request("GET", "/v1/mandates", params=params)
    _print_json(result)


def cmd_answer(args: argparse.Namespace) -> None:
    try:
        answers = json.loads(args.answers_json)
    except json.JSONDecodeError as exc:
        _die(f"Invalid JSON for answers: {exc}")
        return  # unreachable

    if not isinstance(answers, list):
        _die("Answers must be a JSON array of objects with question_id and value.")
        return

    body = {"answers": answers}
    result = _request("POST", f"/v1/mandates/{args.mandate_id}/answers", body=body)
    _print_json(result)


def cmd_close(args: argparse.Namespace) -> None:
    result = _request("POST", f"/v1/mandates/{args.mandate_id}/close")
    _print_json(result)


def cmd_matches(args: argparse.Namespace) -> None:
    result = _request("GET", "/v1/matches")
    _print_json(result)


def cmd_match(args: argparse.Namespace) -> None:
    result = _request("GET", f"/v1/matches/{args.match_id}")
    _print_json(result)


def cmd_accept(args: argparse.Namespace) -> None:
    result = _request("POST", f"/v1/matches/{args.match_id}/accept")
    _print_json(result)


def cmd_decline(args: argparse.Namespace) -> None:
    result = _request("POST", f"/v1/matches/{args.match_id}/decline")
    _print_json(result)


# ── Argument Parser ──────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openmandate",
        description="OpenMandate CLI helper for OpenClaw agents.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    # create
    p_create = sub.add_parser("create", help="Create a new mandate")
    p_create.add_argument("--email", required=True, help="Contact email (revealed on mutual accept)")
    p_create.add_argument("--category", default=None, help="Optional category hint (e.g. services, recruiting)")
    p_create.set_defaults(func=cmd_create)

    # get
    p_get = sub.add_parser("get", help="Get a mandate by ID")
    p_get.add_argument("mandate_id", help="Mandate ID (e.g. mnd_xxx)")
    p_get.set_defaults(func=cmd_get)

    # list
    p_list = sub.add_parser("list", help="List mandates")
    p_list.add_argument("--status", default=None, help="Filter by status (active, intake, closed)")
    p_list.add_argument("--limit", type=int, default=None, help="Max results")
    p_list.set_defaults(func=cmd_list)

    # answer
    p_answer = sub.add_parser("answer", help="Submit answers to intake questions")
    p_answer.add_argument("mandate_id", help="Mandate ID")
    p_answer.add_argument("answers_json", help='JSON array: [{"question_id":"q_xxx","value":"..."}]')
    p_answer.set_defaults(func=cmd_answer)

    # close
    p_close = sub.add_parser("close", help="Close a mandate")
    p_close.add_argument("mandate_id", help="Mandate ID")
    p_close.set_defaults(func=cmd_close)

    # matches
    p_matches = sub.add_parser("matches", help="List all matches")
    p_matches.set_defaults(func=cmd_matches)

    # match
    p_match = sub.add_parser("match", help="Get a match by ID")
    p_match.add_argument("match_id", help="Match ID (e.g. m_xxx)")
    p_match.set_defaults(func=cmd_match)

    # accept
    p_accept = sub.add_parser("accept", help="Accept a match")
    p_accept.add_argument("match_id", help="Match ID")
    p_accept.set_defaults(func=cmd_accept)

    # decline
    p_decline = sub.add_parser("decline", help="Decline a match")
    p_decline.add_argument("match_id", help="Match ID")
    p_decline.set_defaults(func=cmd_decline)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
