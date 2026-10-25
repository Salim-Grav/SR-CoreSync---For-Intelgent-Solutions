"""
S&R CoreSync For Intelligent Solutions - Publish Set Rules
===============================================================================
Single source of truth for "what gets published to GitHub Pages".

Both the local builder (`scripts/prepare_publish_set.py`) and the CI guard
(`scripts/validate_publish_set.py`) import this module, so the artifact that
CI verifies is byte-for-byte the artifact that CI publishes.

The site is a static GitHub Pages deployment. Everything in EXCLUDED_DIRS or
EXCLUDED_ROOT_FILES is server-side material that must never be reachable from
the public domain.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Directories that are never published (at any depth).
# ---------------------------------------------------------------------------
EXCLUDED_DIRS = {
    '.git', '_site', '.github', '.agents', '.vscode', '.zwork', 'api', 'config',
    'workers', 'scripts', 'dist', 'scratch', 'node_modules', '__pycache__'
}

# Any other dot-directory is tooling state (editor caches, agent artefacts), not
# site content. Excluding the whole class stops the next tool from leaking a
# screenshot into the published artefact the way .zwork nearly did.
ALLOWED_DOT_DIRS = {'.nojekyll', '.well-known'}

# ---------------------------------------------------------------------------
# Root level files that are never published.
# ---------------------------------------------------------------------------
EXCLUDED_ROOT_FILES = {
    '.env', '.env.example', '.env.local', '.gitignore', '.htaccess', 'serve.py'
}

# Root level file suffixes that are never published.
EXCLUDED_ROOT_SUFFIXES = ('.md', '.bat', '.url', '.ps1')

# ---------------------------------------------------------------------------
# Root level development artifacts that must never be published.
# They are internal component / e-mail / modal mock-ups and debug harnesses:
# no published page links to them, they carry no `noindex`, and publishing
# them exposed 13 stale duplicates of the real portals to search engines.
# ---------------------------------------------------------------------------
EXCLUDED_DEV_PAGES = {
    'debug_header.html',
    'preview_emblem_tuning.html',
    'preview_new_official_emblem.html',
    'preview_roi_modal.html',
    'preview-booking-modal.html',
    'preview-checkout.html',
    'preview-client-portal.html',
    'preview-comparison.html',
    'preview-header.html',
    'preview-invoice-quote.html',
    'preview-license-manager.html',
    'preview-software-modal.html',
    'preview-welcome-email.html',
}

# ---------------------------------------------------------------------------
# Global file suffixes that are never published.
# ---------------------------------------------------------------------------
EXCLUDED_SUFFIXES = ('.pyc',)

# ---------------------------------------------------------------------------
# Paths that must never appear in the published artifact.
# ---------------------------------------------------------------------------
FORBIDDEN_PUBLISHED = [
    'api', 'config', 'workers', 'scripts', 'dist',
    '.htaccess', '.env', '.env.example', '.github'
]

# ---------------------------------------------------------------------------
# Files that must always be present in the published artifact.
# ---------------------------------------------------------------------------
REQUIRED_PUBLISHED = [
    '_headers',
    '.nojekyll',
    # Mail clients fetch this to configure themselves. If it stops being
    # published, the only remaining discovery path is the CNAME that fails its
    # certificate check, so failing the build is the correct response.
    '.well-known/autoconfig/mail/config-v1.1.xml',
]


def is_excluded(rel_path):
    """Return True when the repository-relative path must not be published."""
    rel = rel_path.replace('\\', '/')
    parts = rel.split('/')
    name = parts[-1]

    if name in EXCLUDED_DIRS:
        return True
    if name.startswith('.') and name not in ALLOWED_DOT_DIRS and len(parts) > 1:
        return True
    if name.endswith(EXCLUDED_SUFFIXES):
        return True
    if len(parts) == 1:
        if name in EXCLUDED_ROOT_FILES:
            return True
        if name in EXCLUDED_DEV_PAGES:
            return True
        if name.lower().endswith(EXCLUDED_ROOT_SUFFIXES):
            return True
    return False


def iter_publish_files(root=None):
    """Yield every repository-relative path that belongs to the publish set."""
    base = root or ROOT
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS)
        rel_dir = os.path.relpath(dirpath, base).replace('\\', '/')
        if rel_dir == '.':
            rel_dir = ''
        for name in sorted(filenames):
            rel = (rel_dir + '/' + name) if rel_dir else name
            if is_excluded(rel):
                continue
            yield rel


def publish_set(root=None):
    return list(iter_publish_files(root))
