from lexical_analyzer.lexical import Lexical
import traceback
import sys
import os

class LexicalAnalizer:
  def __init__(self, file_name):
    try:
      file = open(file_name, 'r')
    except Exception:
      traceback.print_exc()
  
    self.lexical_analyzer = Lexical(file=file)
    
    while(self.lexical_analyzer.has_next_token()):
      token = self.lexical_analyzer.next_token()
      token.print_token()

def main():
  if(len(sys.argv) <= 1):
    print("No path directory was passed in arguments.")
    return

  # cwd = os.getcwd()  # Get the current working directory (cwd)
  # files = os.listdir(cwd)  # Get all the files in that directory
  # print("Files in %r: %s" % (cwd, files))

  for i in range(1, len(sys.argv)):
    file_name = sys.argv[i]
    LexicalAnalizer(file_name)
    
    if(i != len(sys.argv) - 1):
      print("\n\n")

main()