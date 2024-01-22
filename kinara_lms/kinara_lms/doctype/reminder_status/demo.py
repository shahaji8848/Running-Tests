import ast
from collections import Counter

def count_function_occurrences(tree):
    function_occurrences = Counter()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_occurrences[node.name] += 1

    return function_occurrences

def break_functions(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    tree = ast.parse(code)
    function_occurrences = count_function_occurrences(tree)

    new_lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if function_occurrences[node.name] > 3:
                # Break the function after every 10 lines
                for i in range(0, len(node.body), 10):
                    new_lines.extend(node.body[i:i + 10])
                    new_lines.append('')  # Add an empty line after every 10 lines
            else:
                new_lines.append(ast.unparse(node))
        else:
            new_lines.append(ast.unparse(node))

    new_code = '\n'.join(new_lines)

    with open(file_path, 'w') as file:
        file.write(new_code)

    print(f"Functions appearing more than 3 times in {file_path} have been broken after every 10 lines.")

if __name__ == "__main__":
    # Specify the path to your Python file
    python_file_path = "path/to/your/file.py"
    break_functions(python_file_path)
