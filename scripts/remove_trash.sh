#!/bin/sh

cd .. || exit 1
rm -rf ./logs
rm -rf ./.pytest_cache

cd app || exit 1
rm -rf ./logs
rm -rf ./__pycache__

cd ../tests || exit 1
rm -rf ./logs
rm -rf ./.pytest_cache
rm -rf ./__pycache__
