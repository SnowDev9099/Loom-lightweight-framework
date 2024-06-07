import os

class LoomInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.dependencies = {}

    def interpret(self, code):
        lines = code.split('\n')
        for line in lines:
            if line.strip().startswith('function'):
                self.define_function(line)
            elif '=' in line:
                self.assign_variable(line)
            elif line.strip().startswith('loop'):
                self.execute_loop(line)
            elif 'placeholder' in line:
                self.handle_placeholder(line)
            elif line.strip().startswith('require.dependency'):
                self.load_dependency(line)
            elif line.strip().startswith('debug.system.log'):
                self.log_message(line)
            elif line.strip().startswith('#') or line.strip() == '':
                continue
            else:
                print(f"Error: Unrecognized command: {line}")

    def define_function(self, line):
        parts = line.split('(')
        func_name = parts[0].split(' ')[1].strip()
        params = parts[1].split(')')[0].split(',')

        exec(line)
        self.functions[func_name] = locals()[func_name]

    def assign_variable(self, line):
        var_name, value = line.split('=')
        var_name = var_name.strip()
        value = value.strip()
        
        self.variables[var_name] = self.evaluate_expression(value)

    def evaluate_expression(self, expr):
        if '(' in expr and ')' in expr:
            parts = expr.split('(')
            func_name = parts[0].strip()
            args = parts[1].split(')')[0].split(',')
            args = [self.variables[arg.strip()] if arg.strip() in self.variables else arg.strip() for arg in args]
            return self.functions[func_name](*args)
        elif expr.strip() in self.variables:
            return self.variables[expr.strip()]
        else:
            return expr.strip()

    def execute_loop(self, line):
        parts = line.split('(')
        times = int(parts[1].split(')')[0])
        body = parts[1].split(')')[1].strip()

        for _ in range(times):
            self.interpret(body)

    def handle_placeholder(self, line):
        var_name, value = line.split('=')
        var_name = var_name.strip()
        value = value.strip()
        
        self.variables[var_name] = self.evaluate_expression(value)

    def load_dependency(self, line):
        parts = line.split('(')
        filename = parts[1].split(')')[0].strip()

        if filename not in self.dependencies:
            with open(filename, 'r') as file:
                self.dependencies[filename] = file.read()

        self.interpret(self.dependencies[filename])

    def log_message(self, line):
        message = line.split('(')[1].split(')')[0].strip()
        print(message)

    def run_script(self, file_name):
        script_dir = os.path.join(os.path.dirname(__file__), 'Scripts')
        script_path = os.path.join(script_dir, file_name)
        
        if os.path.exists(script_path):
            with open(script_path, 'r') as file:
                script_code = file.read()
            self.interpret(script_code)
        else:
            print(f"Error: Script '{file_name}' not found.")


# Example Loom code
loom_code = """

debug.system.log("Inside factorial function")

# Your Loom code here
"""

# Create and run the interpreter
interpreter = LoomInterpreter()
interpreter.interpret(loom_code)
