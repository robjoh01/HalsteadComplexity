$base = $PSScriptRoot
$targets = @(
	"plotly/js/plotly.js-1.0.0",
	"plotly/js/plotly.js-2.0.0",
	"plotly/js/plotly.js-3.0.0"
)
$output = "plotly/js/inputs.txt"

# Directories to exclude
$excludeDirs = @("build", "devtools", "dist", "lib", "tasks", "test", "tests", "doc", "validators", "codegen", "stackgl_modules")

# Initialize empty array for all lines
$lines = @()

# Process each target path
foreach ($target in $targets) {
	$files = Get-ChildItem -Recurse -Path $target -File | Where-Object {
		$filePath = $_
		$_.Extension -eq ".js" -and
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