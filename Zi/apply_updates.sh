#!/usr/bin/env bash
# ==================================================
#  SR-CoreSync - Apply Updates (one command)
#  Usage:
#    ./apply_updates.sh /path/to/your/project-folder
#    (or run it without arguments and it will ask you)
# ==================================================
set -u

SRC="$(cd "$(dirname "$0")" && pwd)/full_files"
if [ ! -d "$SRC" ]; then
    echo '[ERROR] "full_files" folder not found next to this script.'
    echo '        Keep this script inside the extracted package folder.'
    exit 1
fi

REPO="${1:-}"
if [ -z "$REPO" ]; then
    read -rp "Enter the full path to your project folder: " REPO
fi
REPO="${REPO%/}"
if [ -z "$REPO" ] || [ ! -d "$REPO" ]; then
    echo "[ERROR] Project folder not found: $REPO"
    exit 1
fi

echo
echo "[1/2] Copying updated files into: $REPO"
cp -R "$SRC"/. "$REPO"/
echo "      [OK] All files copied. Existing files with the same"
echo "           names were overwritten - this is expected."
echo

if [ -d "$REPO/.git" ]; then
    echo "[2/2] Git repository detected. Saving changes..."
    cd "$REPO"
    git add -A
    git commit -m "Apply SR-CoreSync updates: P0 security patches + full i18n translation fixes" || true
    echo
    echo "      Now pushing to GitHub..."
    echo "      A browser window may open asking you to log in."
    echo "      >>> Approve it there - nothing uploads without your OK. <<<"
    echo
    if git push; then
        echo "      [OK] Successfully pushed to GitHub!"
    else
        echo "      [NOTE] Push did not finish (your copy may be behind"
        echo "             GitHub). Run:  git pull  then  git push"
    fi
else
    echo "[2/2] No .git folder found here, so nothing was sent to"
    echo "      GitHub. Disk files were updated - that is all you need"
    echo "      if this copy is your live website folder."
fi

echo
echo "=================================================="
echo "  Done."
echo "=================================================="
