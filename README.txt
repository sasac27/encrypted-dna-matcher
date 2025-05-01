# Encrypted DNA Matcher

This project demonstrates homomorphic encryption using Microsoft SEAL (via a custom PySEAL wrapper) to perform private DNA sequence matching. A pattern is searched within an encrypted DNA sequence without ever decrypting the data on the server.

## Features
- **Fully Encrypted Pattern Matching** using the CKKS scheme.
- **Batch Window Search** to improve performance.
- **Command-Line Interface** and programmatic usage.
- **Automated Test Suite** for validation and performance benchmarking.
- **Modular Project Structure** for easy maintenance and extension.

## Project Structure
```
encrypted-dna-matcher/
├── pyseal_wrapper/            # C++ bindings to Microsoft SEAL
├── src/
│   ├── encryptor.py           # Main logic (EncryptedDNAMatcher class)
│   ├── cli.py                 # CLI for interactive use
├── tests/
│   └── tester.py              # Test suite for accuracy and performance
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/encrypted-dna-matcher.git
cd encrypted-dna-matcher
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Build the PySEAL wrapper
Make sure you have CMake and a C++ compiler installed (e.g., `g++`).
```bash
cd pyseal_wrapper
mkdir -p build && cd build
cmake ..
make
```

This builds the `pyseal` module used throughout the project.

## Usage

### Run the CLI
```bash
python src/cli.py
```

### Run the Test Suite
```bash
python tests/tester.py
```

## License
MIT License

---

## requirements.txt
```
pybind11
numpy
```

Note: Microsoft SEAL and the compiled `.so` file for `pyseal` are not included in `requirements.txt` and must be built manually.

