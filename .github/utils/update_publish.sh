#!/usr/bin/env bash
set -e

echo -e "\n-o- Setting commit user -o-"
git config --local user.email "${GIT_USER_EMAIL}"
git config --local user.name "${GIT_USER_NAME}"

echo -e "\n-o- Update version -o-"
invoke setver --ver="${GITHUB_REF#refs/tags/}"

echo -e "\n-o- Commit updates - Version & Changelog -o-"
git add oteapi/__init__.py
git add CHANGELOG.md
git commit -m "Release ${GITHUB_REF#refs/tags/} - Changelog"

echo -e "\n-o- Update version tag -o-"
TAG_MSG=.github/utils/release_tag_msg.txt
sed -i "s|TAG_NAME|${GITHUB_REF#refs/tags/}|" "${TAG_MSG}"
git tag -af -F "${TAG_MSG}" ${GITHUB_REF#refs/tags/}
