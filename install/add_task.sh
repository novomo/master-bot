#!/bin/bash
source "$(realpath "$0" | sed 's|\(.*\)/.*|\1|')/constants.sh"

dir=$(realpath "$0" | sed 's|\(.*\)/.*|\1|')
parentdir="$(dirname "$dir")"

curl -g \
-X POST \
-H "Content-Type: application/json" \
-H "Authorization: API $apiKey" \
-d '{"query":"mutation($task:String!, $ip:String!){assignTask({task: $task, ip:$ip})}"}, "variables" : "{\"name\" : \"$parentdir\", \"ip\" : \"$HOSTNAME\"}' \
$serverAddress
