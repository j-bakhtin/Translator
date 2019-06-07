
# Created on 4 Feb. 2019 y.
# @author: Jurij Bakhtin

from builtins import str
import sys
import os
import re

# Символы ограничители
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
            'cast': 'Cast',
            'plus': 'Add',
            'minus': 'Min',
            'mult': 'Mul',
            'lt': 'LT',
            'gt': 'GT',
            'div': 'Div',
            'mod': 'Mod',
            'eq': 'EQ',
            'ne': 'NE',
            'le': 'LE',
            'ge': 'GE',
            'let': 'Let'}

# Управляющие символы
control_words = {
            'skip': 'Skip',
            'space': 'Space',
            'tab': 'Tab'}

# Зарезервированные слова
reserved_words = ['Box', 'End', 'Int', 'Real', 'Vector', 'TypeInt', 'TypeReal', 'Goto', 'Read', 'Var', 'Loop', 'Do',
                  'Break', 'Tools', 'Proc', 'Call', 'If', 'Case', 'Then', 'Else', 'Of', 'Or', 'While', 'Write']


class Lexeme:
    # Класс, описывающий лексему в формате <номер строки>lex:<лексема>[<тип>:<распознанное_значение>][val:<значение>]

    description = ''

    def __init__(self, line_number, value, definite_lexeme=None, error_description=None):
        self.line_number = str(line_number)
        self.lexeme = None
        self.value = str(value)
        self.real_value = None
        self.definite_lexeme = definite_lexeme
        self.error_description = error_description

    # -*- Полное описание лексемы -*-
    def get_description(self):
        description = self.line_number

        if self.definite_lexeme == 'Error':
            self.lexeme = 'Error'
            description += ' lex:' + self.lexeme + ' val:' + self.value
            if self.error_description is None:
                self.error_description = 'invalid syntax'
        elif self.definite_lexeme == 'Comment':
            self.lexeme = 'Comment'
            description += ' lex:' + self.lexeme
        elif self.definite_lexeme == 'Label':
            self.lexeme = 'Label'
            description += ' lex:' + self.lexeme + ' val:' + self.value
        elif self.value.lower() in [x.lower() for x in reserved_words]:
            self.lexeme = self.value.title()
            description += ' lex:' + self.lexeme + ' val:' + self.value
        elif self.value.lower() in limiters.keys():
            self.lexeme = limiters.get(self.value)
            description += ' lex:' + self.lexeme + ' val:' + self.value
        elif self.value.lower() in reserved_operators.keys():
            self.lexeme = reserved_operators.get(self.value)
            description += ' lex:' + self.lexeme + ' val:' + self.value
        elif self.value.lower() in control_words.keys():
            self.lexeme = control_words.get(self.value)
            description += ' lex:' + self.lexeme + ' val:' + self.value
        elif self.definite_lexeme == 'TypeDec':
            self.lexeme = 'TypeInt'
            if re.search(r'[dD]', self.value):
                self.real_value = int(re.sub(r'[dD]', '', self.value),10)
            else:
                self.real_value = self.value
            description += ' lex:' + self.lexeme + ' Int' + \
                           ':' + str(self.real_value) + ' val:' + self.value
        elif self.definite_lexeme == 'TypeReal':
            if -3.4e+38 < float(self.value) < 3.4e+38:
                self.lexeme = 'TypeReal'
                self.real_value = self.value
                description += ' lex:' + self.lexeme + ' ' + type(float(self.value)).__name__ + \
                               ':' + self.real_value + ' val:' + self.value
            else:
                self.lexeme = 'Error'
                description += ' lex:' + self.lexeme + ' val:' + self.value
                self.definite_lexeme = 'Error'
                self.error_description = ':Overflow'
        elif self.definite_lexeme == 'TypeBin':
            self.lexeme = 'TypeInt'
            self.real_value = int(re.sub(r'[bB]', '', self.value), 2)
            description += ' lex:' + self.lexeme + ' ' + type(self.real_value).__name__ + \
                           ':' + str(self.real_value) + ' val:' + self.value
        elif self.definite_lexeme == 'TypeOctal':
            self.lexeme = 'TypeInt'
            self.real_value = int(re.sub(r'[cC]', '', self.value), 8)
            description += ' lex:' + self.lexeme + ' ' + type(self.real_value).__name__ + \
                           ':' + str(self.real_value) + ' val:' + self.value
        elif self.definite_lexeme == 'TypeHex':
            self.lexeme = 'TypeInt'
            self.real_value = int(re.sub(r'[hH]', '', self.value), 16)
            description += ' lex:' + self.lexeme + ' ' + type(self.real_value).__name__ + \
                           ':' + str(self.real_value) + ' val:' + self.value

        else:
            self.lexeme = 'Id'
            description += ' lex:' + self.lexeme + ' val:' + self.value

        return description

    def get_line_number(self):
        return self.line_number

    def get_error_description(self):
        return self.error_description


# Определение принадлежности символа к классу букв -*-
def is_letter(ch):
    return ('A' <= ch <= 'Z') or ('a' <= ch <= 'z') or ch == '_'


# Определение принадлежности символа к классу десятичных цифр -*-
def is_digit(ch):
    return '0' <= ch <= '9'


# Определение принадлежности символа к классу пропусков -*-
def is_skip(ch):
    return ch == ' ' or ch == '\t' or ch == '\n' or ch == '\f' or ch == '\r' or ch == '\v' or ch == '\0'


# Определяет принадлежность к классу игнорируемых символов -*-
def is_control_characters(ch):
    return ch in control_words


def is_reserved_word(ch):
    return ch in reserved_words


def is_reserved_operators(ch):
    return ch in reserved_operators


def is_limiters(ch):
    return ch in limiters


def scanner(file_program):
    # Лексический анализатор (Сканер)
    # Принимает фйал с программой
    # Возвращает список c описанием лексем
    # Формат описания лексемы: <номер строки>lex:<лексема>[<тип>:<распознанное_значение>][val:<значение>]

    obj_list = []

    for line_number, line in enumerate(file_program):
        line_number += 1
        index_in_line = 0
        line += '\0'
        lexeme = ''

        while index_in_line < len(line):
            definite_lexeme = ''
            error_description = ''

            # Обработка отступов
            if is_skip(line[index_in_line]):
                index_in_line += 1
                continue

            # Обработка символов ограничителей
            if is_limiters(line[index_in_line]):
                lexeme = lexeme + line[index_in_line]
                obj = Lexeme(line_number, lexeme)
                obj_list.append(obj)
                lexeme = ''
                index_in_line += 1
                continue

            # Обработка комментария
            if line[index_in_line] is '/':
                lexeme = lexeme + line[index_in_line]
                index_in_lexeme = index_in_line + 1

                if line[index_in_lexeme] is '/':
                    lexeme = lexeme + line[index_in_line]
                    definite_lexeme = 'Comment'
                    obj = Lexeme(line_number, lexeme, definite_lexeme)
                    obj_list.append(obj)
                    index_in_line = len(line) - 1
                else:
                    index_in_line += 1
                lexeme = ''
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

                    elif is_skip(line[index_in_lexeme]):
                        obj = Lexeme(line_number, lexeme, definite_lexeme, error_description)
                        obj_list.append(obj)
                        index_in_line = index_in_lexeme
                        lexeme = ''
                        break

                    elif is_limiters(line[index_in_lexeme]):
                        if line[index_in_lexeme] is ':':
                            definite_lexeme = 'Label'
                            lexeme = lexeme + line[index_in_lexeme]
                            index_in_lexeme += 1

                        obj = Lexeme(line_number, lexeme, definite_lexeme)
                        obj_list.append(obj)
                        lexeme = ''
                        index_in_line = index_in_lexeme
                        break

                    else:
                        definite_lexeme = 'Error'
                        error_description = ':Invalid syntax. ' + "Name can not include '" + line[index_in_lexeme] + "'"

                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue
                continue

            if is_digit(line[index_in_line]) or line[index_in_line] == '-':
                lexeme = lexeme + line[index_in_line]
                index_in_lexeme = index_in_line + 1

                while index_in_lexeme < len(line):

                    if is_digit(line[index_in_lexeme]):
                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue

                    elif is_letter(line[index_in_lexeme]):
                        definite_lexeme = 'Error'
                        error_description = ':Invalid syntax. Name can not begin with digit'

                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue

                    elif re.match(r'[.+-]', line[index_in_lexeme]):
                        if definite_lexeme is '':
                            definite_lexeme = 'TypeReal'
                        elif definite_lexeme is 'TypeReal':
                            definite_lexeme = 'Error'

                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue

                    elif is_skip(line[index_in_lexeme]) or is_limiters(line[index_in_lexeme]):
                        if definite_lexeme is '':
                            definite_lexeme = 'TypeDec'
                        elif definite_lexeme is 'Error':
                            if re.match(r'[0-1]+b$', lexeme.lower()):
                                definite_lexeme = 'TypeBin'
                            elif re.match(r'[0-7]+c$', lexeme.lower()):
                                definite_lexeme = 'TypeOctal'
                            elif re.match(r'[0-9]+d$', lexeme.lower()):
                                definite_lexeme = 'TypeDec'
                            elif re.match(r'[0-9a-fA-F]+h$', lexeme.lower()):
                                definite_lexeme = 'TypeHex'
                            elif re.match(r'^[0-9]+e[+-]?[0-9]+$', lexeme.lower()):
                                definite_lexeme = 'TypeReal'
                            elif re.match(r'^[0-9]+\.[0-9]+e[+-]?[0-9]+$', lexeme.lower()):
                                definite_lexeme = 'TypeReal'
                            elif re.match(r'^[0-9]+\.e[+-]?[0-9]+$', lexeme.lower()):
                                definite_lexeme = 'TypeReal'
                        obj = Lexeme(line_number, lexeme, definite_lexeme, error_description)
                        obj_list.append(obj)
                        lexeme = ''
                        index_in_line = index_in_lexeme
                        break
                    else:
                        definite_lexeme = 'Error'
                        error_description = ':Invalid syntax. ' + "Digit can not include '" + line[index_in_lexeme] + "'"

                        lexeme = lexeme + line[index_in_lexeme]
                        index_in_lexeme += 1
                        continue

                # index_in_line += 1
                continue

            else:
                lexeme = lexeme + line[index_in_line]
                index_in_lexeme = index_in_line + 1

                while index_in_lexeme < len(line):
                    if is_skip(line[index_in_lexeme]) or is_limiters(line[index_in_lexeme]):
                        if re.match(r'^\.[0-9]+e[\+-]?[0-9]+$', lexeme.lower()):
                            definite_lexeme = 'TypeReal'
                        elif re.match(r'^.[0-9]+$', lexeme.lower()):
                            definite_lexeme = 'TypeReal'
                        else:
                            definite_lexeme = 'Error'
                            error_description = ':Invalid syntax. '

                        obj = Lexeme(line_number, lexeme, definite_lexeme, error_description)
                        obj_list.append(obj)
                        lexeme = ''
                        index_in_line = index_in_lexeme
                        break

                    lexeme = lexeme + line[index_in_lexeme]
                    index_in_lexeme += 1
                continue

            index_in_line += 1

    return obj_list


def main(fp, fl):

    with open(fp, 'r') as input_file_program:
        obj_list = scanner(input_file_program)

    errors = False
    with open(fl, 'w') as output_file_program:
        for obj in obj_list:
            line = obj.get_description()
            output_file_program.write(line + '\n')

            if obj.definite_lexeme is 'Error':
                line = 'Error:' + str(obj.get_line_number()) + obj.get_error_description()

                print(line)
                errors = True

    if not errors:
        print('OK')


if __name__ == '__main__':
    if not len(sys.argv) < 3:
        if os.stat(sys.argv[1]).st_size is not 0:
            main(sys.argv[1], sys.argv[2])
        else:
            print("Error. Input file is empty")
    else:
        print('Error:Parameters are incorrect')
