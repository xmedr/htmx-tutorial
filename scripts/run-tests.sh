#!/bin/bash
result=0
trap 'result=1' ERR

flake8 htmx_tut tests
npx eslint htmx_tut/static/js/*.js
pytest -sxv

exit "$result"
