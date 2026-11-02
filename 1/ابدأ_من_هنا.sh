#!/usr/bin/env bash
# =====================================================================
#   SR-CoreSync — Automatic Updater (does everything on your behalf)
#   Put this file in the SAME folder as the two ZIP files, then run it.
# =====================================================================
set -u

REPO_URL="https://github.com/Salim-Grav/SR-CoreSync---For-Intelgent-Solutions.git"
UPLOAD_PAGE="https://github.com/Salim-Grav/SR-CoreSync---For-Intelgent-Solutions/upload/main"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "====================================================="
echo "  SR-CoreSync Automatic Updater"
echo "  (updates your project + GitHub with one approval)"
echo "====================================================="
echo

# ---------- 1) make sure both packages are available ----------
for PKG in SR-CoreSync_P0_Patches SR-CoreSync_i18n_Fixes; do
    if [ ! -d "$HERE/$PKG" ] && [ -f "$HERE/$PKG.zip" ]; then
        echo "[prepare] Extracting $PKG.zip ..."
        if command -v unzip >/dev/null 2>&1; then
            unzip -q -o "$HERE/$PKG.zip" -d "$HERE"
        else
            python3 -m zipfile -e "$HERE/$PKG.zip" "$HERE/"
        fi
    fi
done
if [ ! -d "$HERE/SR-CoreSync_P0_Patches" ] || [ ! -d "$HERE/SR-CoreSync_i18n_Fixes" ]; then
    echo "[ERROR] I could not find the two packages."
    echo "        Keep this file in the same folder as the two ZIP files."
    echo "        (macOS: a folder may appear inside another folder -"
    echo "         move this file next to the two ZIPs and try again)"
    exit 1
fi
echo "[prepare] Both packages found and ready."
echo

# ---------- 2) decide WHERE to apply ----------
echo "Where is your project?"
echo "  - Drag your existing project folder into this window and press Enter,"
echo "  - or just press ENTER to download a fresh copy from GitHub."
read -rp "> " TARGET
TARGET="${TARGET%\"}"; TARGET="${TARGET#\"}"; TARGET="${TARGET%/}"
if [ -z "$TARGET" ]; then
    if ! command -v git >/dev/null 2>&1; then
        echo
        echo "[INFO] git is not installed on this machine, so I cannot download"
        echo "       or push automatically. I will prepare a ready upload folder"
        echo "       for the browser method instead (very easy, 3 clicks)."
        GIT_MISSING=1
        TARGET="$HERE/updated-project"
    else
        TARGET="$HERE/SR-CoreSync-project"
        if [ ! -d "$TARGET" ]; then
            echo "[download] Downloading your project from GitHub ..."
            git clone --quiet "$REPO_URL" "$TARGET" || {
                echo "[ERROR] Download failed. Check your internet connection."; exit 1; }
        fi
    fi
fi
if [ ! -d "$TARGET" ]; then
    echo "[ERROR] Folder not found: $TARGET"
    exit 1
fi
echo "[target] $TARGET"
echo

# ---------- 3) apply both packages ----------
echo "[apply 1/2] Copying security update files (P0) ..."
cp -R "$HERE/SR-CoreSync_P0_Patches/full_files/." "$TARGET/"
echo "[apply 2/2] Copying translation files (all languages) ..."
cp -R "$HERE/SR-CoreSync_i18n_Fixes/full_files/." "$TARGET/"
echo "            [OK] All files are in place."
echo

# ---------- 4) send to GitHub ----------
if [ "${GIT_MISSING:-0}" = "1" ]; then
    mkdir -p "$HERE/GITHUB_UPLOAD"
    cp -R "$HERE/SR-CoreSync_P0_Patches/full_files/." "$HERE/GITHUB_UPLOAD/"
    cp -R "$HERE/SR-CoreSync_i18n_Fixes/full_files/." "$HERE/GITHUB_UPLOAD/"
    echo "====================================================="
    echo "  LAST STEP (3 clicks, I opened the page for you):"
    echo "  1. A browser page opened: 'Upload files' on GitHub."
    echo "  2. Drag EVERYTHING you see inside the folder"
    echo "     GITHUB_UPLOAD  into that page."
    echo "  3. Click 'Commit changes'. Done!"
    echo "====================================================="
    (open "$UPLOAD_PAGE" 2>/dev/null || xdg-open "$UPLOAD_PAGE" 2>/dev/null) &
    (open "$HERE/GITHUB_UPLOAD" 2>/dev/null || xdg-open "$HERE/GITHUB_UPLOAD" 2>/dev/null) &
    exit 0
fi

if [ -d "$TARGET/.git" ]; then
    cd "$TARGET"
    echo "[github] Saving changes..."
    git add -A
    git commit -m "Apply SR-CoreSync updates: P0 security patches + full i18n translation fixes" || true
    echo
    echo "[github] Sending to GitHub..."
    echo "         A browser window may open asking you to log in."
    echo "         >>> Give your approval there - nothing is sent without it. <<<"
    echo
    if git push; then
        echo "         [OK] GitHub is now up to date! Refresh the page to see it."
    else
        echo "         [NOTE] Push did not finish - your copy may be behind"
        echo "                GitHub. Run:  git pull   then   git push"
    fi
else
    echo "[github] This folder has no git repository, so nothing was sent."
    echo "         Disk files were updated - enough if this is your live folder."
fi

echo
echo "====================================================="
echo "  All done. You can close this window."
echo "====================================================="
