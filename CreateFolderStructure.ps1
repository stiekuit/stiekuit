$baseDir = "C:\Repo\"

# Create Solution Structure
$directories = @(
    "src\MyApp.Application",
    "src\MyApp.Domain",
    "src\MyApp.Infrastructure",
    "src\MyApp.WebApi",
    "tests\MyApp.Application.Tests",
    "tests\MyApp.WebApi.Tests"
)

foreach ($directory in $directories) {
    $fullPath = Join-Path -Path $baseDir -ChildPath $directory
    New-Item -Path $fullPath -ItemType Directory -Force
}

# Create Solution File (optional)
$projectFile = Join-Path -Path $baseDir -ChildPath "MyApp.sln"
New-Item -Path $projectFile -ItemType File -Force
