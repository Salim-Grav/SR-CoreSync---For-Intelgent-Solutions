@echo off
:: يُنفَّذ هذا الملف لإزالة Git Worktrees الوهمية
set "W1=d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project\.git\worktrees\copilot-prewarm-studious-guide"
set "W2=d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project\.git\worktrees\salim-grav-animated-memory"

echo Removing worktrees...
rd /s /q "%W1%" 2>nul
rd /s /q "%W2%" 2>nul
echo Done.
