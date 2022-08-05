#!/bin/sh
# Author: Andriy Babak
# email: ababak@gmail.com

if [ -z "$1" ]; then
    echo "Please specify the tag to update:"
    git tag --list --sort=-v:refname
    exit 1
fi
TAGS=$(git tag --list "$1" | wc -l);
if [[ $TAGS != 1 ]]; then
    echo "Found ${TAGS} tags matching your request"
    exit 1
fi
git push origin :refs/tags/$1
git tag -fa -m "Updating $1 tag" $1
git push origin master --tags
echo "Tag $1 updated successfully"
