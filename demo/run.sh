#!/bin/bash

MY_PATH=$(dirname "$0")
cd "$MY_PATH" || return
cd ..
python3 -m demo
