'''
Created on 4 Feb. 2019 y.

@author: Jurij Bakhtin
'''
from builtins import str
from itertools import islice, count
import sys
import os

# -*- Символы ограничители
limeters = [',', '.', '(', ')', '{', '}','[', ']', ':', ';', '+', '-', '*', '/', '<', '>', '@']
# -*- Зарезервированные слова
reserved_words = [ "program", "var", "real", "integer", "begin", "for", "downto", "do", "begin", "end", "writeln" ]

# -*- Класс, описывающий лексему в формате <номер строки>lex:<лексема>[<тип>:<распознанное_значение>][val:<значение>] -*-
class Lexeme:  
    def __init__(self, lineNumber = None, lexeme = None, typeLexeme = None, recognizedValue = None, value = None):
        self.lineNumber = str(lineNumber)
        self.lexeme = str(lexeme)
        self.typeLexeme = str(typeLexeme)
        self.recognizedValue = str(recognizedValue)
        self.value = str(value)
    
    
    # -*- Полное описание лексемы -*-
    def getDescription(self):
        description = ''
        description += self.lineNumber
        if self.lexeme == 'Error':
            description += 'lex:Error' + 'val:' + self.value
            return description
            
        return(self.lineNumber + 'lex:' + self.lexeme + self.typeLexeme + ':'+self.recognizedValue + 'val:' + self.value) 
    
    
    def getDescriptionTable(self):
        return("Номер строки: " + self.lineNumber + '\nЛексема: ' + self.lexeme + '\nТип: ' + self.typeLexeme + 
               '\nРАспознанное значение: ' + self.recognizedValue + '\nЗначение: ' + self.value) 


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
    if (ch > chr(0) and ch < ' ' and ch != '\t' and ch != '\n' and ch !='\f'):
        return True
    else:
        return False


def isReserved(ch):
    return ch in reserved_words


def isLimeters(ch):
    return ch in limeters


def transliterator(ch):
    pass


# -*- Лексический анализатор. Принимает целый файл-*-
def scanner(file_programm):
    lexems = []  # Список лексем.
    obj_list = [] # Список лексем-объектов
    lexem = ''  # Обрабатываемая лексема
    # Разбиваем вхожной поток по строкам
    for line_number, line in enumerate(file_programm):
        index_in_line = 0 # Индекс обрабатываемого символа, обнуляем для каждой строки
        lexem = '' # обнуляем лексему
        # Блок транслитератор?!    <<<---
        # Начинаем перебор символов
        while index_in_line < len(line):
            # Тип лексемы
            name_lexeme = ''
            
            if isSkip(line[index_in_line]):
                index_in_line +=1
                continue
            
            if isLimeters(line[index_in_line]):
                lexem = lexem + line[index_in_line]
                obj = Lexeme(line_number, name_lexeme, lexem, lexem, lexem)
                obj_list.append(obj)
                lexems.append(lexem)
                lexem = ''
                index_in_line +=1
                continue
                    
            # Если БУКВА, то начинаем обрабатывать возможные лексемы:
            #  - ЗАРЕЗЕРВИРОВАННАЯ ИНСТРУКЦИЯ
            #  - ИДЕНТИФИКАТОР
            #  - ... Дописать    <<<---
            if isLetter(line[index_in_line]):
                # Заполняем лексему 
                lexem = lexem + line[index_in_line]
                # Обрабатываем дальш потенциальную лексему
                index_in_lexem = index_in_line + 1
                while index_in_lexem < len(line):
                    # Если последующий символ БУКВА то
                    if isLetter(line[index_in_lexem]):
                        name_lexeme = 'ID'
                        # Заполняем лесему
                        lexem = lexem + line[index_in_lexem]
                        # Продолжаем обработку возможной лексемы
                        index_in_lexem += 1
                        continue
                    elif isDigit(line[index_in_lexem]):
                        name_lexeme = 'ID'
                        # Заполняем лесему
                        lexem = lexem + line[index_in_lexem]
                        # Продолжаем обработку возможной лексемы
                        index_in_lexem += 1
                        continue
                    
                    elif line[index_in_lexem] == '_':
                        lexem = lexem + line[index_in_lexem]
                        index_in_lexem += 1
                        continue
                        
                    # Иначе, если разделяющий символ, то определена лексема (ИДЕНТИФИКАТОР или ЗАРЕЗЕРВИРОВАННАЯ ИНСТРУКЦИЯ)
                    elif isSkip(line[index_in_lexem]):
                        # Добавляем лексему в список
                        lexems.append(lexem)
                        if isReserved(lexem.lower()):
                            obj = Lexeme(lineNumber=line_number, lexeme=reserved_words[reserved_words.index(lexem.lower())], value=lexem)
                            obj_list.append(obj)
                        else:
                            obj = Lexeme(lineNumber=line_number, lexeme=name_lexeme, value=lexem)
                            obj_list.append(obj)
                        # Обнуляем обрабатываемую лексему
                        index_in_line = index_in_lexem
                        lexem = ''
                        # Заканчиваем обраьотку лесемы
                        break
                    
                    elif isLimeters(line[index_in_lexem]):
                        obj = Lexeme(line_number, name_lexeme, lexem, lexem, lexem)
                        obj_list.append(obj)
                        lexems.append(lexem)
                        lexem = ''
                        index_in_line = index_in_lexem
                        break
                    
                    # Если символ не определен, то предположение о возможной лексеме ложно
                    else:
                        # Обнуляем обрабатываемую лесему
                        lexem = ''
                        # Заканчиваем обраьотку лесемы
                        index_in_line = index_in_lexem
                        break
                # Выходим из цикла, чтобы начать обработку новой, потенциальной, лексемы
                continue
            
            if isDigit(line[index_in_line]):
                lexem = lexem + line[index_in_line]
                index_in_lexem = index_in_line + 1
                
                while index_in_lexem < len(line): 
                    if isDigit(line[index_in_lexem]):
                        if name_lexeme != "Error":
                            name_lexeme = "Int"
                        lexem = lexem + line[index_in_lexem]
                        index_in_lexem += 1
                        continue
                    
                    elif isLetter(line[index_in_lexem]):
                        name_lexeme = "Error"
                        lexem = lexem + line[index_in_lexem]
                        index_in_lexem += 1
                        continue
                    
                    elif line[index_in_lexem] == '.':
                        if name_lexeme != "Error":
                            name_lexeme = "Real"
                        lexem = lexem + line[index_in_lexem]
                        index_in_lexem += 1
                        continue 
                      
                    elif isSkip(line[index_in_lexem]):
                        obj = Lexeme(line_number, name_lexeme, lexem, lexem, lexem)
                        obj_list.append(obj)
                        lexems.append(lexem)
                        lexem = ''
                        index_in_line = index_in_lexem
                        break
                    
                    elif isLimeters(line[index_in_lexem]):
                        obj = Lexeme(line_number, name_lexeme, lexem, lexem, lexem)
                        obj_list.append(obj)
                        lexems.append(lexem)
                        lexem = ''
                        index_in_line = index_in_lexem
                        break
                    
                    else:
                        lexem = ''
                        index_in_line = index_in_lexem
                        break
                    
                index_in_line += 1
                continue
            
            index_in_line += 1
                        
    return obj_list


# -*- Главная функция -*-
def main(fp, fl):
    obj_list = []
    
    if len(sys.argv) != 1:
        if os.stat(sys.argv[1]).st_size != 0:
            with open(fp) as input_file_programm:
                obj_list = scanner(input_file_programm)
        else:
            print("Input file is empty")
    else:
        print('Parametrs not found')
        
    for obj in obj_list:
        print(obj.getDescription())


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

