#!/bin/bash

# Claude Code Status Line Script  
# Modern zsh-style prompt: path git:(branch) ➜

# Read input from stdin
input=$(cat)

# Extract current directory from JSON input, fallback to pwd
if command -v jq >/dev/null 2>&1; then
    current_dir=$(echo "$input" | jq -r '.workspace.current_dir // empty' 2>/dev/null)
fi

# Fallback to pwd if jq is not available or extraction failed
if [[ -z "$current_dir" ]]; then
    current_dir=$(pwd)
fi

# Convert absolute path to relative with ~ for home directory
display_path="${current_dir/#$HOME/~}"

# Abbreviate long paths (keep first and last 2 directories)
if [[ $(echo "$display_path" | tr '/' '\n' | wc -l) -gt 4 ]]; then
    first_part=$(echo "$display_path" | cut -d'/' -f1-2)
    last_part=$(echo "$display_path" | rev | cut -d'/' -f1-2 | rev)
    display_path="${first_part}/.../${last_part}"
fi

# Get git status if in a git repository
git_info=""
if git rev-parse --git-dir >/dev/null 2>&1; then
    # Skip git operations if index is locked to avoid hanging
    if [[ ! -f "$(git rev-parse --git-dir)/index.lock" ]]; then
        branch_name=$(git symbolic-ref --quiet --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)
        if [[ -n "$branch_name" ]]; then
            # Check for git status indicators
            git_status=""
            if ! git diff-index --quiet HEAD -- 2>/dev/null; then
                git_status="*"  # Modified files
            elif ! git diff --cached --quiet 2>/dev/null; then
                git_status="+"  # Staged files
            fi
            git_info=" git:($branch_name$git_status)"
        fi
    fi
fi

# Get username
username=$(whoami)

# Output the status line in custom format
if [[ -n "$git_info" ]]; then
    # In git repo: $user -> $pwd ($branch) $
    branch_only=$(echo "$git_info" | sed 's/ git:(\(.*\))/\1/' | sed 's/[*+]//')
    printf "%s -> %s (%s) $" "$username" "$display_path" "$branch_only"
else
    # Not in git repo: $user -> $pwd $
    printf "%s -> %s $" "$username" "$display_path"
fi