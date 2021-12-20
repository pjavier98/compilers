import re
from lexical_analyzer.lexeme_table import LexemeTable
from lexical_analyzer.separators import Separators
from tokens.token import Token
from tokens.token_category import TokenCategory

class Lexical():
  def __init__(self, file):
    self.last_token = ""
    self.current_token = ""
    self.line_count = 0
    self.current_column = 0
    self.current_line = ""
    self.file = file
    self.separators = Separators().separators
    self.lexeme_table = LexemeTable().dict
    self.EOF = False

  def increment_line_count(self):
    self.line_count += 1

  def increment_column(self):
    self.current_column += 1

  def get_current_char(self):
    return str(self.current_line[self.current_column])
  
  def print_line(self):
    # Case of empty file
    if (len(self.current_line) == 0):
      return

    current_line_index = len(self.current_line) - 1
    if(self.current_line[current_line_index] == "\n"):
      print("{:>4d}  {}".format(self.line_count, self.current_line), end="")
    else:
      print("{:>4d}  {}".format(self.line_count, self.current_line))

  def is_number(self, lexeme):
    return re.match('[0-9]', lexeme)
  
  def is_float_number(self, lexeme):
    return self.get_current_char() == '.' and self.is_number(lexeme)
  
  def is_string(self, lexeme):
    return lexeme == '"' or lexeme == '\''

  def is_int_number_type(self, lexeme):
    return re.match('[0-9]*$', lexeme)

  def is_char_type(self, lexeme):
    starts_with_single_quote = lexeme[0] == '\''
    ends_with_single_quote = lexeme[-1] == '\''
    is_length_equal_to_three = len(lexeme) == 3

    return starts_with_single_quote and ends_with_single_quote and is_length_equal_to_three

  def is_string_type(self, lexeme):
    start_with_double_quotes = lexeme[0] == '"'
    ends_with_double_quotes = lexeme[-1] == '"'

    return start_with_double_quotes and ends_with_double_quotes

  def is_identifier(self, lexeme):
    return re.match("[a-zA-Z]([A-Za-z0-9\_]*)", lexeme)

  def is_float_number_type(self, lexeme):
    return re.match('^[0-9]+\.[0-9]+', lexeme)

  def is_simple_or_double_quotes(self, lexeme):
    is_single_quotes = (self.get_current_char() == '\'' and lexeme[0] == '\'')
    is_double_quotes = self.get_current_char() == '"' and lexeme[0] == '"'

    return (is_single_quotes or is_double_quotes)

  def is_white_space_or_end_of_line(self, column_index):
    is_white_space = self.current_line[column_index] == ' '
    is_end_of_line = self.current_line[column_index] == '\n'

    return (is_white_space or is_end_of_line)

  def not_end_of_line(self):
    column_index = self.current_column
    line_size = len(self.current_line)

    return column_index < line_size

  def is_between_bounds(self):
    return self.current_column < self.line_count

  def next_token(self):
    if (self.EOF == True):
      self.line_count += 1
      self.current_line = "EOF"
      self.print_line()
      return Token(TokenCategory.EOF.name, self.line_count, 1, TokenCategory["EOF"].value, "")

    while (self.not_end_of_line() and self.is_white_space_or_end_of_line(self.current_column)):
      self.increment_column()

    lexeme = self.get_current_char()
    
    # Case of number
    if (self.is_number(lexeme)):
      self.increment_column()
      
      while (self.not_end_of_line()):
        if (self.is_number(self.get_current_char())):
          lexeme += self.get_current_char()
          self.increment_column()
          continue

        # Case of float
        if (self.get_current_char() != '.'):
          if (self.is_float_number_type(lexeme)):
            return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["floatVal"].value, TokenCategory.floatVal.name)
          # Case of int
          elif (self.is_int_number_type(lexeme)):
            return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["intVal"].value, TokenCategory.intVal.name)
          # if it is none of the above, it is not identified
          else:
            return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["tokenNotDefined"].value, TokenCategory.tokenNotDefined.name)

        # Read until last caracter of the float number
        if (self.is_float_number(lexeme)):
          lexeme += self.get_current_char()
          self.increment_column()
      
      if (self.is_float_number_type(lexeme)):
        return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["floatVal"].value, TokenCategory.floatVal.name)
      # Case of int
      elif (self.is_int_number_type(lexeme)):
        return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["intVal"].value, TokenCategory.intVal.name)
      # if it is none of the above, it is not identified
      else:
        return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["tokenNotDefined"].value, TokenCategory.tokenNotDefined.name)
    
    # Other cases
    while (self.not_end_of_line()):
      if (self.get_current_char() in self.separators):
        # Case of string
        if (self.is_string(lexeme)):
          self.increment_column()
          
          while (self.not_end_of_line()):
            if (self.get_current_char() != '\n'):
              lexeme += self.get_current_char()
            
            if (self.is_simple_or_double_quotes(lexeme)):
              self.increment_column()
              break
            self.increment_column()
          
          if (self.is_string_type(lexeme)):
            return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["stringVal"].value, TokenCategory.stringVal.name)
          
          elif (self.is_char_type(lexeme)):
            return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["charVal"].value, TokenCategory.charVal.name)

        # Case of union of two separators
        elif (lexeme == self.get_current_char()):
          self.increment_column()
          
          if (self.not_end_of_line()):
            two_separators_token = lexeme + self.get_current_char()
            
            if (two_separators_token in self.lexeme_table):
              lexeme = two_separators_token
              self.increment_column()
    
          if (lexeme in self.lexeme_table):
            return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory[self.lexeme_table.get(lexeme)].value, self.lexeme_table.get(lexeme))
          else:
            return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["tokenNotDefined"].value, TokenCategory.tokenNotDefined.name)

        else:
          # Verify if it is a reserved word
          if (lexeme in self.lexeme_table):
            return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory[self.lexeme_table.get(lexeme)].value, self.lexeme_table.get(lexeme))
          else:
            # Verify if it is a identifier
            if (self.is_identifier(lexeme)):
              return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["identifier"].value, TokenCategory.identifier.name)

        # If it is none of the above, it is not defined
        return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["tokenNotDefined"].value, TokenCategory.tokenNotDefined.name)
      
      self.increment_column()

      # Identifier or Number
      if (self.current_column == len(self.current_line) and self.is_identifier(lexeme)):
        return Token(lexeme, self.line_count, self.current_column - len(lexeme) + 1, TokenCategory["identifier"].value, TokenCategory.identifier.name)
        
      if (not(self.get_current_char() in self.separators)):
        lexeme += self.get_current_char()

  def has_next_line(self):
    line = self.file.readline()

    if (not line):
      return False
    
    self.increment_line_count()
    self.current_line = line
    self.current_column = 0

    return True

  def has_next_token(self):
    if(self.line_count == 0 and self.current_column == 0):
      if(self.has_next_line()):
        self.print_line()
      else:
        self.print_line()
        return False
        
    if(re.match('[\s]*$', self.current_line[self.current_column:])):
      while(self.has_next_line()):
        self.print_line()
        if(not re.match('[\s]*$', self.current_line)):
          return True
      
      if(self.EOF == False):
        self.EOF = True
        return True

      return False

    if(self.EOF == True):
      return False
      
    return True