#!/usr/bin/env bash
# ==============================================================================
# S&R CoreSync - Quick Handover Sync Script for ZaiChat Desktop (Linux Environment)
# ==============================================================================
set -e

ACTION=${1:-menu}

if [ "$ACTION" = "pull" ]; then
    echo "📥 Pulling latest updates from GitHub..."
    git pull origin main
    echo "✅ Up to date with latest Antigravity IDE changes!"
elif [ "$ACTION" = "push" ]; then
    echo "📤 Pushing updates to GitHub..."
    git add -A
    git commit -m "feat: updates completed in ZaiChat Desktop" || true
    git push origin main
    echo "✅ Pushed to GitHub successfully!"
else
    echo "=========================================================="
    echo "   S&R CoreSync - ZaiChat Handover Tool (Linux/VM)       "
    echo "=========================================================="
    echo "1) Pull latest from GitHub (when starting session)"
    echo "2) Push all to GitHub     (before switching to Antigravity)"
    echo "3) Check Git Status"
    echo "4) Exit"
    echo "=========================================================="
    read -p "Select option [1-4]: " choice
    case $choice in
        1)
            git pull origin main
            ;;
        2)
            git add -A
            git commit -m "feat: updates completed in ZaiChat Desktop" || true
            git push origin main
            ;;
        3)
            git status
            ;;
        *)
            exit 0
            ;;
    esac
fi
