import traceback

from lexical.analyzer.lexical import Lexical
from lexical.tokens.token import Token
from lexical.tokens.token_category import TokenCategory

class Syntatic:
  def __init__(self, file_name):

    try:
      file = open(file_name, 'r')
    except Exception:
      traceback.print_exc()

    self.epsilon = "ε"
    self.token = ''
    self.lexical_analyser = Lexical(file=file)
    self.get_next_token()
    self.run()
    
  def get_next_token(self):
    if (self.lexical_analyser.has_next_token()):
      self.token = self.lexical_analyser.next_token()
  
  def print_production(self, str1, str2):
    print("          {:s} = {:s}".format(str1, str2))

  def unexpected_token(self, expected):
    print("Error: Expected {:s} at [{:>04d}, {:>04d}] but got {:s}".format(expected, self.token.line, self.token.column, self.token.token_category))
    quit()

  def run(self):
    if (self.token.token_category == TokenCategory.typeInt.name):
      self.print_production("S", "'typeInt' sr")
      self.token.print_token()
      self.get_next_token()
      self.sr()

    elif (self.token.token_category in 
      [
        TokenCategory.typeFloat.name,
        TokenCategory.typeString.name,
        TokenCategory.typeChar.name,
        TokenCategory.typeBool.name
      ]
    ):
      self.print_production("S", "not_int_type decl S")
      self.not_int_type()
      self.get_next_token()
      self.decl()
      self.run()

    elif (self.token.token_category == TokenCategory.typeVoid.name):
      self.print_production("S", "'typeVoid' 'fnDecl' 'identifier' decl_func S")
      self.token.print_token()
      self.get_next_token()
      
      if (self.token.token_category == TokenCategory.fnDecl.name):
        self.token.print_token()
        self.get_next_token()
        
        if (self.token.token_category == TokenCategory.identifier.name):
          self.token.print_token()
          self.get_next_token()
          self.decl_func()
          self.run()
        else:
          self.unexpected_token("'identifier'")
      else:
        self.unexpected_token("'fnDecl'")
    else:
      self.print_production("S", self.epsilon)

  def sr(self):
    if (self.token.token_category == TokenCategory.fnDecl.name):
      self.print_production("sr", "'fnDecl' s_aux")
      self.token.print_token()
      self.get_next_token()
      self.s_aux()
    
    elif (self.token.token_category == TokenCategory.identifier.name):
      self.print_production("sr", "'identifier' decl_var S")
      self.token.print_token()
      self.get_next_token()
      self.decl_var()
      self.run()
    
    elif (self.token.token_category in 
      [
        TokenCategory.arrayBegin.name, 
        TokenCategory.fnDecl.name
      ]
    ):
      self.print_production("sr", "type_arr_opc 'fnDecl' 'identifier' decl_func S")
      self.type_arr_opc()

      if (self.token.token_category == TokenCategory.fnDecl.name):
        self.token.print_token()
        self.get_next_token()
      
        if (self.token.token_category == TokenCategory.identifier.name):
          self.token.print_token()
          self.get_next_token()
          self.decl_func()
          self.get_next_token()
          self.run()
        else:
          self.unexpected_token("'identifier'")
    else:
      self.unexpected_token("'fnDecl' or '[' or 'identifier'")
  
  def s_aux(self):
    if (self.token.token_category == TokenCategory.main.name):
      self.print_production("s_aux", "'main' main")
      self.token.print_token()
      self.get_next_token()
      self.main()

    elif (self.token.token_category == TokenCategory.identifier.name):
      self.print_production("s_aux", "'identifier' decl_func S")
      self.token.print_token()
      self.get_next_token()
      self.decl_func()
      self.run()

  def main(self):
    if (self.token.token_category == TokenCategory.paramBegin.name):
      self.print_production("main", " '(' ')' body")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.paramEnd.name):
        self.token.print_token()
        self.get_next_token()
        self.body()
      else:
        self.unexpected_token("')'")
    else:
      self.unexpected_token("'('")
  
  def body(self):
    self.print_production("body", "'{' content '}'")
    self.token.print_token()
    self.get_next_token()
    self.content()

    if (self.token.token_category == TokenCategory.scopeEnd.name):
      self.token.print_token()
    else:
      self.unexpected_token("'}'")

  def content(self):
    if (self.token.token_category in 
      [
        TokenCategory.cmdIf.name, 
        TokenCategory.cmdWhile.name, 
        TokenCategory.cmdFor.name, 
        TokenCategory.fnRead.name, 
        TokenCategory.fnWrite.name
      ]
    ):
      self.print_production("content", "command content")
      self.command()
      self.content()

    elif (self.token.token_category == TokenCategory.identifier.name):
      self.print_production("content", "'identifier' content_x")
      self.token.print_token()
      self.get_next_token()
      self.content_x()  

    elif (self.token.token_category == TokenCategory.fnRtn.name):
      self.print_production("content", "'fnRtn' rtn ';'")
      self.token.print_token()
      self.get_next_token()
      self.rtn()
      if (self.token.token_category != TokenCategory.semicolon.name):
        self.unexpected_token(';')
      else:
        self.token.print_token()
        self.get_next_token()

    elif (self.token.token_category in 
      [
        TokenCategory.typeInt.name, 
        TokenCategory.typeFloat.name,
        TokenCategory.typeChar.name, 
        TokenCategory.typeString.name, 
        TokenCategory.typeBool.name
      ]
    ):
      self.print_production("content", "var_type 'identifier' decl_var content")
      self.var_type()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.identifier.name):
        self.token.print_token()
        self.get_next_token()
        self.decl_var()
        self.content()
      else:
        self.unexpected_token("'identifier'")
    else:
      self.print_production("content", self.epsilon)

  def content_x(self):
    if (self.token.token_category == TokenCategory.paramBegin.name):
      self.print_production("content_x", "'(' params_call ')' ';' content")
      self.token.print_token()
      self.get_next_token()
      self.params_call()

      if (self.token.token_category == TokenCategory.paramEnd.name):
        self.token.print_token()
        self.get_next_token()

        if (self.token.token_category == TokenCategory.semicolon.name):
          self.token.print_token()
          self.get_next_token()
          self.content()
        else:
          self.unexpected_token("';'")
      else:
        self.unexpected_token("')'")
    else:
      self.print_production("content_x", "l_attr ';' content")
      self.l_attr()
      if (self.token.token_category == TokenCategory.semicolon.name):
        self.token.print_token()
        self.get_next_token()
        self.content()
      else:
        self.unexpected_token("';'")

  def command(self):
    if (self.token.token_category == TokenCategory.cmdIf.name):
      self.print_production("command", "'cmdIf' '(' eb ')' body l_elsif cmd_else")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.paramBegin.name):
        self.token.print_token()
        self.get_next_token()
        self.eb()

        if (self.token.token_category == TokenCategory.paramEnd.name):
          self.token.print_token()
          self.get_next_token()

          if (self.token.token_category == TokenCategory.scopeBegin.name):
            self.body()

            if (self.token.token_category == TokenCategory.scopeEnd.name):
              self.get_next_token()
              self.l_elsif()
              self.cmd_else()
            else:
              self.unexpected_token("'}'")
          else:
            self.unexpected_token("'{'")
        else:
          self.unexpected_token("')'")
      else:
        self.unexpected_token("'('")

    elif (self.token.token_category == TokenCategory.cmdWhile.name):
      self.print_production("command", "'cmdWhile' '(' eb ')' body")
      self.token.print_token()
      self.get_next_token()
      
      if (self.token.token_category == TokenCategory.paramBegin.name):
        self.token.print_token()
        self.get_next_token()
        self.eb()

        if (self.token.token_category == TokenCategory.paramEnd.name):
          self.token.print_token()
          self.get_next_token()
          
          if (self.token.token_category == TokenCategory.scopeBegin.name):
            self.body()

            if (self.token.token_category != TokenCategory.scopeEnd.name):                      
              self.unexpected_token("'}'")
            else:
              self.get_next_token()
          else:
            self.unexpected_token("'{'")
        else:
          self.unexpected_token("')'")
      else:
        self.unexpected_token("'('")
    
    elif (self.token.token_category == TokenCategory.cmdFor.name):
      self.print_production("command", "'cmdFor' 'identifier' 'in' '(' ea ',' ea ',' ea ')' body")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.identifier.name):
        self.token.print_token()
        self.get_next_token()  

        if (self.token.token_category == TokenCategory.identifier.name):
          self.token.print_token()
          self.get_next_token() 

          if (self.token.token_category == TokenCategory.paramBegin.name):
            self.token.print_token()
            self.get_next_token() 
            self.ea()

            if (self.token.token_category == TokenCategory.commaSep.name):
              self.token.print_token()
              self.get_next_token()
              self.ea()

              if (self.token.token_category == TokenCategory.commaSep.name):
                self.token.print_token()
                self.get_next_token()
                self.ea()

                if (self.token.token_category == TokenCategory.paramEnd.name):
                  self.token.print_token()
                  self.get_next_token()
                  self.body()
                else:
                  self.unexpected_token("')'")
              else:
                self.unexpected_token("','")
            else:
              self.unexpected_token("','")
          else:
            self.unexpected_token("'('")
        else:
          self.unexpected_token("'in'")
      else:
        self.unexpected_token("'identifier'")
    
    elif (self.token.token_category == TokenCategory.fnRead.name):
      self.print_production("command", "'fnRead' '(' LIdentfier ')' ';'")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.paramBegin.name):
        self.token.print_token()
        self.get_next_token()
        self.l_identifier()
        if (self.token.token_category == TokenCategory.paramEnd.name):
          self.token.print_token()
          self.get_next_token()
          if (self.token.token_category == TokenCategory.semicolon.name):
            self.token.print_token()
            self.get_next_token()
          else: 
            self.unexpected_token("';'")
        else:
          self.unexpected_token("')'") 
      else: 
        self.unexpected_token("'('")

    elif (self.token.token_category == TokenCategory.fnWrite.name):
      self.print_production("command", "'fnWrite' '(' 'stringVal' print_params ')' ';'")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.paramBegin.name):
        self.token.print_token()
        self.get_next_token()

        if (self.token.token_category == TokenCategory.stringVal.name):
          self.token.print_token()
          self.get_next_token()
          self.print_params()

          if (self.token.token_category == TokenCategory.paramEnd.name):
            self.token.print_token()
            self.get_next_token()

            if (self.token.token_category == TokenCategory.semicolon.name):
              self.token.print_token()
              self.get_next_token()
            else: 
              self.unexpected_token("';'")
          else:
            self.unexpected_token("',' or ')'")
        else:
          self.unexpected_token("'stringVal'")
      else: 
        self.unexpected_token("')'")

  def l_elsif(self):
    if (self.token.token_category == TokenCategory.cmdElsif.name):
      self.print_production("l_elsif", "'cmdElsif' '(' eb ')' body l_elsif")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.paramBegin.name):
        self.token.print_token()
        self.get_next_token()
        self.eb()
        
        if (self.token.token_category == TokenCategory.paramEnd.name):
          self.token.print_token()
          self.get_next_token()

          if (self.token.token_category == TokenCategory.scopeBegin.name):
            self.body()

            if (self.token.token_category == TokenCategory.scopeEnd.name):
              self.get_next_token()
              self.l_elsif()
            else:
              self.unexpected_token("'}'")
          else:
            self.unexpected_token("'{'")
        else:
          self.unexpected_token("')'")
      else:
        self.unexpected_token("'('")
    else:
      self.print_production("l_elsif", self.epsilon)

  def cmd_else(self):
    if (self.token.token_category == TokenCategory.cmdElse.name):
      self.print_production("cmd_else", "'cmdElse' body")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.scopeBegin.name):
        self.body()

        if (self.token.token_category == TokenCategory.scopeEnd.name):
          self.get_next_token()
        else:
          self.unexpected_token("'}'")
      else:
        self.unexpected_token("'{'")

  def l_identifier(self):
    if (self.token.token_category == TokenCategory.identifier.name):
      self.print_production("l_identifier", "'identifier' l_identifier_x")
      self.token.print_token()
      self.get_next_token()
      self.l_identifier_x()
    else:
      self.print_production("l_identifier", self.epsilon)

  def l_identifier_x(self):
    if (self.token.token_category == TokenCategory.commaSep.name):
      self.print_production("l_identifier_x", "',' 'identifier' l_identifier_x")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.identifier.name):
        self.token.print_token()
        self.get_next_token()
        self.l_identifier_x()
      else:
        self.unexpected_token('identifier')

    elif (self.token.token_category == TokenCategory.paramEnd.name):
      self.print_production("l_identifier_x", self.epsilon)
    else:
      self.unexpected_token("paramEnd")

  def print_params(self):
    if (self.token.token_category == TokenCategory.commaSep.name):
      self.print_production("print_params", "',' eb print_params")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.paramEnd.name):
        self.unexpected_token('identifier')
      
      self.eb()
      self.print_params()

    elif (self.token.token_category == TokenCategory.paramEnd.name):
      self.print_production("print_params", self.epsilon)
    else:
      self.unexpected_token('paramEnd')

  def var_type(self):
    if (self.token.token_category == TokenCategory.typeInt.name):
      self.print_production("var_type", "'typeInt'")
      self.token.print_token()

    elif (self.token.token_category == TokenCategory.typeFloat.name):
      self.print_production("var_type", "'typeFloat'")
      self.token.print_token()

    elif (self.token.token_category == TokenCategory.typeString.name):
      self.print_production("var_type", "'typeString'")
      self.token.print_token()

    elif (self.token.token_category == TokenCategory.typeChar.name):
      self.print_production("var_type", "'typeChar'")
      self.token.print_token()

    elif (self.token.token_category == TokenCategory.typeBool.name):
      self.print_production("var_type", "'typeBool'")
      self.token.print_token()

  def decl_var(self):
    self.print_production("decl_var", "l_var ';'")
    self.l_var()

    if (self.token.token_category == TokenCategory.semicolon.name):
      self.token.print_token()
      self.get_next_token()
    else:
      self.unexpected_token("';'")
  
  def l_var(self):
    if (self.token.token_category == TokenCategory.semicolon.name):
      self.print_production("l_var", self.epsilon)

    elif (self.token.token_category in 
      [
        TokenCategory.opAttr.name, 
        TokenCategory.arrayBegin.name, 
        TokenCategory.commaSep.name
      ]
    ):
      self.print_production("l_var", "var_x l_var_x")
      self.var_x()
      self.l_var_x()

      if (self.token.token_category == TokenCategory.opAttr.name):
        self.token.print_token()
        self.get_next_token()

  def l_var_x(self):
    if (self.token.token_category == TokenCategory.commaSep.name):
      self.print_production("l_var_x", "',' var l_var_x")
      self.token.print_token()
      self.get_next_token()
      self.var()
      self.l_var_x()
    else:
      self.print_production("l_var_x", self.epsilon)
  
  def var(self):
    if (self.token.token_category == TokenCategory.identifier.name):
      self.print_production("var", "'identifier' var_x")
      self.token.print_token()
      self.get_next_token()
      self.var_x()
    else:
      self.unexpected_token("'identifier'")

  def var_x(self):
    if (self.token.token_category == TokenCategory.opAttr.name):
      self.print_production("var_x", "'=' ec")
      self.token.print_token()
      self.get_next_token()
      self.ec()
    else:
      self.print_production("var_x", "arr_opc")
      self.arr_opc()

  def params_call(self):
    if (self.token.token_category == TokenCategory.paramEnd.name):
      self.print_production("params_call", self.epsilon)
    else:
      self.print_production("params_call", "ec params_call_x")
      self.token.print_token()
      self.get_next_token()
      self.ec()
      self.params_call_x()
    
  def params_call_x(self):
    if (self.token.token_category == TokenCategory.commaSep.name):
      self.print_production("params_call_x", "',' ec params_call_x")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.paramEnd.name):
        self.unexpected_token("'identifier', 'intVal', 'floatVal', 'stringVal', 'charVal', 'boolVal'")
      
      self.ec()
      self.params_call_x()
    
    elif (self.token.token_category == TokenCategory.paramEnd.name):
      self.print_production("params_call_x", self.epsilon)
    else:
      self.unexpected_token("')'")

  def l_attr(self):
    if (self.token.token_category in 
      [
        TokenCategory.opAttr.name, 
        TokenCategory.arrayBegin.name
      ]
    ):
      if (self.token.token_category == TokenCategory.opAttr.name):
        self.print_production("l_attr_x", "'=' ec l_attr_x")
        self.token.print_token()
        self.get_next_token()
        self.ec()
        self.l_attr_x()
      else:
        self.print_production("l_attr_x", "[' ea ']' '=' ec l_attr_x")
        self.token.print_token()
        self.get_next_token()
        self.ea()

        if (self.token.token_category == TokenCategory.arrayEnd.name):
          self.token.print_token()
          self.get_next_token()

          if (self.token.token_category == TokenCategory.opAttr.name):
            self.token.print_token()
            self.get_next_token()
            self.ec()
            self.l_attr_x()
          else:
            self.unexpected_token("'='")
        else:
          self.unexpected_token("']'")
    else:
      self.unexpected_token("'=' or '['")

  def l_attr_x(self):
    if (self.token.token_category == TokenCategory.commaSep.name):
      self.print_production("l_attr_x", "',' l_attr_x_x")
      self.token.print_token()
      self.get_next_token()
      self.l_attr_x_x()
    else:
      self.print_production("l_attr_x", self.epsilon)

  def l_attr_x_x(self):
    if (self.token.token_category in 
      [
        TokenCategory.identifier.name, 
        TokenCategory.arrayBegin.name
      ]
    ):
      if (self.token.token_category == TokenCategory.identifier.name):
        self.print_production("l_attr_x_x", "'identifier' '=' ec l_attr_x")
        self.token.print_token()
        self.get_next_token()

        if (self.token.token_category == TokenCategory.opAttr.name):
          self.token.print_token()
          self.get_next_token()
          self.ec()
          self.l_attr_x()
        else:
          self.unexpected_token("'='")
      else:
        self.print_production("l_attr_x_x", "'[' ea ']' '=' ec l_attr_x")
        self.token.print_token()
        self.get_next_token()

        if (self.token.token_category == TokenCategory.arrayBegin.name):
          self.token.print_token()
          self.get_next_token()
          self.ea()

          if (self.token.token_category == TokenCategory.arrayEnd.name):
            self.token.print_token()
            self.get_next_token()

            if (self.token.token_category == TokenCategory.opAttr.name):
              self.token.print_token()
              self.get_next_token()
              self.ec()
              self.l_attr_x()
            else:
              self.unexpected_token("'='")
          else:
            self.unexpected_token("']'")
        else:
          self.unexpected_token("'['")
    else:
      self.unexpected_token("'identifier' or '['")

  def rtn(self):
    if (self.token.token_category == TokenCategory.semicolon.name):
       self.print_production("rtn", self.epsilon)
    else:
      self.print_production("rtn", "ec")
      self.ec()

  def decl_func(self):
    self.print_production("decl_func", " '(' params ')' body")
    
    if (self.token.token_category == TokenCategory.paramBegin.name):
      self.token.print_token()
      self.get_next_token()  
      self.params()
      self.get_next_token()

      if (self.token.token_category == TokenCategory.scopeBegin.name):
        self.body()
      else:
        self.unexpected_token("'{'")
    else:
      self.unexpected_token("'('")

  def params(self):
    if (self.token.token_category in 
      [
        TokenCategory.typeInt.name,
        TokenCategory.typeFloat.name,
        TokenCategory.typeString.name,
        TokenCategory.typeChar.name,
        TokenCategory.typeBool.name
      ]
    ):
      self.print_production("params", "var_type 'identifier' arr_opc params_x")
      self.var_type()
      self.get_next_token()

      if (self.token.token_category != TokenCategory.identifier.name):
        self.unexpected_token("'identifier'")
      else:
        self.token.print_token()
        self.get_next_token()
        self.arr_opc_params()
        self.params_x()
    else:
      self.print_production("params", self.epsilon)
      self.token.print_token()

  def params_x(self):
    if (self.token.token_category == TokenCategory.commaSep.name):
      self.print_production("params_x", "',' var_type 'identifier' arr_opc params_x")
      self.get_next_token()

      if (self.token.token_category in 
        [
          TokenCategory.typeInt.name,
          TokenCategory.typeFloat.name,
          TokenCategory.typeChar.name,
          TokenCategory.typeString.name, 
          TokenCategory.typeBool.name
        ]
      ):
        self.var_type()
        self.get_next_token()

        if (self.token.token_category == TokenCategory.identifier.name):
          self.token.print_token()
          self.get_next_token()
          self.arr_opc_params()
          self.params_x()
        else:
          self.unexpected_token("'identifier'")
      else:
        self.unexpected_token("'typeInt', 'typeFloat', 'typeChar', 'typeString' or 'typeBool'")
    
    elif (self.token.token_category == TokenCategory.paramEnd.name):
      self.print_production("params_x", self.epsilon)
    else:
      self.unexpected_token("')'")

  def arr_opc(self):
    if (self.token.token_category != TokenCategory.arrayBegin.name):
       self.print_production("arr_opc", self.epsilon)
       self.token.print_token()
    else:
      self.print_production("arr_opc", "'[' arr_size_obg ']'")
      self.token.print_token()
      self.get_next_token()
      self.arr_size_obg()
      self.get_next_token()

      if (self.token.token_category != TokenCategory.arrayEnd.name):
        self.unexpected_token("']'")
      
      self.token.print_token()
      self.get_next_token()

  def arr_opc_params(self):
    if (self.token.token_category != TokenCategory.arrayBegin.name):
       self.print_production("arr_opc", self.epsilon)
       self.token.print_token()
    else:
      self.print_production("arr_opc", "'['']'")
      self.token.print_token()
      self.get_next_token()
      
      if (self.token.token_category != TokenCategory.arrayEnd.name):
        self.unexpected_token("']'")
      
      self.token.print_token()
      self.get_next_token()
          
  def arr_size_obg(self):
    if (self.token.token_category == TokenCategory.identifier.name):
      self.print_production("arr_size_obg", "'identifier'")
      self.token.print_token()
    elif (self.token.token_category == TokenCategory.intVal.name):
      self.print_production("arr_size_obg", "'intVal'")
      self.token.print_token()
    else:
      self.unexpected_token("'identifier', 'intVal'")

  def type_arr_opc(self):
    if (self.token.token_category == TokenCategory.arrayBegin.name):
      self.print_production("type_arr_opc", "'[' ']'")
      self.token.print_token()
      self.get_next_token()

      if (self.token.token_category != TokenCategory.arrayEnd.name):
        self.unexpected_token("']'")
      else:
        self.token.print_token()
        self.get_next_token()
    else:
      self.print_production("type_arr_opc", self.epsilon)

  def not_int_type(self):
    if (self.token.token_category == TokenCategory.typeFloat.name):
      self.print_production("not_int_type", "'typeFloat'")
      self.token.print_token()
    elif (self.token.token_category == TokenCategory.typeString.name):
      self.print_production("not_int_type", "'typeString'")
      self.token.print_token()
    elif (self.token.token_category == TokenCategory.typeChar.name):
      self.print_production("not_int_type", "'typeChar'")
      self.token.print_token()
    elif (self.token.token_category == TokenCategory.typeBool.name):
      self.print_production("not_int_type", "'typeBool'")
      self.token.print_token()
      
  def decl(self):
    self.type_arr_opc()
    self.decl_x()

  def decl_x(self):
    if (self.token.token_category in 
      [
        TokenCategory.fnDecl.name, 
        TokenCategory.identifier.name
      ]
    ):
      if (self.token.token_category == TokenCategory.fnDecl.name):
        self.print_production("decl_x", "'fnDecl' 'identifier' decl_func")
        self.token.print_token()
        self.get_next_token()

        if (self.token.token_category == TokenCategory.identifier.name):
          self.token.print_token()
          self.get_next_token()
          self.decl_func()
        else:
          self.unexpected_token("'identifier'")
          
      elif (self.token.token_category == TokenCategory.identifier.name):
        self.print_production("decl_x", "'identifier' decl_var")
        self.token.print_token()
        self.get_next_token()
        self.decl_var()      
    else:
      self.unexpected_token("'identifier' or 'fnDecl'")

  def ec(self):
    self.print_production("ec", "eb ec_x")
    self.eb()
    self.ec_x()
  
  def ec_x(self):
    if (self.token.token_category == TokenCategory.opConcat.name):
      self.print_production("ec_x", "'opConcat' eb ec_x")
      self.token.print_token()
      self.get_next_token()
      self.eb()
      self.ec_x()
    else:
      self.print_production("ec_x", self.epsilon)

  def eb(self):
    self.print_production("eb", "tb eb_x")
    self.tb()
    self.eb_x()

  def eb_x(self):
    if (self.token.token_category == TokenCategory.opOr.name):
      self.print_production("eb_x", "'opOr' tb eb_x")
      self.token.print_token()
      self.get_next_token()
      self.tb()
      self.eb_x()
    else:
      self.print_production("eb_x", self.epsilon)
  
  def tb(self):
    self.print_production("tb", "fb tb_x")
    self.fb()
    self.tb_x()

  def tb_x(self):
    if (self.token.token_category == TokenCategory.opAnd.name):
      self.print_production("tb_x", "'opAnd' fb tb_x")
      self.token.print_token()
      self.get_next_token()
      self.fb()
      self.tb_x()
    else:
      self.print_production("tb_x", self.epsilon)

  def fb(self):
    if (self.token.token_category == TokenCategory.opNot.name):
      self.print_production("fb", "'opNot' fb")
      self.token.print_token()
      self.get_next_token()
      self.fb()
    else:
      self.print_production("fb", "ra fb_x")
      self.ra()
      self.fb_x()

  def fb_x(self):
    if (self.token.token_category in 
      [
        TokenCategory.opGtrThan.name,
        TokenCategory.opLessThan.name,
        TokenCategory.opGtrEqual.name,
        TokenCategory.opLessEq.name
      ]
    ):
      if (self.token.token_category == TokenCategory.opGtrThan.name):
        self.print_production("fb_x", "'opGtrThan' ra fb_x")
      elif (self.token.token_category == TokenCategory.opLessThan.name):
        self.print_production("fb_x", "'opLessThan' ra fb_x")
      elif (self.token.token_category == TokenCategory.opGtrEqual.name):
        self.print_production("fb_x", "'opGtrEqual' ra fb_x")
      elif (self.token.token_category == TokenCategory.opLessEq.name):
        self.print_production("fb_x", "'opLessEq' ra fb_x")  
      
      self.token.print_token()
      self.get_next_token()
      self.fb()
      self.fb_x()
    else:
      self.print_production("fb_x", self.epsilon)

  def ra(self):
    self.print_production("ra", "ea ra_x")
    self.ea()
    self.ra_x()

  def ra_x(self):
    if (self.token.token_category in 
      [
        TokenCategory.opEqual.name, 
        TokenCategory.opNotEqual.name
      ]
    ):
      if (self.token.token_category == TokenCategory.opEqual):
        self.print_production("ra_x", "'opEqual' ea ra_x")
      elif (self.token.token_category == TokenCategory.opNotEqual):
        self.print_production("ra_x", "'opNotEqual' ea ra_x")
      
      self.token.print_token()
      self.get_next_token()
      self.ea()
      self.ra_x()
    else:
      self.print_production("ra_x", self.epsilon)

  def ea(self):
    self.print_production("ea", "ta ea_x")
    self.ta()
    self.ea_x()

  def ea_x(self):
    if (self.token.token_category in 
      [
        TokenCategory.opAdd.name,
        TokenCategory.opSub.name
      ]
    ):
      if (self.token.token_category == TokenCategory.opAdd):
        self.print_production("ea_x", "'opAdd' fa ea_x")
      elif (self.token.token_category == TokenCategory.opSub):
        self.print_production("ea_x", "'opSub' fa ea_x")
      
      self.token.print_token()
      self.get_next_token()
      self.fa()
      self.ea_x()
    else:
      self.print_production("ea_x", self.epsilon)
  
  def ta(self):
    self.print_production("ta", "fa ta_x")
    self.fa()
    self.ta_x()

  def ta_x(self):
    if (self.token.token_category in 
      [
        TokenCategory.opMult.name,
        TokenCategory.opDiv.name,
        TokenCategory.opMod.name
      ]
    ):
      if (self.token.token_category == TokenCategory.opMult):
        self.print_production("ta_x", "'opMult' fa ta_x")
      elif (self.token.token_category == TokenCategory.opDiv):
        self.print_production("ta_x", "'opDiv' fa ta_x")
      elif (self.token.token_category == TokenCategory.opMod):
        self.print_production("ta_x", "'opMod' fa ta_x")
      
      self.token.print_token()
      self.get_next_token()
      self.fa()
      self.ta_x()
    else:
      self.print_production("ta_x", self.epsilon)

  def fa(self):
    if (self.token.token_category == TokenCategory.paramBegin.name):
      self.print_production("fa", "'(' ec ')'")
      self.token.print_token()
      self.get_next_token()
      self.ec()
      self.get_next_token()
      
      if (self.token.token_category == TokenCategory.paramEnd):
        self.token.print_token()
      else:
        self.token.print_token()
        self.unexpected_token(")")
    elif (self.token.token_category == TokenCategory.opUnaryNeg.name):
      self.print_production("fa", "'opUnaryNeg' fa ")
      self.token.print_token()
      self.get_next_token()
      if (self.token.token_category == TokenCategory.opUnaryNeg.name):
        self.token.print_token()
        self.unexpected_token("'(', var_or_func, 'intVal', 'floatVal', 'stringVal', 'charVal', 'boolVal'")
      self.fa()
    elif (self.token.token_category == TokenCategory.identifier.name):
      self.print_production("fa", "var_or_func")
      self.var_or_func()
    elif (self.token.token_category == TokenCategory.intVal.name):
      self.print_production("fa", "'intVal'")
      self.token.print_token()
      self.get_next_token()
    elif (self.token.token_category == TokenCategory.floatVal.name):
      self.print_production("fa", "'floatVal'")
      self.token.print_token()
      self.get_next_token()
    elif (self.token.token_category == TokenCategory.stringVal.name):
      self.print_production("fa", "'stringVal'")
      self.token.print_token()
      self.get_next_token()
    elif (self.token.token_category == TokenCategory.charVal.name):
      self.print_production("fa", "'charVal'")
      self.token.print_token()
      self.get_next_token()
    elif (self.token.token_category == TokenCategory.boolVal.name):
      self.print_production("fa", "'boolVal'")
      self.token.print_token()
      self.get_next_token()

  def var_or_func(self):
    self.print_production("var_or_func", "'identifier' var_or_func_x")
    self.token.print_token()
    self.get_next_token()
    self.var_or_func_x()

  def var_or_func_x(self):
    if (self.token.token_category == TokenCategory.arrayBegin.name):
      self.print_production("var_or_func_x","'[' ea ']'")
      self.token.print_token()
      self.get_next_token()
      self.ea()
      
      if (self.token.token_category == TokenCategory.arrayEnd.name):
        self.token.print_token()
        self.get_next_token()
      else:
        self.unexpected_token("']'")
    elif (self.token.token_category == TokenCategory.paramBegin.name):
      self.print_production("VarOfFuncx", "'(' params_call ')'")
      self.token.print_token()
      self.get_next_token()
      self.params_call()

      if (self.token.token_category == TokenCategory.paramEnd.name):
        self.token.print_token()
        self.get_next_token()
      else:
        self.unexpected_token("')'")
    else:
      self.print_production("var_or_func_x", self.epsilon)