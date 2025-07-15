#!/bin/bash

# Function to clean up git lock files
cleanup_git_locks() {
    echo "🧹 Cleaning up Git lock files..."
    if [ -f ".git/index.lock" ]; then
        rm -f .git/index.lock
        echo "✅ Removed .git/index.lock"
    fi
    if [ -f ".git/refs/heads/main.lock" ]; then
        rm -f .git/refs/heads/main.lock
        echo "✅ Removed .git/refs/heads/main.lock"
    fi
}

# Clean up any existing lock files
cleanup_git_locks

# Check if git repo already exists
if [ -d ".git" ]; then
    echo "📁 Git repository already exists. Checking status..."
    git status
else
    echo "🚀 Initializing new Git repository..."
    git init
fi

# Configure git if not already configured
if [ -z "$(git config user.name)" ]; then
    echo "⚙️  Please configure Git:"
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email
    git config user.name "$git_name"
    git config user.email "$git_email"
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Check if there are any changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit."
else
    echo "💾 Committing changes..."
    git commit -m "Initial commit: SunScore solar data collector" || {
        echo "❌ Commit failed. Cleaning up and retrying..."
        cleanup_git_locks
        git commit -m "Initial commit: SunScore solar data collector"
    }
fi

# Check if remote already exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 Remote 'origin' already exists:"
    git remote get-url origin
    read -p "Do you want to update it? (y/N): " update_remote
    if [[ $update_remote =~ ^[Yy]$ ]]; then
        read -p "Enter new repository URL: " repo_url
        git remote set-url origin "$repo_url"
    fi
else
    echo "🔗 Please create a repository on GitHub and enter the URL:"
    read -p "Repository URL: " repo_url
    git remote add origin "$repo_url"
fi

# Create main branch if it doesn't exist
if ! git show-ref --verify --quiet refs/heads/main; then
    echo "🌿 Creating main branch..."
    git branch -M main
fi

# Push to remote
echo "⬆️  Pushing to remote repository..."
git push -u origin main || {
    echo "❌ Push failed. This might be because:"
    echo "   1. The repository doesn't exist on GitHub"
    echo "   2. You don't have push permissions"
    echo "   3. Authentication issues"
    echo ""
    echo "💡 Manual steps to resolve:"
    echo "   1. Create the repository on GitHub first"
    echo "   2. Make sure you're authenticated (use 'gh auth login' or set up SSH keys)"
    echo "   3. Try: git push -u origin main"
}

echo ""
echo "✅ Setup complete! Don't forget to:"
echo "1. Set environment variables for NSRDB_API_KEY and USER_EMAIL"
echo "2. Add your uszips.csv file to the project directory"
echo "3. Review the README.md for usage instructions"
