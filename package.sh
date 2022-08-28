#!/usr/bin/env sh

# make sure 'fpm' is installed
# and 'dist/splasher' is generated

# Create folders.
[ -e package ] && rm -r package
mkdir -p package/opt
mkdir -p package/usr/share/applications

# Copy files (change icon names, add lines for non-scaled icons)
cp -r dist/splasher package/opt/splasher
cp splasher.desktop package/usr/share/applications

# Change permissions
find package/opt/splasher -type f -exec chmod 644 -- {} +
find package/opt/splasher -type d -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +
chmod +x package/opt/splasher/splasher
