#!/bin/bash

baseDir="/root/MyApp"

# Create Solution Structure
directories=(
    "src/MyApp.Application"
    "src/MyApp.Domain"
    "src/MyApp.Infrastructure"
    "src/MyApp.WebApi"
    "tests/MyApp.Application.Tests"
    "tests/MyApp.WebApi.Tests"
)

for directory in "${directories[@]}"; do
    fullPath="$baseDir/$directory"
    mkdir -p "$fullPath"
done

# Create Solution File (optional)
projectFile="$baseDir/MyApp.sln"
touch "$projectFile"
