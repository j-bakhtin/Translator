
# Created on 4 Feb. 2019 y.
# @author: Jurij Bakhtin

from builtins import str
import sys
import os
import re

import scanner

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
            return (xml_tree, i)  # Не распознано как brief
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

    xml_tree = "<brief name='" + name + "' length='" + str(length) + ">\n"

    return (xml_tree, i)

# Функции процедур

def proc(tokens_list, i):
    pass

def parser(tokens_list):
    xml_tree = '<?xml version="1.0" ?>' + '\n'
    xml_tree += '<program>' + '\n'

    i = 0
    while i < len(tokens_list):
        if tokens_list[i].value.lower() == 'int' or tokens_list[i].value.lower() == 'real':
            xml_subtree, i  = dfn(tokens_list, i) #Описание
            xml_tree += xml_subtree
        elif tokens_list[i].value.lower() == 'Proc':
            xml_subtree, i = proc(tokens_list, i)  # процедура
            xml_tree += xml_subtree
        elif False:
            pass # Оператор
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
        print('OK. Lexical analysis completed successfully')
        xml_tree, line_error = parser(tokens_list)

        if line_error is None:
            with open(file_xml_tree, 'w') as output_file_xml_tree:
                output_file_xml_tree.write(xml_tree)
                print('OK. Parsing completed successfully')
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