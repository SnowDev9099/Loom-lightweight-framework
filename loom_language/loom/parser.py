from lexer import Lexer

class AST:
    pass

class Dependency(AST):
    def __init__(self, name):
        self.name = name

class BoolAssignment(AST):
    def __init__(self, value, var_name):
        self.value = value
        self.var_name = var_name

class StringAssignment(AST):
    def __init__(self, value, var_name):
        self.value = value
        self.var_name = var_name

class IfStatement(AST):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class Condition(AST):
    def __init__(self, var_name, expected_value):
        self.var_name = var_name
        self.expected_value = expected_value

class StringModification(AST):
    def __init__(self, var_name, new_value):
        self.var_name = var_name
        self.new_value = new_value

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def parse_dependency(self):
        self.eat('IDENTIFIER')  # Require
        self.eat('DOT')         # .
        self.eat('IDENTIFIER')  # Dependency
        self.eat('LPAREN')      # (
        name = self.current_token.value
        self.eat('STRING')      # "name"
        self.eat('RPAREN')      # )
        self.eat('EQUALS')      # =
        self.eat('LPAREN')      # (
        self.eat('IDENTIFIER')  # name
        self.eat('RPAREN')      # )
        return Dependency(name)

    def parse_bool_assignment(self):
        self.eat('IDENTIFIER')  # bool
        self.eat('EQUALS')      # =
        self.eat('IDENTIFIER')  # newbool
        self.eat('LPAREN')      # (
        self.eat('RPAREN')      # )
        self.eat('DOT')         # .
        self.eat('IDENTIFIER')  # value
        self.eat('EQUALS')      # =
        self.eat('LPAREN')      # (
        value = self.current_token.value
        self.eat('STRING')      # "value"
        self.eat('RPAREN')      # )
        self.eat('DOT')         # .
        self.eat('IDENTIFIER')  # varsetname
        self.eat('EQUALS')      # =
        self.eat('LPAREN')      # (
        var_name = self.current_token.value
        self.eat('STRING')      # "name"
        self.eat('RPAREN')      # )
        return BoolAssignment(value, var_name)

    def parse_string_assignment(self):
        self.eat('IDENTIFIER')  # string
        self.eat('EQUALS')      # =
        self.eat('IDENTIFIER')  # newstring
        self.eat('LPAREN')      # (
        self.eat('RPAREN')      # )
        self.eat('DOT')         # .
        self.eat('IDENTIFIER')  # value
        self.eat('EQUALS')      # =
        self.eat('LPAREN')      # (
        value = self.current_token.value
        self.eat('STRING')      # "value"
        self.eat('RPAREN')      # )
        self.eat('DOT')         # .
        self.eat('IDENTIFIER')  # varsetname
        self.eat('EQUALS')      # =
        self.eat('LPAREN')      # (
        var_name = self.current_token.value
        self.eat('STRING')      # "name"
        self.eat('RPAREN')      # )
        return StringAssignment(value, var_name)

    def parse_condition(self):
        self.eat('IDENTIFIER')  # get
        self.eat('LPAREN')      # (
        self.eat('IDENTIFIER')  # var
        self.eat('DOT')         # .
        self.eat('IDENTIFIER')  # bool
        self.eat('EQUALS')      # =
        var_name = self.current_token.value
        self.eat('STRING')      # "bools name"
        self.eat('RPAREN')      # )
        self.eat('EQUALS')      # =
        self.eat('IDENTIFIER')  # true
        return Condition(var_name, True)

    def parse_string_modification(self):
        self.eat('IDENTIFIER')  # get
        self.eat('LPAREN')      # (
        self.eat('IDENTIFIER')  # var
        self.eat('DOT')         # .
        var_name = self.current_token.value
        self.eat('STRING')      # "strings name"
        self.eat('RPAREN')      # )
        self.eat('DOT')         # .
        self.eat('IDENTIFIER')  # set
        self.eat('LPAREN')      # (
        self.eat('IDENTIFIER')  # var
        self.eat('DOT')         # .
        self.eat('IDENTIFIER')  # changevalue
        self.eat('DOT')         # .
        self.eat('IDENTIFIER')  # string
        self.eat('RPAREN')      # )
        self.eat('EQUALS')      # =
        self.eat('LPAREN')      # (
        new_value = self.current_token.value
        self.eat('STRING')      # "new value"
        self.eat('RPAREN')      # )
        return StringModification(var_name, new_value)

    def parse_if_statement(self):
        self.eat('IDENTIFIER')  # if
        condition = self.parse_condition()
        self.eat('IDENTIFIER')  # then
        then_branch = self.parse_string_modification()
        self.eat('IDENTIFIER')  # else()
        else_branch = self.parse_string_modification()
        return IfStatement(condition, then_branch, else_branch)

    def parse(self):
        nodes = []
        while self.current_token.type != 'EOF':
            if self.current_token.type == 'IDENTIFIER':
                if self.current_token.value == 'Require':
                    nodes.append(self.parse_dependency())
                elif self.current_token.value == 'bool':
                    nodes.append(self.parse_bool_assignment())
                elif self.current_token.value == 'string':
                    nodes.append(self.parse_string_assignment())
                elif self.current_token.value == 'if':
                    nodes.append(self.parse_if_statement())
                else:
                    self.error()
        return nodes
