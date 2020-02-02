from enums import Symbols, States

class JsonParser():

    def __init__(self):
        self.json_string = ''
        self.json_object = {}
        self.current_state = States.LVALUE
        self.current_pos = 0
        self.max_len = 0

    def _preprocess(self):
        chars_to_trim = [' ', '\n', '\t', '\r']

        for char in chars_to_trim:
            self.json_string = self.json_string.replace(char, '')

    def tokenize(self, string):
        self.json_string = string
        self._preprocess()

        tokens = []
        temp = ""
        
        for char in self.json_string:
            if char in  Symbols._value2member_map_ :
                if len(temp): tokens.append(temp)
                tokens.append(char)
                temp = ""
            
            else:
                if char != '"': temp += char

        return tokens
    
    def _cast_to_int_or_string(self, token):
        if token[0].isdigit():
            if '.' in token:
                return float(token)
            else:
                return int(token)

        return token

    def array_mapper(self, tokens):
        array = []
        value = None
        current_pos = 0

        while current_pos < len(tokens):
            token = tokens[current_pos]

            if token == Symbols.CURLY_LBRACE.value:
                value, len_traversed = self.json_mapper(tokens[current_pos + 1:])
                current_pos += len_traversed
            
            elif token == Symbols.SQUARE_LBRACE.value:
                value, len_traversed = self.array_mapper(tokens[current_pos + 1:])
                current_pos += len_traversed
            
            elif token == Symbols.COMMA.value:
                array.append(value)
            
            elif token == Symbols.SQUARE_RBRACE.value:
                array.append(value)
                break

            else:
                value = self._cast_to_int_or_string(token)

            current_pos += 1

        return array, current_pos + 1

    def json_mapper(self, tokens):
        dict_map= {}
        key = None 
        value = None
        current_state = States.LVALUE
        current_pos = 0

        while current_pos < len(tokens):
            token = tokens[current_pos]

            if token == Symbols.COLON.value:
                current_state = States.RVALUE
            
            elif current_state is States.RVALUE:
                if token == Symbols.CURLY_LBRACE.value:
                    value, len_traversed = self.json_mapper(tokens[current_pos + 1:])
                    current_pos += len_traversed
            
                elif token == Symbols.SQUARE_LBRACE.value:
                    value, len_traversed = self.array_mapper(tokens[current_pos + 1:])
                    current_pos += len_traversed
                
                elif token == Symbols.COMMA.value:
                    dict_map[key] = value
                    current_state = States.LVALUE
                
                elif token == Symbols.CURLY_RBRACE.value:
                    dict_map[key] = value
                    break
                    
                else:
                    value = self._cast_to_int_or_string(token)
            else:
                key =  token
            
            current_pos += 1

        return dict_map, current_pos + 1

    def parse(self, string):
        self.json_string = string
        tokens = self.tokenize(string)

        if tokens[0] != Symbols.CURLY_LBRACE.value:
            raise Exception("Left Curly brace missing in the beginning")
        
        self.max_len = len(tokens)
        self.current_pos += 1
        return self.json_mapper(tokens[1:])    

