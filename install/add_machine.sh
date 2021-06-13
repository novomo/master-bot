#!/bin/bash
source "$(realpath "$0" | sed 's|\(.*\)/.*|\1|')/constants.sh"

curl -g \
-X POST \
-H "Content-Type: application/json" \
-H "Authorization: API $apiKey" \
-d '{"query":"mutation($name:String!, $ip:String!){newMachine(inputMachine:{name: $name, ip:$ip})}"}, "variables" : "{\"name\" : \"$HOSTNAME\", \"ip\" : \"$HOSTNAME\"}' \
$serverAddress
