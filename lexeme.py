'''
Created on 4 Feb. 2019 y.

@author: Jurij Bakhtin
'''
from builtins import str
import sys


# -*- Класс, описывающий лексему в формате <строка>lex:<лексема>[<тип>:<распознанное_значение>][val:<значение>] -*-
class Lexeme:
    def __init__(self, lineNumber, lexeme, recognizedValue, value):
        self.lineNumber = lineNumber
        self.lexeme = lexeme
        self.recognizedValue = recognizedValue
        self.value = value
    
    
    # -*- Полное описание лексемы -*-
    def description(self):
        return(self.lineNumber + 'lex:' + self.lexeme + ':'+self.recognizedValue + 'val:' + self.value) 
    
    
# -*- Определение принадлежности символа к классу букв -*-
def isLetter(ch):
    if (ch >= 'A' and ch <= 'Z') or (ch >= 'a' and ch <= 'z'):
        return True
    else:
        return False

  
# -*- Определение принадлежности символа к классу двоичных цифр -*-
def isBin(ch):
    if((ch == '0' or ch == '1')):
        return True
    else:
        return False

   
# -*- Определение принадлежности символа к классу восьмиричных цифр -*- 
def isOctal(ch):
    if((ch >= '0' and ch <= '7')):
        return True
    else:
        return False


# -*- Определение принадлежности символа к классу десятичных цифр -*-
def isDigit(ch):
    if((ch >= '0' and ch <= '9')):
        return True
    else:
        return False


# -*- Определение принадлежности символа к классу шестнадцатеричныхцифр -*-
def isHex(ch):
    if((ch >= '0' and ch <= '9') or (ch >= 'A' and ch <= 'F') or (ch >= 'a' and ch <= 'f')):
        return True
    else:
        return False
    

# -*-Определение принадлежности символа к классу пропусков -*-
def isSkip(ch):
    if(ch == ' ' or ch == '\t' or ch == '\n' or ch == '\f'):
        return True
    else:
        return False

# -*- Определяет принадлежность к классу игнорируемых символов -*-
def isIgnore(ch):
    if (ch > 0 and ch < ' ' and ch != '\t' and ch != '\n' and ch !='\f'):
        return True
    else:
        return False


def transliterator(ch):
    pass


# -*- Лексический анализатор. Принимает целый файл-*-
def scanner(file_programm):
    lexems = [] # Список лексем.
    lexem = ''  # Обрабатываемая лексема
    ch_index_in_line = 0 # Индекс обрабатываемого символа
    # Разбиваем вхожной поток по строкам
    for line_number, line in enumerate(file_programm):
        # Блок транслитератор?!    <<<---
        # Начинаем перебор символов
        for ch_index_in_line in range(len(line)):
            # Если БУКВА, то начинаем обрабатывать возможные лексемы:
            #  - ЗАРЕЗЕРВИРОВАННАЯ ИНСТРУКЦИЯ
            #  - ИДЕНТИФИКАТОР
            #  - ... Дописать    <<<---
            if isLetter(line[ch_index_in_line]):
                # Заполняем лексему 
                lexem = lexem + line[ch_index_in_line]
                # Обрабатываем дальш потенциальную лексему
                for ch_index_in_line in range(ch_index_in_line + 1, len(line)):
                    # Если последующий символ БУКВА то
                    if isLetter(line[ch_index_in_line]):
                        # Заполняем лесему
                        lexem = lexem + line[ch_index_in_line]
                        # Продолжаем обработку возможной лексемы
                        continue
                    # Иначе, если разделяющий символ, то определена лексема (ИДЕНТИФИКАТОР или ЗАРЕЗЕРВИРОВАННАЯ ИНСТРУКЦИЯ)
                    elif isSkip(line[ch_index_in_line]):
                        # Заканчиваем обраьотку лесемы
                        break
                    # Если символ не определен, то предположение о возможной лексеме ложно
                    else:
                        # Обнуляем обрабатываемую лесему
                        lexem = ''
                        # Заканчиваем обраьотку лесемы
                        break
            # Переходим к следующей строке файла
            break
        # При этом, если лексема была обнаружена, то
        if not lexem == '':
            # добаляем ее в список лексем
            lexems.append(lexem)
            # И обнуляем обрабатываемую лексему
            lexem = ''
    
    print(lexems)

# -*- Главная функция -*-
def main(fp, fl):
    with open(fp) as input_file_programm:
        scanner(input_file_programm)
    
#         lexems = []
#         for line, i in enumerate(input_file_programm):
#             lexems.append(scanner(line))
#         
#         for lex in lexems:      
#             print(lex.description())


if __name__ == '__main__':
    if not len(sys.argv) == 1:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Parametrs not found')
