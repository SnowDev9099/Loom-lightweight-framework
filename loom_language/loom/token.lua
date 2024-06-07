-- loom/token.lua

-- Token definitions for the Loom language

-- Token types
TOKEN_TYPES = {
    KEYWORD = 'KEYWORD',
    IDENTIFIER = 'IDENTIFIER',
    OPERATOR = 'OPERATOR',
    SEPARATOR = 'SEPARATOR',
    LITERAL = 'LITERAL',
    COMMENT = 'COMMENT',
}

-- Keywords
KEYWORDS = {
    ['function'] = 'FUNCTION',
    ['loop'] = 'LOOP',
    ['require.dependency'] = 'REQUIRE_DEPENDENCY',
    ['debug.system.log'] = 'DEBUG_LOG',
}

-- Operators
OPERATORS = {
    ['+'] = 'ADD',
    ['-'] = 'SUBTRACT',
    ['*'] = 'MULTIPLY',
    ['/'] = 'DIVIDE',
    ['='] = 'ASSIGN',
}

-- Separators
SEPARATORS = {
    ['('] = 'LEFT_PAREN',
    [')'] = 'RIGHT_PAREN',
    [','] = 'COMMA',
}

-- Literal types
LITERAL_TYPES = {
    STRING = 'STRING_LITERAL',
    NUMBER = 'NUMBER_LITERAL',
    BOOLEAN = 'BOOLEAN_LITERAL',
}
