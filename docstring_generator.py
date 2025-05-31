import ast
import re
from openai import OpenAI
import gradio as gr

# Setup Ollama client
MODEL = "llama3.2"
openai = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def extract_functions_and_classes(code):
    """Extract function and class definitions from Python code."""
    try:
        tree = ast.parse(code)
        elements = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                # Check if it already has a docstring
                has_docstring = False
                if node.body and isinstance(node.body[0], ast.Expr):
                    if isinstance(node.body[0].value, ast.Constant):
                        if isinstance(node.body[0].value.value, str):
                            has_docstring = True
                
                element_type = "function" if isinstance(node, ast.FunctionDef) else "class"
                elements.append({
                    'name': node.name,
                    'type': element_type,
                    'line': node.lineno,
                    'has_docstring': has_docstring
                })
        
        return elements
    except:
        return []

def generate_docstring(code, element_name, element_type):
    """Generate docstring using Ollama."""
    prompt = f"""
Generate a high-quality docstring for this Python {element_type}. 
Follow Google style format and be concise but informative.

Code:
```python
{code}
```

Write ONLY the docstring content (without triple quotes).
Include:
- Brief description
- Parameters with types (if any)
- Return value (if applicable)
- Keep it professional and clear

Docstring:"""
    
    try:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert Python developer who writes clear, concise docstrings."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        docstring = response.choices[0].message.content.strip()
        # Clean up any quotes that might be included
        docstring = docstring.replace('"""', '').replace("'''", '')
        return docstring
    except Exception as e:
        return f"Error generating docstring: {str(e)}"

def add_docstring_to_code(original_code, element_name, docstring):
    """Add docstring to the code."""
    lines = original_code.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Look for function/class definition
        if f"def {element_name}" in line or f"class {element_name}" in line:
            if line.strip().endswith(':'):
                # Get indentation of next line or default to 4 spaces
                indent = "    "
                if i + 1 < len(lines) and lines[i + 1].strip():
                    next_line = lines[i + 1]
                    indent = next_line[:len(next_line) - len(next_line.lstrip())]
                    if not indent:
                        indent = "    "
                
                # Add docstring
                docstring_lines = docstring.split('\n')
                new_lines.append(f'{indent}"""')
                for doc_line in docstring_lines:
                    if doc_line.strip():
                        new_lines.append(f'{indent}{doc_line}')
                    else:
                        new_lines.append('')
                new_lines.append(f'{indent}"""')
    
    return '\n'.join(new_lines)

def process_code(code_input):
    """Main function to process code and generate docstrings."""
    if not code_input.strip():
        return "Please enter some Python code!", ""
    
    # Extract functions and classes
    elements = extract_functions_and_classes(code_input)
    
    if not elements:
        return "No functions or classes found in the code!", ""
    
    # Show what we found
    found_items = []
    for elem in elements:
        status = "✅ Has docstring" if elem['has_docstring'] else "❌ Missing docstring"
        found_items.append(f"Line {elem['line']}: {elem['type']} '{elem['name']}' - {status}")
    
    analysis = "Found:\n" + "\n".join(found_items)
    
    # Generate docstring for the first element without docstring
    for elem in elements:
        if not elem['has_docstring']:
            print(f"Generating docstring for {elem['name']}...")
            docstring = generate_docstring(code_input, elem['name'], elem['type'])
            
            # Add docstring to code
            updated_code = add_docstring_to_code(code_input, elem['name'], docstring)
            
            result = f"""
🎯 Generated docstring for: {elem['type']} '{elem['name']}'

📝 Generated Docstring:
\"\"\"
{docstring}
\"\"\"

📋 Analysis:
{analysis}
"""
            return result, updated_code
    
    return f"All functions/classes already have docstrings!\n\n{analysis}", code_input

# Sample code for testing
SAMPLE_CODE = '''def calculate_distance(x1, y1, x2, y2):
    import math
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class DataProcessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
    
    def load_data(self):
        with open(self.data_path, 'r') as f:
            self.data = f.read()
        return self.data
'''

# Create Gradio interface
with gr.Blocks(title="Code Agent: Docstring Generator") as demo:
    gr.Markdown("# 🤖 Code Agent: Docstring Generator")
    gr.Markdown("🔗 **OpenPilot Repository**: [https://github.com/commaai/openpilot](https://github.com/commaai/openpilot)")
    gr.Markdown("Paste your Python code below and generate professional docstrings")
    
    with gr.Row():
        with gr.Column():
            code_input = gr.Textbox(
                label="📝 Input Python Code",
                lines=15,
                placeholder="Paste your Python functions or classes here...",
                value=SAMPLE_CODE
            )
            generate_btn = gr.Button("🚀 Generate Docstrings", variant="primary")
        
        with gr.Column():
            result_output = gr.Textbox(
                label="📊 Analysis & Generated Docstring",
                lines=10,
                interactive=False
            )
            code_output = gr.Code(
                label="✨ Updated Code with Docstring",
                language="python"
            )

    
    generate_btn.click(
        fn=process_code,
        inputs=[code_input],
        outputs=[result_output, code_output]
    )

if __name__ == "__main__":
    print("🚀 Starting Code Agent Docstring Generator...")
    demo.launch(share=True,inbrowser=True)