class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {
            'bools': {},
            'strings': {}
        }

    def visit_Dependency(self, node):
        print(f'Requiring dependency: {node.name}')

    def visit_BoolAssignment(self, node):
        value = node.value == 'true'
        self.GLOBAL_SCOPE['bools'][node.var_name] = value

    def visit_StringAssignment(self, node):
        self.GLOBAL_SCOPE['strings'][node.var_name] = node.value

    def visit_Condition(self, node):
        return self.GLOBAL_SCOPE['bools'].get(node.var_name, False) == node.expected_value

    def visit_StringModification(self, node):
        self.GLOBAL_SCOPE['strings'][node.var_name] = node.new_value

    def visit_IfStatement(self, node):
        if self.visit(node.condition):
            self.visit(node.then_branch)
        else:
            self.visit(node.else_branch)

    def interpret(self):
        tree = self.parser.parse()
        for node in tree:
            self.visit(node)
        return self.GLOBAL_SCOPE
