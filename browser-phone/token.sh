#!/bin/bash

Seed="+turtleville"
token="${QUERY_STRING:-$1,}"
token=$(echo -n "${token%,*}${Seed}" | md5sum)
echo -n "${token%% *}"
