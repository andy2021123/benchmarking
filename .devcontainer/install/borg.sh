#!/bin/bash

mkdir -p /tmp/install
cd /tmp/install

# Clean up downloaded files at the end
cleanup() {
  cd - > /dev/null
  rm -rf /tmp/install
}
trap cleanup EXIT

# Define variables
VERSION="1.4.0"
GPG_FINGERPRINT="9F88FB52FAF7B393"

# Install Restic from GitHub releases
wget -q https://github.com/borgbackup/borg/releases/download/$VERSION/borg-linux-glibc236
wget -q https://github.com/borgbackup/borg/releases/download/$VERSION/borg-linux-glibc236.asc

# Import the GPG key
echo "Importing GPG key..."
gpg --recv-key "$GPG_FINGERPRINT" || {
  echo "Failed to download GPG key. Aborting."
  exit 1
}

# Verify GPG signature
echo "Verifying GPG signature..."
if gpg --verify borg-linux-glibc236.asc; then
  echo "Signature verification passed."
else
  echo "Signature verification failed! Aborting installation."
  exit 1
fi

# Make binary executable
chmod +x borg-linux-glibc236

# Move binary to /bin
echo "Installing restic binary to /bin..."
mv borg-linux-glibc236 /bin/borg

# Verify installation
echo "Verifying installation..."
if command -v borg >/dev/null; then
  echo "Borg $VERSION has been installed successfully!"
else
  echo "Borg installation failed or borg is not in PATH."
  exit 1
fi
