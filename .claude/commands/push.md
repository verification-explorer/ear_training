Stage all changed files, create a detailed commit, and push to GitHub.

Steps:
1. Run `git status` to see what files changed
2. Run `git diff` to understand what actually changed in the code
3. Based on the diff, write a meaningful commit message following this format:
   - First line: short summary (max 50 chars), e.g. "Add factorial operation to core and CLI"
   - Blank line
   - Bullet points describing what changed and why
4. Run `git add .`
5. Run `git commit -m "<your generated message>"`
6. Run `git push origin main`
7. Confirm the push succeeded and print the commit hashclaude