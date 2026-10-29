# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
=============================================================================
"""

"""
S&R CoreSync - GitHub Sovereign Branch Protection & Ruleset Configurator
========================================================================
Configures and verifies Branch Protection Rules and Repository Rulesets on the
`main` branch of `Salim-Grav/SR-CoreSync---For-Intelgent-Solutions` via the
official GitHub REST API, and exports the official importable GitHub Ruleset
JSON (`deploy/github-main-branch-ruleset.json`) enforcing Secret Scanning &
Publish Set Validation checks as documented in `.github/BRANCH_PROTECTION.md`.

Usage:
    python scripts/configure_branch_protection.py --apply
    python scripts/configure_branch_protection.py --status
    python scripts/configure_branch_protection.py --export-ruleset
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "Salim-Grav/SR-CoreSync---For-Intelgent-Solutions"
BRANCH = "main"
RULESET_PATH = os.path.join(ROOT, "deploy", "github-main-branch-ruleset.json")


def build_ruleset_spec():
    """Build the official GitHub Repository Ruleset specification for `main`."""
    return {
        "name": "S&R CoreSync Sovereign Main Branch Protection",
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [
            {
                "actor_id": 5,
                "actor_type": "RepositoryRole",
                "bypass_mode": "always",
            }
        ],
        "conditions": {
            "ref_name": {
                "include": ["~DEFAULT_BRANCH", "refs/heads/main"],
                "exclude": [],
            }
        },
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {"type": "required_linear_history"},
            {
                "type": "pull_request",
                "parameters": {
                    "required_approving_review_count": 1,
                    "dismiss_stale_reviews_on_push": True,
                    "require_code_owner_review": True,
                    "require_last_push_approval": False,
                    "required_review_thread_resolution": True,
                },
            },
            {
                "type": "required_status_checks",
                "parameters": {
                    "strict_required_status_checks_policy": True,
                    "do_not_enforce_on_create": False,
                    "required_status_checks": [
                        {"context": "validate"},
                        {
                            "context": "Audit Repository Credentials & Private Keys"
                        },
                    ],
                },
            },
        ],
    }


def export_ruleset_json():
    spec = build_ruleset_spec()
    try:
        os.makedirs(os.path.dirname(RULESET_PATH), exist_ok=True)
        with open(RULESET_PATH, "w", encoding="utf-8") as fh:
            json.dump(spec, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"[Ruleset] Exported official GitHub Ruleset JSON -> {RULESET_PATH}")
    except PermissionError:
        pass
    return spec


def load_github_token(explicit_token=None):
    """Retrieve GITHUB_TOKEN from CLI flag, environment, git credential manager, or .env."""
    if explicit_token and explicit_token.strip():
        return explicit_token.strip()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and token.strip():
        return token.strip()

    gcm_exe = r"C:\Program Files\Git\ucrt64\bin\git-credential-manager.exe"
    if os.path.isfile(gcm_exe):
        try:
            env = dict(os.environ)
            env["GIT_TERMINAL_PROMPT"] = "0"
            env["GCM_INTERACTIVE"] = "never"
            env["PATH"] = (
                r"C:\Program Files\Git\ucrt64\bin;C:\Program Files\Git\cmd;C:\Program Files\Git\usr\bin;"
                + env.get("PATH", "")
            )
            accts_proc = subprocess.run(
                [gcm_exe, "github", "list"],
                capture_output=True,
                timeout=5,
                cwd=ROOT,
                env=env,
            )
            accts = [
                a.strip()
                for a in accts_proc.stdout.decode("utf-8", errors="ignore").splitlines()
                if a.strip()
            ]
            accts = ["Salim-Grav"] + [a for a in accts if a != "Salim-Grav"]
            for acct in accts:
                proc = subprocess.run(
                    [gcm_exe, "get"],
                    input=f"protocol=https\nhost=github.com\nusername={acct}\n\n".encode("utf-8"),
                    capture_output=True,
                    timeout=5,
                    cwd=ROOT,
                    env=env,
                )
                out = proc.stdout.decode("utf-8", errors="ignore")
                for line in out.splitlines():
                    if line.startswith("password="):
                        val = line.split("=", 1)[1].strip()
                        if val:
                            print(
                                f"[Auth] Loaded GitHub credential via GCM for {acct} (prefix: {val[:4]}...)"
                            )
                            return val
        except Exception:
            pass

    env_path = os.path.join(ROOT, ".env")
    if os.path.isfile(env_path):
        with open(env_path, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                s = line.strip()
                if not s or s.startswith("#") or "=" not in s:
                    continue
                k, v = s.split("=", 1)
                if k.strip() in ("GITHUB_TOKEN", "GH_TOKEN"):
                    val = v.strip().strip('"').strip("'")
                    if val and not val.startswith("your_") and "xxx" not in val.lower():
                        print(
                            f"[Auth] Loaded GitHub token from .env (prefix: {val[:10]}...)"
                        )
                        return val

    return None


def gh_api(method, path, token, payload=None):
    url = f"https://api.github.com{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "SR-CoreSync-Sovereign-Governance/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="ignore")
        try:
            return exc.code, json.loads(err_body)
        except Exception:
            return exc.code, {"message": err_body}
    except Exception as exc:
        return 0, {"message": str(exc)}


def discover_check_contexts(token):
    status, data = gh_api("GET", f"/repos/{REPO}/commits/{BRANCH}/check-runs", token)
    contexts = []
    if status == 200 and isinstance(data, dict):
        for cr in data.get("check_runs", []):
            name = cr.get("name")
            if name and name not in contexts:
                contexts.append(name)
    for req_ctx in ("validate", "Audit Repository Credentials & Private Keys"):
        if req_ctx not in contexts:
            contexts.append(req_ctx)
    return contexts


def apply_branch_protection(token, strict_pr=True):
    print("=" * 76)
    print(f"S&R CoreSync - Configuring Cloud Branch Protection on {REPO} ({BRANCH})")
    print("=" * 76)

    export_ruleset_json()
    contexts = discover_check_contexts(token)
    print(f"Enforced CI Status Check Contexts on `{BRANCH}`: {contexts}")

    protection_payload = {
        "required_status_checks": {
            "strict": True,
            "contexts": [
                "validate",
                "Audit Repository Credentials & Private Keys",
            ],
        },
        "enforce_admins": True,
        "required_pull_request_reviews": (
            {
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": True,
                "required_approving_review_count": 1,
            }
            if strict_pr
            else None
        ),
        "restrictions": None,
        "required_linear_history": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": True,
    }

    status, resp = gh_api(
        "PUT",
        f"/repos/{REPO}/branches/{BRANCH}/protection",
        token,
        protection_payload,
    )
    print(f"PUT /repos/{REPO}/branches/{BRANCH}/protection -> HTTP {status}")

    if status == 200:
        print("✅ Classic Branch Protection applied successfully on GitHub Cloud!")
        sig_status, _ = gh_api(
            "POST",
            f"/repos/{REPO}/branches/{BRANCH}/protection/required_signatures",
            token,
        )
        print(f"POST .../protection/required_signatures -> HTTP {sig_status}")
        return status, resp

    # Also attempt Repository Rulesets API
    rs_status, rs_resp = gh_api(
        "POST",
        f"/repos/{REPO}/rulesets",
        token,
        build_ruleset_spec(),
    )
    print(f"POST /repos/{REPO}/rulesets -> HTTP {rs_status}")
    if rs_status in (200, 201):
        print("✅ GitHub Repository Ruleset applied successfully on GitHub Cloud!")
        return rs_status, rs_resp

    print(f"Response detail: {json.dumps(resp, indent=2)}")
    return status, resp


def inspect_status(token):
    print("=" * 76)
    print(f"S&R CoreSync - Auditing Live GitHub Branch Protection Status ({REPO})")
    print("=" * 76)

    # Public repo metadata can also be queried without token if token is expired
    status_repo, repo_info = gh_api("GET", f"/repos/{REPO}", token)
    if status_repo == 401:
        status_repo, repo_info = gh_api("GET", f"/repos/{REPO}", None)
    print(
        f"Repository check: HTTP {status_repo} | Visibility: {repo_info.get('visibility')} | Default branch: {repo_info.get('default_branch')}"
    )

    status_br, br_info = gh_api("GET", f"/repos/{REPO}/branches/{BRANCH}", token)
    if status_br == 401:
        status_br, br_info = gh_api("GET", f"/repos/{REPO}/branches/{BRANCH}", None)
    print(f"Branch `{BRANCH}` protected flag: {br_info.get('protected')}")

    status_prot, prot_info = gh_api(
        "GET", f"/repos/{REPO}/branches/{BRANCH}/protection", token
    )
    print(f"GET /branches/{BRANCH}/protection -> HTTP {status_prot}")
    if status_prot == 200:
        rsc = prot_info.get("required_status_checks", {})
        rpr = prot_info.get("required_pull_request_reviews", {})
        print(f"  - Strict Up-to-Date Branches: {rsc.get('strict')}")
        print(f"  - Required Status Checks:     {rsc.get('contexts')}")
        print(
            f"  - Enforce Admins:             {prot_info.get('enforce_admins', {}).get('enabled')}"
        )
        print(
            f"  - Require Linear History:     {prot_info.get('required_linear_history', {}).get('enabled')}"
        )
        print(
            f"  - Allow Force Pushes:         {prot_info.get('allow_force_pushes', {}).get('enabled')}"
        )
        print(
            f"  - Allow Deletions:            {prot_info.get('allow_deletions', {}).get('enabled')}"
        )
        if rpr:
            print(
                f"  - Require Code Owner Reviews: {rpr.get('require_code_owner_reviews')}"
            )
            print(f"  - Dismiss Stale Approvals:    {rpr.get('dismiss_stale_reviews')}")
            print(
                f"  - Required Approvals Count:   {rpr.get('required_approving_review_count')}"
            )
    else:
        print(f"  - Message: {prot_info.get('message')}")

    return status_prot, prot_info


def main():
    parser = argparse.ArgumentParser(
        description="Configure GitHub Branch Protection Rules"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply Branch Protection Rules to GitHub",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check current Branch Protection Rules on GitHub",
    )
    parser.add_argument(
        "--export-ruleset",
        action="store_true",
        help="Export importable GitHub Ruleset JSON to deploy/github-main-branch-ruleset.json",
    )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="Explicit GitHub Personal Access Token (Administration: Read & Write)",
    )
    parser.add_argument(
        "--allow-direct-push",
        action="store_true",
        help="Require status checks and block force-push/deletion without requiring PRs for solo owner pushes",
    )
    args = parser.parse_args()

    export_ruleset_json()
    if args.export_ruleset and not args.apply and not args.status:
        return 0

    token = load_github_token(args.token)
    if not token:
        print(
            "ERROR: No GitHub token found in environment, .env, or git credential manager."
        )
        return 2

    if args.apply:
        st, _ = apply_branch_protection(token, strict_pr=not args.allow_direct_push)
        inspect_status(token)
        return 0 if st in (200, 201) else 1

    st, _ = inspect_status(token)
    return 0 if st == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
