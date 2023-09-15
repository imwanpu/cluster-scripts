#!/bin/bash

set -e

cd "$(dirname "${BASH_SOURCE[0]}")" ||exit 1

source ./up2baseline.sh

echo_red "test echo_red." "this is the second argument"

echo_log "test echo_log." "this is the second argument"

yum_install tldr gcc-c++
