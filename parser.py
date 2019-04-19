
# Created on 4 Feb. 2019 y.
# @author: Jurij Bakhtin

from builtins import str
import sys
import os
import re

import scanner

operations = ["mult", "div", "mod", "plus", "minus", "eq", "ne", "lt", "gt", "le", "ge"]
qualifier = ['skip', 'space', 'tab']
reserved_words = ['Box', 'End', 'Int', 'Real', 'Vector', 'TypeInt', 'TypeReal', 'Goto', 'Read', 'Var', 'Loop', 'Do',
                  'Break', 'Tools', 'Proc', 'Call', 'If', 'Case', 'Then', 'Else', 'Of', 'Or', 'While']


# Функции описания
def dfn(tokens_list, i):
    xml_subtree = ''
    length = 1

    try:
        type = tokens_list[i].value
        i += 1

        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error:' + str(tokens_list[i].line_number) + ':После TYPE должно идти имя переменной')
            sys.exit(0)
        name = tokens_list[i].value
        i += 1

        if tokens_list[i].value is '[':
            i += 1
            if not re.search(r'lex:TypeInt', tokens_list[i].get_description()):
                print('Error:' + str(tokens_list[i].line_number) +
                      ":После открывающей скобки должно идти число тапа INT")
                sys.exit(0)
            length = tokens_list[i].value
            i += 1

            if tokens_list[i].value is not ']':
                print('Error:' + str(tokens_list[i].line_number) + ":Не обнаружена закрывающая скобка")
                sys.exit(0)
            i += 1

        have_brief = False
        while i < len(tokens_list):
            if tokens_list[i].value == ',':
                xml_temp, i = brief(tokens_list, i)
                xml_subtree += xml_temp
                have_brief = True
            else:
                break

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    if not have_brief:
        xml_tree = "<dfn name='" + name + "' length='" + str(length) + "' type='" + type + "'>\n"
    else:
        xml_tree = "<dfn type='" + type + "'>\n" + \
                   "<brief name='" + name + "' length='" + str(length) + "'>\n" + \
                   xml_subtree + "</dfn>\n"

    return xml_tree, i


def brief(tokens_list, i):
    xml_tree = ''
    length = 1

    try:
        if tokens_list[i].value != ',':
            return xml_tree, i  # Не распознано как brief
        i += 1

        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error:' + str(tokens_list[i].line_number) + ':Ожиидается имя переменной')
            sys.exit(0)
        name = tokens_list[i].value
        i += 1

        if tokens_list[i].value is '[':
            i += 1
            if not re.search(r'lex:TypeInt', tokens_list[i].get_description()):
                print('Error:' + str(
                    tokens_list[i].line_number) + ":После открывающей скобки должно идти число тапа INT")
                sys.exit(0)
            length = tokens_list[i].value
            i += 1

            if tokens_list[i].value is not ']':
                print('Error:' + str(tokens_list[i].line_number) + ":Не обнаружена закрывающая скобка")
                sys.exit(0)
            i += 1

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree = "<brief name='" + name + "' length='" + str(length) + "'>\n"

    return xml_tree, i


# Функции процедур
def proc(tokens_list, i):
    xml_tree = "<proc>\n"

    try:
        i += 1

        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error:' + str(tokens_list[i].line_number) + ':Процедура должна иметь имя')
            sys.exit(0)
        # Должна иметь имя?
        i += 1

        while i < len(tokens_list):
            if tokens_list[i].value.lower() == 'int' or tokens_list[i].value.lower() == 'real':
                xml_subtree, i = dfn(tokens_list, i)  # Описание
                xml_tree += xml_subtree

                if tokens_list[i].value is not ';':
                    print('Error:' + str(tokens_list[i].line_number) + ":Ожидался символ ';'")
                    sys.exit(0)
                i += 1
            else:
                break


        if not tokens_list[i].value.lower() == 'start':
            print('Error:' + str(tokens_list[i].line_number) + ':Процедура должна иметь тело')
            sys.exit(0)
        else:
            xml_subtree, i = compound(tokens_list, i)  # Составной оператор
            xml_tree += xml_subtree

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "</proc>\n"
    return xml_tree, i


def label_clause(tokens_list, i):
    xml_tree = "<clause>\n"
    try:
        if re.search(r'lex:Label', tokens_list[i].get_description()):
            xml_tree += "<label name='" + tokens_list[i].value.replace(':','') + "'>"
            i += 1
            xml_subtree, i = clause(tokens_list, i)  # Оператор после метки
            xml_tree += xml_subtree
        else:
            xml_subtree, i = clause(tokens_list, i)  # Оператор
            xml_tree += xml_subtree
    except IndexError:
        print('Error:' + str(tokens_list[i - 1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "</clause>\n"
    return xml_tree, i

# функции операторов
def clause(tokens_list, i):  # Оператор
    xml_tree = ''

    try:
        if tokens_list[i].value.lower() == 'write':
            xml_subtree, i = write(tokens_list, i)  # оператор write
            xml_tree += xml_subtree
        elif tokens_list[i].value.lower() == 'read':
            xml_subtree, i = read(tokens_list, i)  # оператор read
            xml_tree += xml_subtree
        elif tokens_list[i].value.lower() == 'goto':
            xml_subtree, i = goto(tokens_list, i)  # оператор read
            xml_tree += xml_subtree
        elif tokens_list[i].value.lower() == 'cast':
            xml_subtree, i = cast(tokens_list, i)  # оператор read
            xml_tree += xml_subtree
        elif tokens_list[i].value.lower() == 'while':
            xml_subtree, i = pwhile(tokens_list, i)  # оператор read
            xml_tree += xml_subtree
        elif tokens_list[i].value.lower() == 'break':
            xml_subtree = "</break>\n"
            xml_tree += xml_subtree
            i += 1
            return xml_tree, i
        elif tokens_list[i].value.lower() == 'let':
            xml_subtree, i = assign(tokens_list, i)  # оператор assign
            xml_tree += xml_subtree
        elif tokens_list[i].value.lower() == 'if':
            xml_subtree, i = pif(tokens_list, i)  # оператор if
            xml_tree += xml_subtree
            return xml_tree, i
        elif  tokens_list[i].value.lower() == 'start':
            xml_subtree, i = compound(tokens_list, i)  # Составной оператор
            xml_tree += xml_subtree
            return xml_tree, i
        else:
            pass

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    return xml_tree, i

def compound(tokens_list, i):  # Составной оператор
    xml_tree = "<compound>\n"

    try:
        if tokens_list[i].value != 'start':
            print('Error:' + str(tokens_list[i].line_number) + ':Составной оператор должне '
                                                                     'начинаться со слова "start"')
            sys.exit(0)
        i += 1

        if tokens_list[i].value != 'stop':
            while i < len(tokens_list):
                temp = i
                xml_subtree, i = label_clause(tokens_list, i)  # Оператор
                xml_tree += xml_subtree
                if tokens_list[i].value != ';':
                    print('Error:' + str(tokens_list[i].line_number) + ":Ожидаеться ';'")
                    sys.exit(0)
                i += 1

                if temp == i or tokens_list[i].value != 'stop':
                    print('Error:' + str(tokens_list[i].line_number) + ':Нераспознанная конструкция')
                    sys.exit(0)

                if tokens_list[i].value == 'stop':
                    i += 1
                    break
        else:
            print('Error:' + str(tokens_list[i].line_number) + ':Составной оператор не должен быть пустым')
            sys.exit(0)

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "</compound>\n"
    return xml_tree, i


def pwhile(tokens_list, i):  # Оператор While
    xml_tree = "<while>\n"

    try:
        i += 1
        xml_subtree, i = expressions(tokens_list, i)  # Выражение
        xml_tree += xml_subtree

        if tokens_list[i].value != 'do':
            print('Error:' + str(tokens_list[i].line_number) + ":Ожидаеться 'do'")
            sys.exit(0)
        else:
            i += 1
            if re.search(r'lex:Label', tokens_list[i].get_description()):
                print('Error:' + str(tokens_list[i].line_number) + ':Нераспознанная конструкция')
                sys.exit(0)
            else:
                xml_subtree, i = label_clause(tokens_list, i)  # Оператор
                xml_tree += xml_subtree

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "</while>\n"
    return xml_tree, i


def cast(tokens_list, i):  # Оператор cast
    xml_tree = "<cast>\n"

    try:
        i += 1
        xml_subtree, i = var(tokens_list, i)  # Оператор
        xml_tree += xml_subtree

        if tokens_list[i].value != ',':
            print('Error:' + str(tokens_list[i].line_number) + ":Ожидаеться ','")
            sys.exit(0)
        else:
            i += 1
            xml_subtree, i = var(tokens_list, i)  # Оператор
            xml_tree += xml_subtree

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "</cast>\n"
    return xml_tree, i


def pif(tokens_list, i):  # Оператор if
    xml_tree = "<if>\n"

    try:
        i += 1

        xml_subtree, i = expressions(tokens_list, i)  # Выражение
        xml_tree += xml_subtree

        if not tokens_list[i].value == 'then':
            print('Error:' + str(tokens_list[i].line_number) + ":Ожидался обяязательное слово 'then'")
            sys.exit(0)
        i += 1


        xml_subtree, i = label_clause(tokens_list, i)  # Выражеине
        xml_tree += xml_subtree

        while i < len(tokens_list):
            if tokens_list[i].value == ';':
                i += 1
                xml_subtree, i = label_clause(tokens_list, i)  # Выражеине
                xml_tree += xml_subtree
            else:
                break

        if tokens_list[i].value == 'else':
            xml_tree += "</if>\n"
            xml_tree += "<else>\n"
            i += 1
            xml_subtree, i = label_clause(tokens_list, i)  # Выражеине
            xml_tree += xml_subtree

            while i < len(tokens_list):
                if tokens_list[i].value == ';':
                    i += 1
                    xml_subtree, i = label_clause(tokens_list, i)  # Выражеине
                    xml_tree += xml_subtree
                else:
                    xml_tree += "</else>\n"

                    break


        if not tokens_list[i].value == 'end':
            print('Error:' + str(tokens_list[i].line_number) + ":Ожидался обяязательное слово 'end'")
            sys.exit(0)
        i += 1

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "</if>\n"
    return xml_tree, i


def assign(tokens_list, i):  # Оператор Assign
    xml_tree = "<assign>\n"

    try:
        i += 1

        xml_subtree, i = var(tokens_list, i)  # Переменная
        xml_tree += xml_subtree

        if not tokens_list[i].value == ',':
            print('Error:' + str(tokens_list[i].line_number) + ":Ожидался символ ','")
            sys.exit(0)
        i += 1

        xml_subtree, i = expressions(tokens_list, i)  # Выражеине
        xml_tree += xml_subtree

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "</assign>\n"
    return xml_tree, i


def goto(tokens_list, i):  # Оператор goto
    try:
        i += 1
        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error:' + str(tokens_list[i].line_number) + ':Ожидаеться имя метки')
            sys.exit(0)
        label = tokens_list[i].value
        i += 1

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree = "<goto label='" + label + "'>\n"
    return xml_tree, i


def write(tokens_list, i):  # Оператор Write
    xml_tree = "<write>\n"

    try:
        i += 1
        while i < len(tokens_list):
            if tokens_list[i].value in qualifier:
                xml_tree += "<qualifier kind='" + tokens_list[i].value + "'>\n"
                i += 1
            else:
                xml_subtree, i = expressions(tokens_list, i)  # Выражеине
                xml_tree += xml_subtree

            if i < len(tokens_list):
                if tokens_list[i].value != ',':
                    break
                else:
                    i += 1
            else:
                break

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "</write>\n"
    return xml_tree, i


def read(tokens_list, i):  # Оператор Read
    xml_tree = "<read>\n"

    try:
        i += 1

        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error:' + str(tokens_list[i].line_number) + ':Ожидалось имя переменной')
            sys.exit(0)
        else:
            xml_subtree, i = var(tokens_list, i)  # Переменная
            xml_tree += xml_subtree

        while i < len(tokens_list):
            if tokens_list[i].value == ',':
                i += 1
                xml_temp, i = var(tokens_list, i)  # Переменная
                xml_subtree += xml_temp
            else:
                break

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "</read>\n"
    return xml_tree, i


def var(tokens_list, i):  # Переменная
    index = 0

    try:
        if not re.search(r'lex:Id', tokens_list[i].get_description()):
            print('Error:' + str(tokens_list[i].line_number) + ':Ожидалось имя переменной')
            sys.exit(0)
        name = tokens_list[i].value
        i += 1
        if  i < len(tokens_list):
            if tokens_list[i].value is '[':
                i += 1

                if not re.search(r'lex:TypeInt', tokens_list[i].get_description()) and \
                    not re.search(r'lex:Id', tokens_list[i].get_description()):
                    print('Error:' + str(tokens_list[i].line_number) +
                          ":После открывающей скобки должно идти число тапа INT")
                    sys.exit(0)
                index = tokens_list[i].value
                i += 1

                if tokens_list[i].value is not ']':
                    print('Error:' + str(tokens_list[i].line_number) + ':Не обнаружена закрывающая скобка')
                    sys.exit(0)
                i += 1

        if index != 0:
            xml_tree = "<var name='" + name + "' index='" + index + "'>\n"
        else:
            xml_tree = "<var name='" + name + "'>\n"

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    return xml_tree, i


def expressions(tokens_list, i):  # выражеине
    xml_tree = "<expr>\n"

    try:
        if tokens_list[i].value in operations:
            operator = tokens_list[i].value
            xml_tree += "<" + operator + ">\n"
            i += 1

            xml_subtree, i = operand(tokens_list, i)  # Операнд
            xml_tree += xml_subtree

            xml_subtree, i = operand(tokens_list, i)  # Операнл
            xml_tree += xml_subtree
            xml_tree += "</" + operator + ">\n"

        elif tokens_list[i].value == '(':
            i += 1
            if tokens_list[i].value == 'minus':
                i += 1
                xml_tree += "<" + 'minus' + ">\n"
                xml_subtree, i = operand(tokens_list, i)  # Операнд
                xml_tree += xml_subtree
                xml_tree += "</" + 'minus' + ">\n"
            if tokens_list[i].value != ')':
                print('Error:' + str(tokens_list[i].line_number) + ':Ожидаеться закрывающая скобка')
                sys.exit(0)
            i += 1
        else:
            xml_subtree, i = operand(tokens_list, i)  # Операнд
            xml_tree += xml_subtree

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "</expr>\n"
    return xml_tree, i


def operand(tokens_list, i):  # Операнд
    xml_tree = ''

    try:
        if tokens_list[i].value in operations:
            xml_subtree, i = expressions(tokens_list, i)  # Выражение
        elif re.search(r'lex:Id', tokens_list[i].get_description()):
            xml_tree += "<op kind='" + tokens_list[i].value + "'>\n"
            i += 1
            return xml_tree, i
        elif re.search(r'lex:TypeInt', tokens_list[i].get_description()):
            xml_tree += "<op kind='" + tokens_list[i].value + "'>\n"
            i += 1
            return xml_tree, i
        elif re.search(r'lex:TypeReal', tokens_list[i].get_description()):
            xml_tree += "<op kind='" + tokens_list[i].value + "'>\n"
            i += 1
            return xml_tree, i
        else:
            print('Error:' + str(tokens_list[i].line_number) + ':Ожидался операнд')
            sys.exit(0)

    except IndexError:
        print('Error:' + str(tokens_list[i-1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += "<op>\n" + xml_subtree
    xml_tree += "</op>\n"
    return xml_tree, i


# парсер
def parser(tokens_list):
    xml_tree = '<?xml version="1.0" ?>' + '\n'
    xml_tree += '<program>' + '\n'

    try:
        i = 0
        while i < len(tokens_list):
            if tokens_list[i].value.lower() == 'int' or tokens_list[i].value.lower() == 'real':
                xml_subtree, i = dfn(tokens_list, i)  # Описание
                xml_tree += xml_subtree
            elif tokens_list[i].value.lower() == 'proc':
                xml_subtree, i = proc(tokens_list, i)  # процедура
                xml_tree += xml_subtree
            else:
                temp = i
                xml_subtree, i = label_clause(tokens_list, i)  # Оператор
                xml_tree += xml_subtree
                if temp == i:
                    if tokens_list[i].value.lower() == ';':
                        pass
                    else:
                        print('Error:' + str(tokens_list[i].line_number) + ':Нераспознанная конструкция')
                        sys.exit(0)

            if tokens_list[i].value.lower()!= ';':
                print('Error:' + str(tokens_list[i].line_number) + ":Ожидался символ ';'")
                sys.exit(0)
            i += 1

    except IndexError:
        print('Error:' + str(tokens_list[i - 1].line_number) + ':Некорректный конец программы')
        sys.exit(0)

    xml_tree += '</program>'
    return xml_tree


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

            if token.definite_lexeme is 'Comment':
                tokens_list.remove(token)


    # Сегмент синтаксического анализа
    if not errors:
        xml_tree = parser(tokens_list)

        with open(file_xml_tree, 'w') as output_file_xml_tree:
            output_file_xml_tree.write(xml_tree)
            print('OK')
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
