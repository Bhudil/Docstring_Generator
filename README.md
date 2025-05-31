# 🤖 Code Agent: Docstring Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gradio](https://img.shields.io/badge/Interface-Gradio-orange.svg)](https://gradio.app/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-green.svg)](https://ollama.ai/)

An intelligent Python tool that automatically generates professional Google-style docstrings for your functions and classes using local LLM through Ollama. Features a user-friendly web interface built with Gradio.

![Screenshot (372)](https://github.com/user-attachments/assets/8cf7d0b9-5a7d-4500-addf-77d1ccdfa205)


## 🌟 Features

- **🔍 Smart Code Analysis**: Automatically detects functions and classes in your Python code
- **📝 Professional Docstrings**: Generates Google-style docstrings with proper formatting
- **🎯 Selective Generation**: Only generates docstrings for elements that don't already have them
- **🖥️ Web Interface**: Clean, intuitive Gradio-based GUI
- **🔧 Local Processing**: Uses Ollama for privacy-focused, offline LLM processing
- **⚡ Batch Processing**: Handles multiple functions and classes in a single run
- **🎨 Proper Formatting**: Maintains code indentation and structure

## 📋 Table of Contents

- [Installation](#-installation)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## 🚀 Installation

### Prerequisites

Before installing the Code Agent, ensure you have the following installed:

1. **Python 3.8 or higher**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Ollama** (for local LLM processing)
   - Visit [Ollama.ai](https://ollama.ai/) to download and install
   - Or use the command line:
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   # Download installer from https://ollama.ai/download
   ```

3. **Pull the Llama 3.2 model**
   ```bash
   ollama pull llama3.2
   ```

### Install Dependencies

Clone the repository and install required packages:

```bash
# Clone the repository
git clone https://github.com/Bhudil/Docstring_Generator.git

# Install dependencies
pip install -r requirements.txt
```

### Requirements File

Create a `requirements.txt` file with:

```txt
openai==1.3.0
gradio==4.0.0
ast-tokenize==1.0.0
```

## ⚡ Quick Start

1. **Run the Code Agent**:
   ```bash
   python docstring_generator.py
   ```

2. **Open your browser** and navigate to the provided local URL (typically `http://127.0.0.1:7860`)

3. **Paste your Python code** into the input area and click "🚀 Generate Docstrings"

## 📖 Usage

### Web Interface

The Gradio interface provides an intuitive way to interact with the docstring generator:

1. **Input Code**: Paste your Python functions or classes in the left panel
2. **Generate**: Click the "🚀 Generate Docstrings" button
3. **Review**: Check the analysis results and generated docstrings
4. **Copy**: Use the updated code from the right panel

### Command Line Usage

You can also use the core functions programmatically:

```python
from docstring_generator import extract_functions_and_classes, generate_docstring, add_docstring_to_code

# Your Python code as a string
code = """
def calculate_area(radius):
    return 3.14159 * radius ** 2
"""

# Extract functions and classes
elements = extract_functions_and_classes(code)

# Generate docstring for the first element
if elements:
    docstring = generate_docstring(code, elements[0]['name'], elements[0]['type'])
    updated_code = add_docstring_to_code(code, elements[0]['name'], docstring)
    print(updated_code)
```

## ⚙️ Configuration

### Model Configuration

To use a different Ollama model, modify the `MODEL` variable in the script:

```python
MODEL = "llama3.2"  # Change to your preferred model
```


### API Configuration

The script uses Ollama's OpenAI-compatible API. Default configuration:

```python
openai = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
```

For remote Ollama instances, update the `base_url` accordingly.

### Docstring Style

Currently generates Google-style docstrings. To modify the style, edit the prompt in the `generate_docstring()` function:

```python
prompt = f"""
Generate a high-quality docstring for this Python {element_type}. 
Follow Google style format and be concise but informative.
# Modify this prompt for different styles (NumPy, Sphinx, etc.)
"""
```

## 📚 Examples

### Example 1: Simple Function

**Input:**
```python
def calculate_distance(x1, y1, x2, y2):
    import math
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

**Output:**
```python
def calculate_distance(x1, y1, x2, y2):
    """
    Calculate the Euclidean distance between two points in 2D space.
    
    Args:
        x1 (float): X coordinate of the first point
        y1 (float): Y coordinate of the first point
        x2 (float): X coordinate of the second point
        y2 (float): Y coordinate of the second point
    
    Returns:
        float: The Euclidean distance between the two points
    """
    import math
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

### Example 2: Class with Methods

**Input:**
```python
class DataProcessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
    
    def load_data(self):
        with open(self.data_path, 'r') as f:
            self.data = f.read()
        return self.data
```

**Output:**
```python
class DataProcessor:
    """
    A class for processing data from files.
    
    Attributes:
        data_path (str): Path to the data file
        data (str): Loaded data content
    """
    def __init__(self, data_path):
        """
        Initialize the DataProcessor with a file path.
        
        Args:
            data_path (str): Path to the data file to be processed
        """
        self.data_path = data_path
        self.data = None
    
    def load_data(self):
        """
        Load data from the specified file path.
        
        Returns:
            str: The content of the loaded data file
        """
        with open(self.data_path, 'r') as f:
            self.data = f.read()
        return self.data
```

## 🔧 API Reference

### Core Functions

#### `extract_functions_and_classes(code: str) -> List[Dict]`

Extracts function and class definitions from Python code using AST parsing.

**Parameters:**
- `code` (str): Python source code as string

**Returns:**
- List of dictionaries containing:
  - `name` (str): Function/class name
  - `type` (str): "function" or "class"
  - `line` (int): Line number in source code
  - `has_docstring` (bool): Whether element already has docstring

#### `generate_docstring(code: str, element_name: str, element_type: str) -> str`

Generates a docstring for a specific function or class using Ollama.

**Parameters:**
- `code` (str): Complete source code
- `element_name` (str): Name of function/class
- `element_type` (str): "function" or "class"

**Returns:**
- Generated docstring content (str)

#### `add_docstring_to_code(original_code: str, element_name: str, docstring: str) -> str`

Inserts a docstring into the original code with proper formatting.

**Parameters:**
- `original_code` (str): Original source code
- `element_name` (str): Name of function/class to add docstring to
- `docstring` (str): Docstring content to insert

**Returns:**
- Updated code with docstring inserted (str)

#### `process_code(code_input: str) -> Tuple[str, str]`

Main processing function that orchestrates the docstring generation workflow.

**Parameters:**
- `code_input` (str): Input Python code

**Returns:**
- Tuple containing:
  - Analysis results and generated docstring info (str)
  - Updated code with docstrings (str)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for providing local LLM infrastructure
- [Gradio](https://gradio.app/) for the excellent web interface framework
- [OpenAI](https://openai.com/) for the API compatibility standard
- The Python community for AST parsing tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/code-agent-docstring-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/code-agent-docstring-generator/discussions)
- **Email**: your.email@example.com

---

⭐ **Star this repository** if you find it useful!

Made with ❤️ by [Your Name]
