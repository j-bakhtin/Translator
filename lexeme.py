'''
Created on 4 Feb. 2019 y.

@author: Jurij Bakhtin
'''
from builtins import str
import sys


# -*- �����, ����������� ������� � ������� <������>lex:<�������>[<���>:<������������_��������>][val:<��������>] -*-
class Lexeme:
    def __init__(self, lineNumber, lexeme, recognizedValue, value):
        self.lineNumber = lineNumber
        self.lexeme = lexeme
        self.type = type
        self.recognizedValue = recognizedValue
        self.value = value
    
    # -*- ������ �������� ������� -*-
    def description(self):
        pass

# -*- ����������� ����������. ��������� ����� -*-
def scanner(keyword):
    pass


# -*- ������� ������� -*-
def main(fp, fl):
    input_file_programm = open(fp, 'r')
    #output_file_lexems = open(fl, 'r')
    
    print(input_file_programm.read())
    #file_lexems.read()


if __name__ == '__main__':
    if not len(sys.argv) == 1:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Parametrs not found')