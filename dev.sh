#!/bin/bash
# A small shell script to bootstrap a development environment

# Function to check whether command exists or not
exists()
{
  if command -v $1 &>/dev/null
  then
    return 0
  else
    return 1
  fi
}

if exists poetry
  then echo "poetry found"
  else echo "poetry not found, exiting"
  exit
fi

INITIAL_SETUP=false
for arg in "$@"
do
  if [ "$arg" == "-s" ]
  then
      INITIAL_SETUP=true
  fi
done

if $INITIAL_SETUP ; then
  echo "Running Initial Setup"
  echo "Gen environment file"
  cp .env.dist .env
  poetry install --dev
fi
poetry run python application.py
