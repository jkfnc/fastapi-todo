# Branch Protection Setup

To ensure all PRs pass tests before merging, configure branch protection rules on GitHub:

## Steps to Enable Branch Protection

1. Go to your repository on GitHub: https://github.com/jkfnc/fastapi-todo
2. Navigate to **Settings** → **Branches**
3. Click **Add rule** under "Branch protection rules"
4. Configure the following:

### Branch name pattern
- Enter: `master` (or `main` if you rename the branch)

### Protection Settings
- ✅ **Require a pull request before merging**
  - ✅ Require approvals (optional, set to 1)
  - ✅ Dismiss stale pull request approvals when new commits are pushed
  
- ✅ **Require status checks to pass before merging**
  - ✅ Require branches to be up to date before merging
  - Search and select these status checks:
    - `test (3.9)`
    - `test (3.10)`
    - `test (3.11)`
    - `test (3.12)`

- ✅ **Require conversation resolution before merging** (optional)

- ✅ **Include administrators** (optional, but recommended)

5. Click **Create** to save the rule

## Result

After enabling these rules:
- All pull requests will automatically run tests via GitHub Actions
- PRs can only be merged if all tests pass
- Direct pushes to master/main will be prevented (except for administrators if not included)

## Testing the Workflow

1. Create a new branch: `git checkout -b test-feature`
2. Make changes and push
3. Create a PR on GitHub
4. Watch the tests run automatically
5. PR can only be merged once all checks pass