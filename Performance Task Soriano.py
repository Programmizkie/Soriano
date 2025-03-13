# Token types 
# 
# EOF (end-of-file) token is used to indicate that 
# there is no more input left for lexical analysis
INTEGER, MUL, DIV, EOF = 'INTEGER', 'MUL', 'DIV', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,'+', or None
        self.value = value


    def __str__(self):
        """String representation of the class instance.

        Examples:

        Token(INTEGER, 3)
        Token(MUL, '*')
        """

        return 'Token({type}, {value})'.format(
            type = self.type,
            value = repr(self.value)
        )


    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]


    def error(self):
        raise Exception('Invalid character')


    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]


    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()


    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)


    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()


    def error(self):
        raise Exception('Invalid Syntax')
   
    
    def eat(self, token_type):
        # compare the current token type with the passed token 
        # type and if they match then "eat" the current token,
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else: 
            self.error()


    def factor(self):
        """Return an INTEGER token value.
        
        factor : INTEGER 
        """
        token = self.current_token
        self.eat(INTEGER)
        return token.value


    def expr(self):
        """Arithmetic expression parser / interpreter.

        expr   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        result = self.factor()   
        
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result // self.factor()    
                
        return result

    
def main():
    while True:
        try: 
            # To run under Python 3 replace 'raw_input' call
            # with 'input'
            text = input('calc>')
        except EOFError:
            break

        if not text:
            continue

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()

        print(result)

if __name__ == '__main__':
    main()

. What does the Term function do?
The term function purpose for me when analyzing the code is that it checks the syntax if the 
current token is in the multiplication or division operator. If the token is in multiplication, the 
function will multiply the result. If the token is in division, the function will divide the result.
2. What does the Factor function do, compared to the Term function?
Term function and factor function are connected to each other since the term function’s purpose 
is to analyze if the current token is in division or multiplication while for the factor function 
tokenizes the current token in order to eat the value.
3. What changes were made to the Expr function? And how does it related to the Term and Factor 
functions?
Expr function is related to term and factor function since it also checks what are the correct 
precedence or in in order its like following the MDAS rule by multiplying and dividing first 
before adding and subtracting.
4. Is operator precedence followed in the code? If no, why? If yes, how?
Yes, when you try to input a value it will first apply the term function before the expr function 
since it has a rules to follow just like MDAS rule
5. What does it mean for an operator to be left-associative?
When there are multiple operators appear it will read the operands first from left to right and 
follows the rules in which what are the operator precedence need to follow first.
