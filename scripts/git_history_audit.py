import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

PURGE_PATHS = [
    ".env.vault",
    "chat_history.txt",
    "sr_agent_sessions.db",
    "sr_rag_knowledge.db",
    "server_test.log",
    "server_test_err.log",
    "srv8002.log",
    "srv8002_err.log",
    "sr_subagent_audit.log",
    "uploads"
]

print("=" * 70)
print(" S&R CoreSync — Git History Audit (P0-4 Purge Targets)")
print("=" * 70)

# Get all objects in git history
try:
    p = subprocess.run(
        ["git", "rev-list", "--objects", "--all"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True
    )
except Exception as e:
    print(f"Error running git rev-list: {e}")
    sys.exit(1)

matches = set()
for line in p.stdout.splitlines():
    parts = line.strip().split(maxsplit=1)
    if len(parts) == 2:
        sha, path = parts
        for target in PURGE_PATHS:
            if path == target or path.startswith(target + "/"):
                matches.add(path)

print(f"\nFound {len(matches)} historical object paths matching purge targets:")
for m in sorted(list(matches))[:40]:
    print(f"  • MATCH: {m}")

if len(matches) > 40:
    print(f"  ... and {len(matches) - 40} more.")

print("\nStatus in current working tree (.gitignore protection):")
for p in PURGE_PATHS:
    check = subprocess.run(["git", "check-ignore", "-v", p], capture_output=True, text=True)
    ignored = check.returncode == 0
    print(f"  • {p:<25}: {'IGNORED (Protected) ✅' if ignored else 'NOT IGNORED ⚠️'}")

print("=" * 70)
