#!/usr/bin/env sh
# Make sure "pyinstaller" and "fpm" are installed first.

# Execute PyInstaller
if [ -d build/ ] || [ -d dist/ ]; then
    rm -rf build/ dist/
fi
pyinstaller splasher.spec

# Create folders.
if [ -d package/ ]; then
    rm -rf package/
fi

mkdir -p package/opt
mkdir -p package/usr/share/applications

# Copy files
cp -r dist/splasher package/opt
cp splasher.desktop package/usr/share/applications

# Change permissions
find package/opt/splasher -type f -exec chmod 644 -- {} +
find package/opt/splasher -type d -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +
chmod +x package/opt/splasher/splasher

# Generate ".fpm" and execute "fpm"
if [ -e .fpm ]; then
    rm .fpm
fi

VERSION=$(< splasher/__version__.py cut -d '"' -f 2)

{
    echo "-C package"
    echo "-s dir"
    echo "-t deb"
    echo "-n 'splasher'"
    echo "-v $VERSION"
    echo "-p splasher.deb"
} >> ".fpm"

if [ -e splasher.deb ]; then
    rm splasher.deb
fi

fpm

# Clean
rm -rf build/ dist/ package/ .fpm
