from os import environ, path as ospath, remove
from subprocess import run as srun


# Retrieve the upstream repository and branch
UPSTREAM_REPO = "https://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@github.com/gitproman/storagebot"
UPSTREAM_BRANCH = "4th"

# Validate the repository URL
if not UPSTREAM_REPO:
    print("Error: UPSTREAM_REPO is missing! Exiting...")
    exit(1)

# Remove existing `.git` directory if it exists
if ospath.exists('.git'):
    srun(["rm", "-rf", ".git"])

# Initialize and update the repository
update = srun([
    "git init -q && "
    "git config --global user.email 'doc.adhikari@gmail.com' && "
    "git config --global user.name 'weebzone' && "
    "git add . && "
    "git commit -sm 'update' -q && "
    f"git remote add origin {UPSTREAM_REPO} && "
    "git fetch origin -q && "
    f"git reset --hard origin/{UPSTREAM_BRANCH} -q"
], shell=True)

# Provide feedback on the update process
if update.returncode == 0:
    print("Successfully updated with the latest commits!")
else:
    print("Error: Update failed! Please retry or check the upstream settings.")
