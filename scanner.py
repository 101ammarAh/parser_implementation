import re

class TokenType:
    INTEGER = '1'
    BOOLEAN = '2'
    OPERATOR = '3'
    KEYWORD = '4'
    IDENTIFIER = '5'
    LITERAL = '6'
    COMMENT = '7'
    LEFT_BRACE = '8'
    RIGHT_BRACE = '9'
    LEFT_PAREN = '10'
    RIGHT_PAREN = '11'
    DATA_TYPE = "12"
    EOL = '13'  

class Token:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme

class Scanner:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []

    def scan(self):
        source_code_lines = self.source_code.split('\n')
        for line in source_code_lines:
            line = line.strip()
            if line:
                self.tokenize_line(line)
                # Add EOL token after each line
                self.tokens.append(Token(TokenType.EOL, "EOL"))
        return self.tokens

    def tokenize_line(self, line):
        # Regular expressions for token patterns
        patterns = [
            (r'\bint\b|\bbool\b', TokenType.DATA_TYPE),
            (r'\b[0-9]+\b', TokenType.INTEGER),
            (r'true|false', TokenType.BOOLEAN),
            (r'\+|\-|\*|\/|\=|\=\=|\!\=', TokenType.OPERATOR),
            (r'if|else|print', TokenType.KEYWORD),
            (r'\b[a-zA-Z][a-zA-Z0-9]*\b', TokenType.IDENTIFIER),
            (r'//.*', TokenType.COMMENT),
            (r'\{', TokenType.LEFT_BRACE),
            (r'\}', TokenType.RIGHT_BRACE),
            (r'\(', TokenType.LEFT_PAREN),
            (r'\)', TokenType.RIGHT_PAREN)
        ]
        
        # Check for comments first
        comment_match = re.match(r'//.*', line)
        if comment_match:
            self.tokens.append(Token(TokenType.COMMENT, "Comment"))
            return

        # Track if any match has occurred
        matched = False
        while line:
            for pattern, token_type in patterns:
                match = re.match(pattern, line)
                if match:
                    lexeme = match.group(0)
                    token = Token(token_type, lexeme)
                    self.tokens.append(token)
                    line = line[len(lexeme):].strip()
                    matched = True
                    break
            else:
                # If no match is found, raise an error for invalid token
                if not matched:
                    raise ValueError("Invalid token at: " + line)

def call_scanner(inputFile):
    # Read MiniLang source code from input.txt file
    with open(inputFile, "r") as file:
        source_code = file.read()
    
    # Tokenize the source code
    scanner = Scanner(source_code)
    tokens = scanner.scan()
    
    # Function to get token types
    def get_token_types(tokens):
        return [token.token_type for token in tokens]
    
    # Get token types
    token_types = get_token_types(tokens)
    return token_types

if __name__ == "__main__":
    # Read MiniLang source code from input.txt file
    with open("input.txt", "r") as file:
        source_code = file.read()

    # Tokenize the source code
    scanner = Scanner(source_code)
    tokens = scanner.scan()

    # Function to get token types
    def get_token_types(tokens):
        return [token.token_type for token in tokens]

    # Get token types
    token_types = get_token_types(tokens)
    print("Token Types:", token_types)
