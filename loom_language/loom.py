from token import Token, TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        ast = []
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == TokenType.FUNCTION:
                ast.append(self.parse_function())
            elif token.type == TokenType.VARIABLE:
                ast.append(self.parse_variable())
            elif token.type == TokenType.LOOP:
                ast.append(self.parse_loop())
            elif token.type == TokenType.PLACEHOLDER:
                ast.append(self.parse_placeholder())
            elif token.type == TokenType.REQUIRE_DEPENDENCY:
                ast.append(self.parse_require_dependency())
            elif token.type == TokenType.SYSTEM_LOG:
                ast.append(self.parse_system_log())
            self.current_token_index += 1
        return ast

    def parse_function(self):
        self.current_token_index += 1  # Skip 'function' keyword
        name = self.tokens[self.current_token_index].value
        self.current_token_index += 2  # Skip '(' and go to first parameter
        parameters = []
        while self.tokens[self.current_token_index].value != ')':
            parameters.append(self.tokens[self.current_token_index].value)
            self.current_token_index += 1
            if self.tokens[self.current_token_index].value == ',':
                self.current_token_index += 1
        self.current_token_index += 2  # Skip ')' and go to '='
        self.current_token_index += 2  # Skip '=' and go to function body
        body = self.tokens[self.current_token_index].value
        return {'type': 'function', 'name': name, 'parameters': parameters, 'body': body}

    def parse_variable(self):
        token = self.tokens[self.current_token_index]
        name = token.value
        self.current_token_index += 2  # Skip variable name and '='
        value = self.tokens[self.current_token_index].value
        return {'type': 'variable', 'name': name, 'value': value}

    def parse_loop(self):
        self.current_token_index += 1  # Skip 'loop'
        times = self.tokens[self.current_token_index].value
        self.current_token_index += 2  # Skip times and '('
        body = self.tokens[self.current_token_index + 1].value
        return {'type': 'loop', 'times': times, 'body': body}

    def parse_placeholder(self):
        token = self.tokens[self.current_token_index]
        self.current_token_index += 2  # Skip placeholder and '='
        value = self.tokens[self.current_token_index].value
        return {'type': 'placeholder', 'value': value}

    def parse_require_dependency(self):
        token = self.tokens[self.current_token_index]
        filename = token.value
        return {'type': 'require_dependency', 'filename': filename}

    def parse_system_log(self):
        token = self.tokens[self.current_token_index]
        message = token.value
        return {'type': 'system_log', 'message': message}


class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.dependencies = {}

    def load_dependency(self, filename):
        with open(filename, 'r') as file:
            code = file.read()
            tokens = self.tokenize(code)
            parser = Parser(tokens)
            ast = parser.parse()
            self.dependencies[filename] = ast

    def visit_Function(self, node):
        params = [self.visit(param) for param in node['parameters']]
        return lambda *args: eval(node['body'], dict(zip(params, args)))

    def visit_Variable(self, node):
        return node['value']

    def visit_Loop(self, node):
        for _ in range(int(node['times'])):
            self.visit(node['body'])

    def visit_Placeholder(self, node):
        return node['value']

    def visit_RequireDependency(self, node):
        filename = node['filename']
        if filename not in self.dependencies:
            self.load_dependency(filename)
        for dependency_node in self.dependencies[filename]:
            self.visit(dependency_node)

    def visit_SystemLog(self, node):
        print(node['message'])

    def interpret(self, code):
        tokens = self.tokenize(code)
        self.parser.tokens = tokens
        ast = self.parser.parse()
        for node in ast:
            self.visit(node)

    def tokenize(self, code):
        tokens = []
        for line in code.split('\n'):
            if line.startswith('function'):
                tokens.append(Token(TokenType.FUNCTION, line))
            elif '=' in line:
                tokens.append(Token(TokenType.VARIABLE, line))
            elif line.startswith('loop'):
                tokens.append(Token(TokenType.LOOP, line))
            elif 'placeholder' in line:
                tokens.append(Token(TokenType.PLACEHOLDER, line))
            elif line.startswith('require.dependency'):
                tokens.append(Token(TokenType.REQUIRE_DEPENDENCY, line))
            elif line.startswith('debug.system.log'):
                tokens.append(Token(TokenType.SYSTEM_LOG, line))
        return tokens


if __name__ == '__main__':
    code = """
    function add(a, b) = (
        return a + b
    )

    x = 10

    loop(5) (
        debug.system.log("Loop iteration")
    )
    """
    parser = Parser([])
    interpreter = Interpreter(parser)
    interpreter.interpret(code)
