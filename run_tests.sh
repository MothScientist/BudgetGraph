#!/bin/bash

cd tests

python build_test_infrastructure.py

cd ..

pytest
