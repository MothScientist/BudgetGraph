#!/bin/env sh

cd tests/src || exit 1

python build_test_infrastructure.py

cd ..

pytests
