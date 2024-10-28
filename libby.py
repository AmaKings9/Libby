import re

#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
        self.as_string()
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        return print(result)

class PalabraIlegalError(Error):
    def __init__(self, details):
        super().__init__('Palabra Ilegal', details)

class ComandoIlegalError(Error):
    def __init__(self, details):
        super().__init__('Comando Ilegal', details)

#######################################
# TOKENS
#######################################

TT_ACTIVADOR = 'ACTIVADOR'

TT_INSTRUCCION = 'INSTRUCCION'

TT_COMPLEMENTO1 = 'COMPLEMENTO1'

TT_COMPLEMENTO2 = 'COMPLEMENTO2'

TT_OBJETO1 = 'OBJETO1'

TT_OBJETO2 = 'OBJETO2'


#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.tokens = []
        self.current_pos = 0
        self.palabras = input_text.split(" ")
        
    def tokenize(self):
        # Expresión regular "Libby turn on TV"
        for palabra in self.palabras: 
            
            er_activador = r"(L|l)evy|((L|l)(i|ea))(ving|bby)"
            er_instruccion = r"(T|t)urn"
            er_complemento1 = r"(O|o)n"
            er_complemento2 = r"(O|o)ff"
            er_objeto1 = r"(T|t)(V|v)"
            er_objeto2 = r"(F|f)an"
                        
            re.match(er_activador, palabra)
            
            if re.match(er_activador, palabra):
                self.tokens.append((TT_ACTIVADOR))
            elif re.match(er_instruccion, palabra):
                self.tokens.append((TT_INSTRUCCION))
            elif re.match(er_complemento1, palabra):
                self.tokens.append((TT_COMPLEMENTO1))
            elif re.match(er_complemento2, palabra):
                self.tokens.append((TT_COMPLEMENTO2))
            elif re.match(er_objeto1, palabra):
                self.tokens.append((TT_OBJETO1))
            elif re.match(er_objeto2, palabra):
                self.tokens.append((TT_OBJETO2))   
            else:
                return [], PalabraIlegalError('"'+ palabra +'"')
                
        return self.tokens

#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        
    def parse(self):
        array_tokens = self.tokens
        
        if len(array_tokens) != 0:
            if array_tokens[0] == TT_ACTIVADOR:
                if array_tokens[1] == TT_INSTRUCCION:
                    if array_tokens[2] == TT_COMPLEMENTO1 and array_tokens[3] == TT_OBJETO1:
                        return "C1"
                    elif array_tokens[2] == TT_COMPLEMENTO2 and array_tokens[3] == TT_OBJETO1:
                        return "C2"
                    elif array_tokens[2] == TT_COMPLEMENTO1 and array_tokens[3] == TT_OBJETO2:
                        return "C3"
                    elif array_tokens[2] == TT_COMPLEMENTO2 and array_tokens[3] == TT_OBJETO2:
                        return "C4"
            return "comando invalido"
        return ""

#######################################
# INTERPRETER
#######################################

class Interpreter:
    def __init__(self, parser_result):
        self.parser_result = parser_result
    
    
    def interpret(self):
        if self.parser_result != "":
            if self.parser_result == "C1":
                print("Executing: Turn on TV")
            elif self.parser_result == "C2":
                print("Executing: Turn off TV")
            elif self.parser_result == "C3":
                print("Executing: Turn on Fan")
            elif self.parser_result == "C4":
                print("Executing: Turn off Fan")
            elif self.parser_result == "comando invalido":
                ComandoIlegalError("Estructura sintactica invalida.")
             

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
    main("Living turn on fan")    
    main("libby turn off Fan")   
    main("libby turn off light")
    main("libby turn off computer")  
    main("LIBBY turn off Fan")    
    main("fan libby turn off") 
    main("turn off tv libby")   
    main("Libby off turn Fan")  


