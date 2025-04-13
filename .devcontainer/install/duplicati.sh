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
VERSION="2.1.0.5_stable_2025-03-04"
GPG_FINGERPRINT="C20E90473DAC703D"

# Install Restic from GitHub releases
wget -q https://github.com/duplicati/duplicati/releases/download/v"$VERSION"/duplicati-$VERSION-linux-x64-cli.deb
wget -q https://github.com/duplicati/duplicati/releases/download/v"$VERSION"/duplicati-$VERSION.signatures.zip

# Unzip the signatures
unzip -q duplicati-$VERSION.signatures.zip || {
  echo "Failed to unzip signatures. Aborting."
  exit 1
}

# Import the GPG key
echo "Importing GPG key..."
gpg --recv-key "$GPG_FINGERPRINT" || {
  echo "Failed to download GPG key. Aborting."
  exit 1
}

# Verify GPG signature
echo "Verifying GPG signature..."
if gpg --verify duplicati-$VERSION-linux-x64-cli.deb.sig; then
  echo "Signature verification passed."
else
  echo "Signature verification failed! Aborting installation."
  exit 1
fi

# Install debian package
dpkg -i duplicati-$VERSION-linux-x64-cli.deb || {
  echo "Failed to install Duplicati. Aborting."
  exit 1
}

# Verify installation
echo "Verifying installation..."
if command -v duplicati-cli >/dev/null; then
  echo "Duplicati $VERSION has been installed successfully!"
else
  echo "Duplicati installation failed or duplicati-cli is not in PATH."
  exit 1
fi
