#!/bin/bash -
# https://fedoraproject.org/wiki/Packaging:SourceURL?rd=Packaging/SourceURL#When_Upstream_uses_Prohibited_Code
# https://bugzilla.redhat.com/show_bug.cgi?id=1191184

version=$1
if [ -z "$version" ]; then
    echo "usage: $0 version"
    exit 1
fi

set -e

wget --quiet "http://lcamtuf.coredump.cx/afl/releases/afl-$version.tgz" -O "afl-$version.tgz"
rm -rf "afl-$version" "afl-$version-no-trademarks.tgz"
tar zxf "afl-$version.tgz"
find "afl-$version" -name 'hello_kitty*' -delete
tar zcf "afl-$version-no-trademarks.tgz" "afl-$version"
rm -r "afl-$version"

echo "Created: afl-$version-no-trademarks.tgz"
