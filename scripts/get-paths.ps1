$base = "C:\Users\user\Documents\Github\halstead-complexity"
$targets = @(
    "plotly/python/plotly.py-2.0.0",
    "plotly/python/plotly.py-3.0.0",
    "plotly/python/plotly.py-4.0.0",
    "plotly/python/plotly.py-5.0.0",
    "plotly/python/plotly.py-6.0.0"
)
$output = "plotly/python/inputs.txt"

# Define directories to exclude - just use the directory name without the path
$excludeDirs = @("dist", "specs", "test", "tests", "doc", "validators", "codegen")

# Initialize empty array for all lines
$lines = @()

# Process each target path
foreach ($target in $targets) {
    $files = Get-ChildItem -Recurse -Path $target -File | Where-Object {
        $filePath = $_
        $_.Extension -eq ".py" -and
        # Check if none of the directory components in the path match any excluded directory
        -not ($excludeDirs | Where-Object {
            # Split path into components and check if any component exactly matches the excluded dir
            $pathComponents = $filePath.DirectoryName -split '\\'
            $pathComponents -contains $_
        })
    }

    # Add each file path to the lines array
    foreach ($file in $files) {
        $relativePath = $file.FullName.Replace($base + "\", "")
        $lines += $relativePath
    }

    # Add an empty line after processing this target
    $lines += ""
}

# Write all lines to the output file
$lines | Set-Content $output