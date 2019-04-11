
# Created on 4 Feb. 2019 y.
# @author: Jurij Bakhtin

from builtins import str
import sys
import os
import re

import scanner

operations = [ "mult", "div", "mod", "plus", "minus", "eq", "ne", "lt", "gt", "le", "ge"]

# Функции описания

def dfn(tokens_list, i):
    xml_tree = ''
    xml_subtree = ''
    length = 1

    try:
        type = tokens_list[i].value
        i += 1

        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error. Line ' + str(tokens_list[i].line_number) + '. После TYPE должно идти имя переменной')
            sys.exit(0) # Ошибка в правле описания
        name = tokens_list[i].value
        i += 1

        if tokens_list[i].value is '[':
            i += 1
            if not re.search(r'lex:TypeInt', tokens_list[i].get_description()):
                print('Error. Line ' + str(tokens_list[i].line_number) + ". После открывающей скобки должно идти число тапа INT")
                sys.exit(0)  # Ошибка в правле описания
            length = tokens_list[i].value
            i += 1

            if tokens_list[i].value is not ']':
                print('Error. Line ' + str(tokens_list[i].line_number) + ". Не обнаружена закрывающая скобка")
                sys.exit(0)  # Ошибка в правле описания
            i += 1

        have_brief = False
        while i < len(tokens_list):
            if tokens_list[i].value == ',':
                xml_temp, i = brief(tokens_list, i)
                xml_subtree += xml_temp
                have_brief = True
            else:
                break

        if tokens_list[i].value is not ';':
            print('Error. Line ' + str(tokens_list[i].line_number) + ". Неожиданный символ")
            sys.exit(0)  # Ошибка в правле описания
        i += 1
    except IndexError:
        print('Error. Некорректный конец программы')
        sys.exit(0)  # Ошибка в правле описания

    if not have_brief:
        xml_tree = "<dfn name='" + name + "' length='" + str(length) + "' type='" + type + "'>\n"
    else:
        xml_tree = "<dfn type='" + type + "'>\n" + xml_subtree + "</dfn>\n"

    return (xml_tree, i)

def brief(tokens_list, i):
    xml_tree = ''
    length = 1

    try:
        if tokens_list[i].value != ',':
            return (xml_tree, i) # Не распознано как brief
        i += 1

        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error. Line ' + str(tokens_list[i].line_number) + '. После TYPE должно идти имя переменной')
            sys.exit(0)  # Ошибка в правле описания
        name = tokens_list[i].value
        i += 1

        if tokens_list[i].value is '[':
            i += 1
            if not re.search(r'lex:TypeInt', tokens_list[i].get_description()):
                print('Error. Line ' + str(
                    tokens_list[i].line_number) + ". После открывающей скобки должно идти число тапа INT")
                sys.exit(0)  # Ошибка в правле описания
            length = tokens_list[i].value
            i += 1

            if tokens_list[i].value is not ']':
                print('Error. Line ' + str(tokens_list[i].line_number) + ". Не обнаружена закрывающая скобка")
                sys.exit(0)  # Ошибка в правле описания
            i += 1

    except IndexError:
        print('Error. Некорректный конец программы')
        sys.exit(0)  # Ошибка в правле описания

    xml_tree = "<brief name='" + name + "' length='" + str(length) + "'>\n"

    return (xml_tree, i)

# Функции процедур

def proc(tokens_list, i):
    xml_tree = ''

    xml_tree += "<proc>\n"

    try:
        i += 1

        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error. Line ' + str(tokens_list[i].line_number) + '. Процедура должна иметь имя')
            sys.exit(0)  # Ошибка в правле описания
        name = tokens_list[i].value
        i += 1

        have_brief = False
        while i < len(tokens_list):
            if tokens_list[i].value.lower() == 'int' or tokens_list[i].value.lower() == 'real':
                xml_subtree, i = dfn(tokens_list, i)  # Описание
                xml_tree += xml_subtree
            else:
                break

        if not tokens_list[i].value.lower() == 'start':
            print('Error. Line ' + str(tokens_list[i].line_number) + '. Процедура должна иметь тело')
            sys.exit(0)  # Ошибка в правле описания
        else:
            xml_subtree, i = compound(tokens_list, i)  # Описание
            xml_tree += xml_subtree

    except IndexError:
        print('Error. Некорректный конец программы')
        sys.exit(0)  # Ошибка в правле описания

    xml_tree += "</proc>\n"

    return (xml_tree, i)

# функции операторов

def clause(tokens_list, i): # Оператор
    xml_tree = ''

    if tokens_list[i].value.lower() == 'write':
        xml_subtree, i = write(tokens_list, i)  # оператор write
        xml_tree += xml_subtree
    else:
        return(xml_tree, i)

    return(xml_tree, i)

def compound(tokens_list, i): # Составной оператор
    xml_tree = ''
    xml_tree += "<compound>\n"

    try:
        if tokens_list[i].value != 'start':
            print('Error. Line ' + str(tokens_list[i].line_number) + '. Составной оператор должне начинаться со "start"')
            sys.exit(0)  # Ошибка в правле описания
        name = tokens_list[i].value
        i += 1

        if tokens_list[i].value != 'finish':
            while i < len(tokens_list):
                temp = i
                xml_subtree, i = clause(tokens_list, i)  # Оператор
                xml_tree += xml_subtree
                if temp == i and tokens_list[i].value != 'finish':
                    print('Error. Line ' + str(tokens_list[i].line_number) + '. Нераспознанная конструкция')
                    sys.exit(0)  # Ошибка в правле описания
                else:
                    break
                # добавить обработку точку с запятой
        else:
            print( 'Error. Line ' + str(tokens_list[i].line_number) + '. Составной оператор не должен быть пустым')
            sys.exit(0)  # Ошибка в правле описания

        if tokens_list[i].value != 'finish':
            print('Error. Line ' + str(tokens_list[i].line_number) + '. Составной оператор должне начинаться со "finish"')
            sys.exit(0)  # Ошибка в правле описания
        name = tokens_list[i].value
        i += 1

    except IndexError:
        print('Error. Некорректный конец программы')
        sys.exit(0)  # Ошибка в правле описания

    xml_tree += "</compound>\n"

    return (xml_tree, i)

def write(tokens_list, i): # Оператор записи
    xml_tree = ''

    xml_tree += "<write>\n"

    try:
        i += 1

        if tokens_list[i].value not in operations:
            print('Error. Line ' + str(tokens_list[i].line_number) + '. Процедура должна иметь имя')
            sys.exit(0)  # Ошибка в правле описания
        else:
            xml_subtree, i = expressions(tokens_list, i)  # Описание
            xml_tree += xml_subtree

    except IndexError:
        print('Error. Некорректный конец программы')
        sys.exit(0)  # Ошибка в правле описания

    xml_tree += "</write>\n"

    return (xml_tree, i)

def expressions(tokens_list, i): # выражеине
    xml_tree = ''

    xml_tree += "<expr>\n"

    try:
        if tokens_list[i].value not in operations:
            print('Error. Line ' + str(tokens_list[i].line_number) + '. Ожидавется операция')
            sys.exit(0)  # Ошибка в правле описания
        operator = tokens_list[i].value
        i += 1

        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error. Line ' + str(tokens_list[i].line_number) + '. Выражение должно содержать операнд')
            sys.exit(0)  # Ошибка в правле описания
        operand_1 = tokens_list[i].value
        i += 1

        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error. Line ' + str(tokens_list[i].line_number) + '. Выражеине не содержит второго операнда')
            sys.exit(0)  # Ошибка в правле описания
        operand_2 = tokens_list[i].value
        i += 1

    except IndexError:
        print('Error. Некорректный конец программы')
        sys.exit(0)  # Ошибка в правле описания

    xml_tree += "<" + operator + ">\n" + \
                "<op kind='" + operand_1 + "'>\n" + \
                "<op kind='" + operand_2 + "'>\n" + \
                "</" + operator + ">\n"
    xml_tree += "</expr>\n"

    return (xml_tree, i)

# парсер
def parser(tokens_list):
    xml_tree = '<?xml version="1.0" ?>' + '\n'
    xml_tree += '<program>' + '\n'

    i = 0
    while i < len(tokens_list):
        if tokens_list[i].value.lower() == 'int' or tokens_list[i].value.lower() == 'real':
            xml_subtree, i  = dfn(tokens_list, i) #Описание
            xml_tree += xml_subtree
        elif tokens_list[i].value.lower() == 'proc':
            xml_subtree, i = proc(tokens_list, i)  # процедура
            xml_tree += xml_subtree
        elif True:
            xml_subtree, i = clause(tokens_list, i)
            xml_tree += xml_subtree
        else:
            break



    xml_tree += '</program>'

    return (xml_tree, None)

def main(file_programm, file_tokens, file_xml_tree):
    # Сегмент лексического анализа
    with open(file_programm, 'r') as input_file_program:
        tokens_list = scanner.scanner(input_file_program)

    errors = False
    with open(file_tokens, 'w') as output_file_tokens:
        for token in tokens_list:
            line = token.get_description()
            output_file_tokens.write(line + '\n')

            if token.definite_lexeme is 'Error':
                line = 'Error:' + str(token.get_line_number()) + token.get_error_description()

                print(line)
                errors = True


    # Сегмент синтаксического анализа
    if not errors:
        # Изменить на вывод соответствующий ТЗ на финальном этапе разработки
        #print('OK. Lexical analysis completed successfully')
        xml_tree, line_error = parser(tokens_list)

        if line_error is None:
            with open(file_xml_tree, 'w') as output_file_xml_tree:
                output_file_xml_tree.write(xml_tree)
                # print('OK. Parsing completed successfully')
                print('OK')

        else:
            print(line_error)
    else:
        sys.exit(0)



if __name__ == '__main__':
    if not len(sys.argv) < 4:
        if os.stat(sys.argv[1]).st_size is not 0:
            main(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            print("Error. Input file is empty")
    else:
        print('Error. Parameters are incorrect')