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
VERSION="0.18.0"

# Install Restic from GitHub releases
wget -q https://github.com/restic/restic/releases/download/v"$VERSION"/restic_"$VERSION"_linux_amd64.bz2
wget -q https://github.com/restic/restic/releases/download/v"$VERSION"/SHA256SUMS
wget -q https://github.com/restic/restic/releases/download/v"$VERSION"/SHA256SUMS.asc

# Import the GPG key
echo "Importing GPG key..."
curl -s https://restic.net/gpg-key-alex.asc | gpg --import - || {
  echo "Failed to download GPG key. Aborting."
  exit 1
}

# Verify GPG signature
echo "Verifying GPG signature..."
if gpg --verify SHA256SUMS.asc; then
  echo "Signature verification passed."
else
  echo "Signature verification failed! Aborting installation."
  exit 1
fi

# Verify downloaded file checksum
echo "Verifying sha256 checksum..."
if grep restic_"$VERSION"_linux_amd64.bz2 SHA256SUMS | sha256sum -c -; then
  echo "Checksum verification passed."
else
  echo "Checksum verification failed! Aborting installation."
  exit 1
fi

# Extract binary
echo "Extracting restic binary..."
bunzip2 -k restic_"$VERSION"_linux_amd64.bz2 || {
  echo "Failed to extract binary. Aborting."
  exit 1
}

# Make binary executable
chmod +x restic_"$VERSION"_linux_amd64

# Move binary to /bin
echo "Installing restic binary to /bin..."
mv restic_"$VERSION"_linux_amd64 /bin/restic

# Verify installation
echo "Verifying installation..."
if command -v restic >/dev/null; then
  echo "Restic $VERSION has been installed successfully!"
else
  echo "Restic installation failed or restic is not in PATH."
  exit 1
fi
