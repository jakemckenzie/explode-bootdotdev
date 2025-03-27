#!/bin/bash

python3 -m src.mypackage.main

cd public && python3 -m http.server 8888