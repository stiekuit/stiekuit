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

//q: How do I create a folder in a specific path using a bash script?
//a: https://stackoverflow.com/questions/793858/how-do-i-create-a-folder-in-a-specific-path-using-a-bash-script
//a: https://stackoverflow.com/questions/793858/how-do-i-create-a-folder-in-a-specific-path-using-a-bash-script/793858#793858
//Can you give me the code to create a folder in a specific path using a bash script?
//mkdir -p /path/to/folder
//mkdir -p /path/to/folder1 /path/to/folder2
//mkdir -p /path/to/folder1 /path/to/folder2 /path/to/folder3
//mkdir -p /path/to/folder1 /path/to/folder2 /path/to/folder3 /path/to/folder4

