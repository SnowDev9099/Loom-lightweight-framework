class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class TokenType:
    FUNCTION = "FUNCTION"
    VARIABLE = "VARIABLE"
    LOOP = "LOOP"
    PLACEHOLDER = "PLACEHOLDER"
    REQUIRE_DEPENDENCY = "REQUIRE_DEPENDENCY"
    SYSTEM_LOG = "SYSTEM_LOG"
