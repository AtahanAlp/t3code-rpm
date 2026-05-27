#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "usage: $0 <version-without-leading-v>" >&2
  exit 2
fi

version="${1#v}"
metadata_url="https://github.com/pingdotgg/t3code/releases/download/v${version}/latest-linux.yml"
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

curl -L --fail --silent --show-error --output "$tmp" "$metadata_url"

asset="$(awk '/^path:/ { print $2; exit }' "$tmp")"
sha512_b64="$(awk '/^sha512:/ { print $2; exit }' "$tmp")"
expected_asset="T3-Code-${version}-x86_64.AppImage"

if [ "$asset" != "$expected_asset" ]; then
  echo "unexpected linux asset: $asset (expected $expected_asset)" >&2
  exit 1
fi

sha512_hex="$(printf '%s' "$sha512_b64" | base64 -d | od -An -tx1 -v | tr -d ' \n')"

sed -i "s/^Version:.*/Version:        ${version}/" t3code.spec
rm -f sources/T3-Code-*-x86_64.AppImage.sha512
printf '%s  %s\n' "$sha512_hex" "$asset" > "sources/${asset}.sha512"

echo "Updated t3code.spec and sources/${asset}.sha512"
