#!/bin/bash

cd tests/src

python build_test_infrastructure.py

cd ..

python test_database_queries.py
python test_sources.py
python test_validators.py
