#!/bin/bash

# Script to find all uml files in repo and produce only raw file urls

# offset=1
# start=0
# pageSize=2500

# s=$((offset + start * pageSize))
# e=$((s + pageSize))

# page=$(sed -n "${s},${e}p" repos.txt)

# gh auth status

# while read -r line; do

#     repo=$(echo "$line" | sed 's/[[:space:]]*$//')

#     echo "$s"

#     # gh api search/code?q=participant+@startuml+extension:uml --jq ".items[:1] | .[].html_url" | \
#     # gh api search/code?q=participant+@startuml+extension:uml --jq ".items[].html_url" | \
#     # gh api search/code?q=participant+@startuml+repo:$repo+extension:uml --jq ".items[].html_url" | \
#     # gh api search/code?q=@startuml+repo:$repo+extension:uml --jq ".items[:1] | .[].html_url" | \
#     # gh api search/code?q=@startuml+repo:$repo+extension:uml --jq ".items[].html_url" | \
#     gh api search/code?q=@startuml+repo:$repo+extension:puml --jq ".items[].html_url" | \
#     sed 's|https://github.com|https://raw.githubusercontent.com|' | \
#     sed 's|/blob||' >> output_puml.txt

#     s=$((s + 1))
    
#     sleep 7s

# done <<< $page



# Script to get second line of files (identify xmi type)
# while IFS= read -r line; do

#     url=$(echo "$line" | sed 's/[[:space:]]*$//')
#     curl -s $url | sed -n '2p' >> uml_types.txt
# done < output.txt



# Script to find plantuml files

for i in {1..10}; do
    # gh api --method=GET search/code -f q="@startuml extension:uml" -f per_page=100 -f page=$i --jq ".items[].html_url"| \
    #     sed 's|https://github.com|https://raw.githubusercontent.com|' | \
    #     sed 's|/blob||' >> output_uml_all.txt

    # gh api --method=GET search/code -f q="@startuml actor extension:uml" -f per_page=100 -f page=$i --jq ".items[].html_url"| \
    #     sed 's|https://github.com|https://raw.githubusercontent.com|' | \
    #     sed 's|/blob||' >> output_uml_actor.txt

    gh api --method=GET search/code -f q="@startuml actor extension:uml" -f per_page=2 -f page=$i --jq ".items[].html_url"| \
        sed 's|https://github.com|https://raw.githubusercontent.com|' | \
        sed 's|/blob||' >> a.txt

    echo "$i"
    sleep 7s
done