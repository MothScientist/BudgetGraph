#!/bin/sh

rm -rf ./logs
rm -rf ./.pytest_cache

cd app
rm -rf ./logs
rm -rf ./__pycache__

cd ..
cd tests
rm -rf ./logs
rm -rf ./.pytest_cache
rm -rf ./__pycache__
