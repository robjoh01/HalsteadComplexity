<div align="center">

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/robjoh01/HalsteadComplexity/blob/HEAD/LICENSE.txt)
![Build Status](https://github.com/robjoh01/HalsteadComplexity/actions/workflows/build-and-release.yml/badge.svg)
![Testing Status](https://github.com/robjoh01/HalsteadComplexity/actions/workflows/testing.yml/badge.svg)

_A Python program that analyzes code complexity using Halstead metrics and presents the results._

</div>

#

A Python program that analyzes code complexity using Halstead metrics and presents the results in a clear and structured format. It evaluates key metrics such as operator and operand counts, program vocabulary, difficulty, and effort, providing insights into the maintainability of the code. The analysis results can be displayed in the terminal with rich formatting or saved to a file for further review.

## ⚙️ Requirements

- **Python 3.x**: Required to build and run the project.

## 🛠️ Dependencies

- [inquirer](https://pypi.org/project/inquirer/): Used for interactive prompts.
- [rich console](https://rich.readthedocs.io/en/latest/console.html): Used for enhanced console output.
- [PyInstaller](https://pyinstaller.org/en/stable/): Used to package the Python script as a standalone `.exe` file.
- [Commitizen](https://github.com/commitizen/cz-cli): Automates version bumping and changelog updates based on conventional commit messages.

## 🚀 Installation

You can install using one of the following methods:

- **Release**: Download the pre-built `.exe` file from the [Releases](https://github.com/robjoh01/HalsteadComplexity/releases) section.
- **Manual Installation**: Follow the instructions in the [Manual Installation](#manual-installation) section.

> [!TIP]
> You can add the `HalsteadComplexity.exe` file to your `PATH` variable to make it accessible from any directory.

### Manual Installation

### 1. Clone the repository:

First, clone the repository to your local machine:

```bash
git clone git@github.com:robjoh01/halstead_complexity.git
cd halstead_complexity
```

### 2. Install dependencies:

To install the dependencies, run this script:

```powershell
.\scripts\install.ps1
```

```bash
./scripts/install.sh
```

### 3. Test the project

When you are working with the project, remember to run the tests:

```powershell
.\scripts\test.ps1
```

```bash
./scripts/test.sh
```

### 3. Run the project:

```powershell
.\scripts\run.ps1
```

```bash
./scripts/run.sh
```

### 4. Building the Executable:

> [!NOTE]
> Building the `.exe`, only works on Windows machines!

You can run the build script to build the `.exe` file from the source code:

```powershell
.\scripts\build.ps1
```

This script will create a virtual environment, install the required dependencies, and build the `.exe` file.

The `.exe` file will be generated in the `dist` folder.

## 🔥 Usage

### Prerequisites

Before running the program, you have to ensure that you have the correct operators for the language you are testing. You can do so in `src/halstead.py`. The default operators are set to Python. JavaScript is also included.

#### Note

- Braces are counted separately.
- Function definitions and calls are both counted as operands.
- Template literals are combined with the string, counting as a single operand (f"{n} is odd.").

### Single mode

```powershell
./scripts/run.ps1 -i "examples/cpp/input/player_bad.txt" -o "examples/cpp/output/player_bad.txt"
./scripts/run.ps1 -i "examples/cpp/input/player_bad.txt" -o "examples/cpp/output/player_bad.csv"
```

### Batch mode

Multiple files:

```powershell
./scripts/run.ps1 -b -il "examples/cpp/inputs.txt" -ol "examples/cpp/outputs.txt"
```

Combined CSV file:

```powershell
./scripts/run.ps1 -b -il "examples/cpp/inputs.txt" -o "examples/cpp/output/combined.csv"
```

Add `-s` to silent the console output.

## 🆘 Support

If you have any questions or issue, just write to my BTH student mail: [roje22](mailto:roje22@student.bth.se)
