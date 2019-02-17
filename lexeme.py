
# Created on 4 Feb. 2019 y.
# @author: Jurij Bakhtin

from builtins import str
import sys
import os

# -*- Символы ограничители
limiters = {
            '(': 'LRB',
            ')': 'RRB',
            '[': 'LSB',
            ']': 'RSB',
            '{': 'LCB',
            '}': 'RCB',
            ':': 'Colon',
            ',': 'Comma',
            ';': 'Semicolon'}

# Зарезервированные операторы
reserved_operators = {
            '+': 'Add',
            '-': 'Min',
            '*': 'Mul',
            '<': 'LT',
            '>': 'GT'}

# Зарезервированные составные операторы
reserved_composite_operators = {
            '==': 'EQ',
            '!=': 'NE',
            '<': 'LT',
            '>': 'GT',
            '<=': 'LE',
            '>=': 'GE',
            ':=': 'Let'}

# -*- Зарезервированные слова
reserved_words = ['Div', 'Mod', 'Cast', 'Box','End', 'Int', 'Vector', 'TypeInt', 'TypeReal', 'Goto', 'Read',
                  'Break', 'Tools', 'Proc', 'Call', 'If', 'Case', 'Then', 'Else', 'Of', 'Or', 'While', 'Loop', 'Do']

# Оставшиеся конструкции     
#             'Comment'
#             'Id'
#             'Label'
#             'Var'
#             'Skip
#             'Space'
#             'Tab'


# -*- Класс, описывающий лексему в формате <номер строки>lex:<лексема>[<тип>:<распознанное_значение>][val:<значение>]
class Lexeme:

    def __init__(self, line_number, value, exception=None):
        self.line_number = str(line_number)
        self.value = str(value)
        self.exception = exception
    
    # -*- Полное описание лексемы -*-
    def get_description(self):
        description = self.line_number

        if self.exception == 'Error':
            description += 'lex:' + 'Error' + 'val:' + self.value
        elif self.exception == 'Comment':
            description += 'lex:' + 'Comment'
        elif self.value in reserved_words:
            description += 'lex:' + self.value + 'val:' + self.value
        elif self.value in limiters.keys():
            description += 'lex:' + limiters.get(self.value) + 'val:' + self.value
        elif self.value in reserved_operators.keys():
            description += 'lex:' + reserved_operators.get(self.value) + 'val:' + self.value
        elif self.value in reserved_composite_operators.keys():
            description += 'lex:' + reserved_composite_operators.get(self.value) + 'val:' + self.value
        else:
            try: 
                if type(int(self.value)) is int:
                    description += 'lex:' + 'TypeInt' + type(int(self.value)).__name__ +\
                                   ':' + self.value + 'val:' + self.value
                    return description
            except ValueError:   
                pass
                
            try: 
                if type(float(self.value)) is float:
                    description += 'lex:' + 'TypeRal' + type(float(self.value)).__name__ +\
                                   ':' + self.value + 'val:' + self.value
                    return description
            except ValueError:   
                description += 'lex:' + 'Id' + 'val:' + self.value

        return description


# -*- Определение принадлежности символа к классу букв -*-
def is_letter(ch):
    return ('A' <= ch <= 'Z') or ('a' <= ch <= 'z')

  
# -*- Определение принадлежности символа к классу двоичных цифр -*-
def is_bin(ch):
    return ch == '0' or ch == '1'

   
# -*- Определение принадлежности символа к классу восьмиричных цифр -*- 
def is_octal(ch):
    return '0' <= ch <= '7'


# -*- Определение принадлежности символа к классу десятичных цифр -*-
def is_digit(ch):
    return '0' <= ch <= '9'


# -*- Определение принадлежности символа к классу шестнадцатеричныхцифр -*-
def is_hex(ch):
    return ('0' <= ch <= '9') or ('A' <= ch <= 'F') or ('a' <= ch <= 'f')
    

# -*-Определение принадлежности символа к классу пропусков -*-
def is_skip(ch):
    return ch == ' ' or ch == '\t' or ch == '\n' or ch == '\f'


# -*- Определяет принадлежность к классу игнорируемых символов -*-
def is_ignore(ch):
    return chr(0) < ch < ' ' and ch != '\t' and ch != '\n' and ch != '\f'


def is_reserved(ch):
    return ch in reserved_words


def is_limiters(ch):
    return ch in limiters


# ===============================================================================
# Лексический анализатор (Сканер)
# Принимает фал с программой
# Возвращает список сописанием лексем
# Формат описания лексемы: <номер строки>lex:<лексема>[<тип>:<распознанное_значение>][val:<значение>]
# ===============================================================================
def scanner(file_program):
    obj_list = []

    for line_number, line in enumerate(file_program):
        index_in_line = 0
        lexeme = ''
        while index_in_line < len(line):
            exception = False

            if is_skip(line[index_in_line]):
                index_in_line += 1
                continue
            
            if is_limiters(line[index_in_line]):
                lexeme = lexeme + line[index_in_line]
                obj = Lexeme(line_number, lexeme)
                obj_list.append(obj)
                lexeme = ''
                index_in_line += 1
                continue
                    
            if is_letter(line[index_in_line]):
                lexeme = lexeme + line[index_in_line]
                index_in_lexeme = index_in_line + 1
                while index_in_lexeme < len(line):

                    if is_letter(line[index_in_lexeme]):
                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue
                    
                    elif is_digit(line[index_in_lexeme]):
                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue
                    
                    elif line[index_in_lexeme] == '_':
                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue
                        
                    elif is_skip(line[index_in_lexeme]):
                        if is_reserved(lexeme.lower()):
                            obj = Lexeme(line_number, lexeme)
                            obj_list.append(obj)
                        index_in_line = index_in_lexeme
                        lexeme = ''
                        break
                    
                    elif is_limiters(line[index_in_lexeme]):
                        obj = Lexeme(line_number, lexeme)
                        obj_list.append(obj)
                        lexeme = ''
                        index_in_line = index_in_lexeme
                        break
                    
                    else:
                        lexeme = ''
                        index_in_line = index_in_lexeme
                        break
                continue
            
            if is_digit(line[index_in_line]):
                lexeme = lexeme + line[index_in_line]
                index_in_lexeme = index_in_line + 1
                
                while index_in_lexeme < len(line):
                    if is_digit(line[index_in_lexeme]):
                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue
                    
                    elif is_letter(line[index_in_lexeme]):
                        exception = 'Error'
                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue
                    
                    elif line[index_in_lexeme] == '.':
                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue 
                      
                    elif is_skip(line[index_in_lexeme]):
                        obj = Lexeme(line_number, lexeme, exception)
                        obj_list.append(obj)
                        lexeme = ''
                        index_in_line = index_in_lexeme
                        break
                    
                    elif is_limiters(line[index_in_lexeme]):
                        obj = Lexeme(line_number, lexeme, exception)
                        obj_list.append(obj)
                        lexeme = ''
                        index_in_line = index_in_lexeme
                        break
                    
                    else:
                        lexeme = ''
                        index_in_line = index_in_lexeme
                        break
                    
                index_in_line += 1
                continue
            
            index_in_line += 1
                        
    return obj_list


# -*- Главная функция -*-
def main(fp, fl):
    obj_list = []

    with open(fp) as input_file_program:
        obj_list = scanner(input_file_program)
        
    for obj in obj_list:
        print(obj.get_description())


if __name__ == '__main__':
    if len(sys.argv) != 1:
        if os.stat(sys.argv[1]).st_size != 0:
            main(sys.argv[1], sys.argv[2])
        else:
            print("Input file is empty")
    else:
        print('Parameters not found')
