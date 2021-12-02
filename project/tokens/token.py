class Token():

  def __init__(self, lexeme, line, column, token_id, token_category):
    self.lexeme = lexeme
    self.line = line
    self.column = column
    self.token_id = token_id
    self.token_category = token_category