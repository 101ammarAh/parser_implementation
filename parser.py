from enum import Enum
from scanner import call_scanner

class TokenType(Enum):
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

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        return self.program()

    def match(self, expected_type):
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index].token_type == expected_type:
            self.current_token_index += 1
        else:
            raise SyntaxError(f"Expected {expected_type}, found {self.tokens[self.current_token_index].token_type}")

    def program(self):
        return self.statement_list()

    def statement_list(self):
        statements = []
        while self.tokens[self.current_token_index].token_type != TokenType.EOL:
            # Check for comments
            if self.tokens[self.current_token_index].token_type == TokenType.COMMENT:
                self.current_token_index += 1  # Skip the comment token
                # Move to the next token (EOL) after the comment
                while self.tokens[self.current_token_index].token_type != TokenType.EOL:
                    self.current_token_index += 1
                self.current_token_index += 1  # Move past the EOL token
                continue  # Continue to the next iteration of the loop
            
            # Parse statements as usual
            statement = self.statement()
            statements.append(statement)
        return statements


    def statement(self):
        if self.tokens[self.current_token_index].token_type == TokenType.KEYWORD and self.tokens[self.current_token_index].lexeme == 'if':
            return self.if_else_statement()
        elif self.tokens[self.current_token_index].token_type == TokenType.KEYWORD and self.tokens[self.current_token_index].lexeme == 'print':
            return self.print_statement()
        else:
            return self.assignment_statement()

    def assignment_statement(self):
        identifier = self.tokens[self.current_token_index].lexeme
        self.match(TokenType.IDENTIFIER)
        self.match(TokenType.OPERATOR)  # =
        expression = self.expression()
        self.match(TokenType.EOL)
        return f"Assign {identifier} = {expression}"

    def if_else_statement(self):
        self.match(TokenType.KEYWORD)  # if
        self.match(TokenType.LEFT_PAREN)
        expression = self.expression()
        self.match(TokenType.RIGHT_PAREN)
        self.match(TokenType.LEFT_BRACE)
        if_statements = self.statement_list()
        self.match(TokenType.RIGHT_BRACE)
        self.match(TokenType.KEYWORD)  # else
        self.match(TokenType.LEFT_BRACE)
        else_statements = self.statement_list()
        self.match(TokenType.RIGHT_BRACE)
        return f"If {expression}: {if_statements} Else: {else_statements}"

    def print_statement(self):
        self.match(TokenType.KEYWORD)  # print
        self.match(TokenType.LEFT_PAREN)
        expression = self.expression()
        self.match(TokenType.RIGHT_PAREN)
        self.match(TokenType.EOL)
        return f"Print {expression}"

    def expression(self):
        term = self.term()
        while self.tokens[self.current_token_index].token_type == TokenType.OPERATOR and \
              self.tokens[self.current_token_index].lexeme in ('+', '-'):
            operator = self.tokens[self.current_token_index].lexeme
            self.match(TokenType.OPERATOR)
            term = f"{term} {operator} {self.term()}"
        return term

    def term(self):
        factor = self.factor()
        while self.tokens[self.current_token_index].token_type == TokenType.OPERATOR and \
              self.tokens[self.current_token_index].lexeme in ('*', '/'):
            operator = self.tokens[self.current_token_index].lexeme
            self.match(TokenType.OPERATOR)
            factor = f"{factor} {operator} {self.factor()}"
        return factor

    def factor(self):
        if self.tokens[self.current_token_index].token_type == TokenType.IDENTIFIER or \
           self.tokens[self.current_token_index].token_type == TokenType.INTEGER or \
           self.tokens[self.current_token_index].token_type == TokenType.BOOLEAN:
            factor = self.tokens[self.current_token_index].lexeme
            self.match(self.tokens[self.current_token_index].token_type)
            return factor
        elif self.tokens[self.current_token_index].token_type == TokenType.LEFT_PAREN:
            self.match(TokenType.LEFT_PAREN)
            expression = self.expression()
            self.match(TokenType.RIGHT_PAREN)
            return expression
        else:
            raise SyntaxError("Invalid expression")

def main():
    # Output from scanner
    token_types = call_scanner("input.txt")
    
    # Convert token types to TokenType enum values
    tokens = [Token(TokenType(token_type), lexeme) for token_type, lexeme in zip(token_types[::2], token_types[1::2])]

    # tokens = [Token(TokenType(int(token_type)), lexeme) for token_type, lexeme in zip(token_types[::2], token_types[1::2])]

    parser = Parser(tokens)
    result = parser.parse()
    print(result)

if __name__ == "__main__":
    main()
