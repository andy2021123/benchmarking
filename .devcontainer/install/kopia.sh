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
VERSION="0.19.0"

# Install Restic from GitHub releases
wget -q https://github.com/kopia/kopia/releases/download/v"$VERSION"/kopia_"$VERSION"_linux_amd64.deb
wget -q https://github.com/kopia/kopia/releases/download/v"$VERSION"/checksums.txt
wget -q https://github.com/kopia/kopia/releases/download/v"$VERSION"/checksums.txt.sig

# Import the GPG key
echo "Importing GPG key..."
curl -s https://kopia.io/signing-key | gpg --import - || {
  echo "Failed to download GPG key. Aborting."
  exit 1
}

# Verify GPG signature
echo "Verifying GPG signature..."
if gpg --verify checksums.txt.sig; then
  echo "Signature verification passed."
else
  echo "Signature verification failed! Aborting installation."
  exit 1
fi

# Verify checksum
echo "Verifying sha256 checksum..."
if grep kopia_"$VERSION"_linux_amd64.deb checksums.txt | sha256sum -c -; then
  echo "Checksum verification passed."
else
  echo "Checksum verification failed! Aborting installation."
  exit 1
fi

# Install debian package
dpkg -i kopia_"$VERSION"_linux_amd64.deb || {
  echo "Failed to install Duplicati. Aborting."
  exit 1
}

# Verify installation
echo "Verifying installation..."
if command -v kopia >/dev/null; then
  echo "Kopia $VERSION has been installed successfully!"
else
  echo "Kopia installation failed or kopia is not in PATH."
  exit 1
fi
