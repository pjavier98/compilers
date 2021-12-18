class Token():

  def __init__(self, lexeme, line, column, token_id, token_category):
    self.lexeme = lexeme
    self.line = line
    self.column = column
    self.token_id = token_id
    self.token_category = token_category

  def print_token(self):
    print("          [{:>04d}, {:>04d}] ({:>04d}, {:>20s}) {{{}}}".format(self.line, self.column, self.token_id, self.token_category, self.lexeme))
