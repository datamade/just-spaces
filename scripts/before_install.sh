#!/bin/bash

# Cause the entire deployment to fail if something in this script exits with
# a non-zero exit code. This will make debugging your deployment much simpler.
# Read more about this here: http://redsymbol.net/articles/unofficial-bash-strict-mode/

set -euo pipefail

# Make directory for project
mkdir -p /home/datamade/just-spaces

# Decrypt files encrypted with blackbox
apt-get update
apt-get install -y gnupg2
cd /opt/codedeploy-agent/deployment-root/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/deployment-archive/ && chown -R datamade.datamade . && sudo -H -u datamade GPG=gpg2 blackbox_postdeploy
