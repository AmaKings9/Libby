import re


class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.tokens = []
        self.current_pos = 0
        
    def tokenize(self):
        # Expresión regular "Libby turn on TV"
        pattern = r"(?i)(levy|libby|living)\s+turn\s+on\s+tv"
        match = re.match(pattern, self.input_text)
        
        if match:
            self.tokens.append(("COMMAND", match.group(0)))
        else:
            raise ValueError("Invalid command")
            
        return self.tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        
    def parse(self):
        if self.tokens[0][0] == "COMMAND":
            return True
        else:
            return False

class Interpreter:
    def __init__(self, parser_result):
        self.parser_result = parser_result
    
    def interpret(self):
        if self.parser_result:
            print("Executing: Turn on TV")
        else:
            print("Invalid command")

def main(input_text):
    try:
        # Lexer
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        
        # Parser
        parser = Parser(tokens)
        parser_result = parser.parse()
        
        # Interpreter
        interpreter = Interpreter(parser_result)
        interpreter.interpret()
        
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main("Libby turn on TV")     
    main("Levy turn on TV")      
    main("Living turn on TV")    
    main("libby turn off TV")    


