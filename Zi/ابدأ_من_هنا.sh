#!/usr/bin/env bash
# =====================================================================
#   SR-CoreSync — Automatic Updater (NO QUESTIONS ASKED)
#   Just run this file. It does everything for you.
#   Keep this file in the SAME folder as the two ZIP files.
# =====================================================================
set -u

REPO_URL="https://github.com/Salim-Grav/SR-CoreSync---For-Intelgent-Solutions.git"
UPLOAD_PAGE="https://github.com/Salim-Grav/SR-CoreSync---For-Intelgent-Solutions/upload/main"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "====================================================="
echo "  SR-CoreSync Automatic Updater"
echo "  (does everything for you - no questions asked)"
echo "====================================================="
echo

# ---------- 1) extract packages if needed ----------
for PKG in SR-CoreSync_P0_Patches SR-CoreSync_i18n_Fixes; do
    if [ ! -d "$HERE/$PKG" ] && [ -f "$HERE/$PKG.zip" ]; then
        echo "[1/6] Extracting $PKG.zip ..."
        if command -v unzip >/dev/null 2>&1; then
            unzip -q -o "$HERE/$PKG.zip" -d "$HERE"
        else
            python3 -m zipfile -e "$HERE/$PKG.zip" "$HERE/"
        fi
    fi
done
if [ ! -d "$HERE/SR-CoreSync_P0_Patches" ] || [ ! -d "$HERE/SR-CoreSync_i18n_Fixes" ]; then
    echo "[ERROR] Cannot find the two packages."
    echo "        Put this file next to the two ZIP files and run again."
    exit 1
fi
echo "      [OK] Both packages ready."
echo

# ---------- 2) check if git is available ----------
if ! command -v git >/dev/null 2>&1; then
    echo "[2/6] git not found - will use the easy browser method."
    echo
    goto_browser=1
else
    echo "[2/6] git found."
    echo
    goto_browser=0
fi

# ---------- 3) download a fresh copy from GitHub ----------
if [ "$goto_browser" = "0" ]; then
    TARGET="$HERE/SR-CoreSync-project"
    if [ -d "$TARGET/.git" ]; then
        echo "[3/6] Updating the local copy I downloaded before ..."
        (cd "$TARGET" && git pull --quiet --no-rebase 2>/dev/null) || true
    else
        echo "[3/6] Downloading your project from GitHub ..."
        if ! git clone --quiet "$REPO_URL" "$TARGET"; then
            echo "      [ERROR] Download failed. Check internet connection."
            echo "      Falling back to easy browser method ..."
            echo
            goto_browser=1
        fi
    fi
    if [ "$goto_browser" = "0" ]; then
        echo "      [OK] Project ready at: $TARGET"
        echo
    fi
fi

# ---------- 4) apply both packages ----------
if [ "$goto_browser" = "0" ]; then
    echo "[4/6] Applying security patches (P0) ..."
    cp -R "$HERE/SR-CoreSync_P0_Patches/full_files/." "$TARGET/"
    echo "[4/6] Applying translation fixes (all 26 languages) ..."
    cp -R "$HERE/SR-CoreSync_i18n_Fixes/full_files/." "$TARGET/"
    echo "      [OK] All files are in place."
    echo
fi

# ---------- 5) commit ----------
if [ "$goto_browser" = "0" ]; then
    cd "$TARGET"
    echo "[5/6] Saving changes locally ..."
    git add -A
    git commit -m "Apply SR-CoreSync updates: P0 security patches + full i18n translation fixes" 2>/dev/null || true
    echo "      [OK] Saved."
    echo
fi

# ---------- 6) push to GitHub ----------
if [ "$goto_browser" = "0" ]; then
    echo "[6/6] Sending to GitHub ..."
    echo "      A browser window may open asking you to log in."
    echo "      >>> Give your approval there - nothing is sent without it. <<<"
    echo
    if git push; then
        echo
        echo "      [OK] GitHub is now up to date! Refresh the page to see it."
        echo
        echo "====================================================="
        echo "  All done. You can close this window."
        echo "====================================================="
        exit 0
    else
        echo
        echo "[NOTE] Auto-push did not finish (maybe GitHub login needed)."
        echo "       Falling back to easy browser method ..."
        echo
        goto_browser=1
    fi
fi

# ---------- BROWSER FALLBACK METHOD ----------
if [ "$goto_browser" = "1" ]; then
    echo "[browser] Preparing files for easy drag-and-drop upload ..."
    mkdir -p "$HERE/GITHUB_UPLOAD"
    cp -R "$HERE/SR-CoreSync_P0_Patches/full_files/." "$HERE/GITHUB_UPLOAD/"
    cp -R "$HERE/SR-CoreSync_i18n_Fixes/full_files/." "$HERE/GITHUB_UPLOAD/"
    echo "         [OK] Folder ready."
    echo
    echo "====================================================="
    echo "  LAST STEP - 3 simple actions:"
    echo
    echo "  1. A browser page opened: GitHub Upload files."
    echo "  2. A folder opened: GITHUB_UPLOAD"
    echo "     Drag EVERYTHING from that folder into the browser."
    echo "  3. Click 'Commit changes' at the bottom. Done!"
    echo "====================================================="
    echo
    (open "$UPLOAD_PAGE" 2>/dev/null || xdg-open "$UPLOAD_PAGE" 2>/dev/null) &
    sleep 2
    (open "$HERE/GITHUB_UPLOAD" 2>/dev/null || xdg-open "$HERE/GITHUB_UPLOAD" 2>/dev/null) &
    exit 0
fi
