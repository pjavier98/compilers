# Compilers

## Repository for works on the subject of compilers

# To run the project:

```
cd project_pj
```

# Create Pipfile
```
pipenv --three
```

# Open Pipfile
```
pipenv shell
```

# Install package
```
pipenv install <package>
```

# Run Python Project

```
pipenv run python3 pj_compiler/lexical/main.py pj_compiler/examples/hello_world.pj

pipenv run python3 pj_compiler/lexical/main.py pj_compiler/examples/hello_world.pj > pj_compiler/output/hello_world.txt

pipenv run python3 pj_compiler/lexical/main.py pj_compiler/examples/fibonacci.pj

pipenv run python3 pj_compiler/lexical/main.py pj_compiler/examples/fibonacci.pj > pj_compiler/output/fibonacci.txt

pipenv run python3 pj_compiler/lexical/main.py pj_compiler/examples/shell_sort.pj

pipenv run python3 pj_compiler/lexical/main.py pj_compiler/examples/shell_sort.pj > pj_compiler/output/shell_sort.txt
```