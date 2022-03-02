# Compilers

## Repository for works on the subject of compilers

# To run the project

```
cd compilers
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
pipenv run python3 pj_compiler/main.py pj_compiler/examples/hello_world.pj

pipenv run python3 pj_compiler/main.py pj_compiler/examples/hello_world.pj > pj_compiler/output/syntactic/hello_world.txt

pipenv run python3 pj_compiler/main.py pj_compiler/examples/fibonacci.pj

pipenv run python3 pj_compiler/main.py pj_compiler/examples/fibonacci.pj > pj_compiler/output/syntactic/fibonacci.txt

pipenv run python3 pj_compiler/main.py pj_compiler/examples/shell_sort.pj

pipenv run python3 pj_compiler/main.py pj_compiler/examples/shell_sort.pj > pj_compiler/output/syntactic/shell_sort.txt
```
