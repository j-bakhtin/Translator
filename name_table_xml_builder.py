# Created on 27 May. 2019 y.
# @author: Jurij Bakhtin

from builtins import str
import sys
import os
import lxml.etree as ET

import scanner
import syntax_tree_xml_builder

def prettify(element, indent='  '):
    queue = [(0, element)]  # (level, element)
    while queue:
        level, element = queue.pop(0)
        children = [(level + 1, child) for child in list(element)]
        if children:
            element.text = '\n' + indent * (level+1)  # for child open
        if queue:
            element.tail = '\n' + indent * queue[0][0]  # for sibling open
        else:
            element.tail = '\n' + indent * (level-1)  # for parent close
        queue[0:0] = children  # prepend so children come before siblings

def find_definitions(subtree, parent):
    for child in subtree.iter('dfn'):

        type_value = child.attrib['type']

        if len(child.attrib) == 1:
            for brief in child.findall('brief'):
                entry = ET.SubElement(parent, 'entry')
                name_value = brief.attrib['name']
                length_value = brief.attrib['length']

                entry.set('type', type_value)
                entry.set('name', name_value)
                entry.set('length', length_value)
                entry.set('ref', '1')
        else:
            entry = ET.SubElement(parent, 'entry')
            name_value = child.attrib['name']
            length_value = child.attrib['length']

            entry.set('type', type_value)
            entry.set('name', name_value)
            entry.set('length', length_value)
            entry.set('ref', '1')

def name_table_xml_builder(tree):

    name_table_tree = ET.Element('table')
    root = tree.getroot()

    proc_list = tree.findall('proc')
    for proc in proc_list:
        proc_parent = proc.getparent()
        proc_parent.remove(proc)

    find_definitions(root, name_table_tree)

    for proc in proc_list:
        name_proc = proc.attrib['name']
        entry_proc = ET.SubElement(name_table_tree, 'entry', {'name':name_proc, 'type':'proc', 'ref':'1'})
        find_definitions(proc, entry_proc)

    #Подсчет ссылок на переменную
    for var in root.iter('var'):
        name_var = var.get('name')

        for entry in name_table_tree:
            name_entry = entry.get('name')
            type_entry = entry.get('type')

            if name_var == name_entry and type_entry != 'type':
                count_ref = int(entry.get('ref'))
                count_ref += 1
                entry.set('ref', str(count_ref))

    #Проверки по заданию

    # 1.1 Допускается присваивание целочисленных значений переменным действительного типа
    #(неявное приведение типов).
    for assign in root.iter('assign'):

        name_var_left = assign.find('var').get('name')

        entrys = {}
        for entry in name_table_tree:  # Проверяем, объявлена ли переменная слева
            name_entry = entry.get('name')
            entrys.update({name_entry:entry})

        if name_var_left != entrys.get(name_var_left).get('name'):
            print('Error.Переменная слева не объявлена')
            exit(0)

        type_var_left = entrys.get(name_var_left).get('type')

        if type_var_left == 'int':
            for operand in assign.iter('op'): # Анализируем операнд справа

                type_operand = operand.get('type')

                if type_operand != None:
                    if type_var_left != type_operand:
                        print('Error:0:Нельзя присвоить переменной типа Int вещественное значение')
                        exit(0)


            expr = assign.find('expr')

            for var_right in expr.iter('var'): # Анализируем операнд справа
                name_var_right = var_right.get('name')

                entrys = {}
                for entry in name_table_tree:  # Проверяем, объявлена ли переменная слева
                    name_entry = entry.get('name')
                    entrys.update({name_entry: entry})

                if name_var_right != entrys.get(name_var_right).get('name'):
                    print('Error:0:Переменная справа не объявлена')
                    exit(0)

                type_var_right = entrys.get(name_var_right).get('type')
                print(type_var_left, type_var_right)

                if type_var_right != None:
                    if type_var_left != type_var_right:
                        print('Error:0:Нельзя присвоить переменной типа Int переменную типа Real')
                        exit(0)




    #Косметические преобразования дерева для вывода
    prettify(name_table_tree)
    tree = ET.ElementTree(name_table_tree)
    return(tree)

def main(file_programm, file_tokens, file_xml_tree):
    tokens_list_without_comment = []

    # Сегмент лексического анализа
    with open(file_programm, 'r') as input_file_program:
        tokens_list = scanner.scanner(input_file_program)

    errors = False
    with open(file_tokens, 'w') as output_file_tokens:
        for token in tokens_list:
            line = token.get_description()
            if token.lexeme != 'Comment':
                tokens_list_without_comment.append(token)
                output_file_tokens.write(line + '\n')

            if token.definite_lexeme is 'Error':
                line = 'Error:' + str(token.get_line_number()) + token.get_error_description()

                print(line)
                errors = True


    # Сегмент синтаксического анализа
    if not errors:
        xml_tree = syntax_tree_xml_builder.xml_builder(tokens_list_without_comment)

        with open(file_xml_tree, 'w') as output_file_xml_tree:
            output_file_xml_tree.write(xml_tree)
            #print('OK')
    else:
        sys.exit(0)

    # Сегмент Семантического анализа
    tree = ET.parse(file_xml_tree)

    xml_tree = name_table_xml_builder(tree)

    with open('name_table.txt', 'w') as output_file_xml_tree:
        xml_tree.write('name_table.txt')

    print('OK')

if __name__ == '__main__':
    if not len(sys.argv) < 4:
        if os.stat(sys.argv[1]).st_size is not 0:
            main(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            print("Error. Input file is empty")
            with open(sys.argv[3], 'w') as output_file_xml_tree:
                output_file_xml_tree.write('<?xml version="1.0" ?>')
    else:
        print('Error. Parameters are incorrect')