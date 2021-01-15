#!/bin/zsh
source ~/.zshrc
~/.virtualenvs/golfpools/bin/python ~/projects/python/golfpools/src/main.py
#if ! pgrep -lf python | grep -q main.py; then
#    ~/.virtualenvs/golfpools/bin/python ~/projects/python/golfpools/src/main.py
#fi
