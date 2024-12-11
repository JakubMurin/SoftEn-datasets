#!/bin/bash

# Script to find all uml files in repo and produce only raw file urls
while IFS= read -r line; do

    repo=$(echo "$line" | sed 's/[[:space:]]*$//')
    # gh api search/code?q=repo:$repo+extension:uml --jq ".items[:1] | .[].html_url" | \
    gh api search/code?q=repo:$repo+extension:uml --jq ".items[].html_url" | \
    sed 's|https://github.com|https://raw.githubusercontent.com|' | \
    sed 's|/blob||' >> output.txt

done < repos.txt

# Script to get second line of files (identify xmi type)
# while IFS= read -r line; do

#     url=$(echo "$line" | sed 's/[[:space:]]*$//')
#     curl -s $url | sed -n '2p' >> uml_types.txt
# done < output.txt
