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
    
    
# -*- Символ принадлежит к классу букв -*-
def isLetter(ch):
    if (ch >= 'A' and ch <= 'Z') or (ch >= 'a' and ch <= 'z'):
        return True
    else:
        return False


# -*- Лексический анализатор. Принимает входную цепочку (строку файла)-*-
def scanner(line):
    lexeme = None
    i = 0
    s_i = 0
    temp = ''
    while i < len(line): 
        if isLetter(line[i]):
            temp = temp + line[i]
            i += 1
        else:
            lexeme = Lexeme('1', 'id', 'type', temp)
            break
        
    return lexeme;
    
    

# -*- Главная функция -*-
def main(fp, fl):
    with open(fp) as input_file_programm:
    
        lexems = []
        for line in input_file_programm:
            lexems.append(scanner(line))
        
        for lex in lexems:      
            print(lex.description())


if __name__ == '__main__':
    if not len(sys.argv) == 1:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Parametrs not found')