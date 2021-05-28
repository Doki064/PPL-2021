# JCOSIM
*Java Compiler Simulator*


A project for Principles of Programming Language course 2021

(International University - Vietnam National University HCMC)

---

# Supported Feature
## Basic
- Primitive data types: int, float, double, string, boolean
- Java type inference using the var keyword
- Simple function call
- Single file compilation
- Comments, both singleline and multiline
## Advanced
- Type inference using `var` keyword

---

# Programming Language
Python version 3.8

---

# Dependencies
## Packages
- pipenv
- pydot

## Dev Packages
- pyinstaller
- autopep8

---

# Target intermediate language
C 

---

# Modules
There are 8 modules in the system:

![JCOSIM Modules](/docs/modules.png "JCOSIM Modules")

Each of the modules is responsible for a different phase in the compilation process.

All of these 8 modules are wrapped inside the main `jcosim` container, which is responsible for initializing, calling and dependency injection between the modules.

The structure of the who system is similar to that of a standard compiler

![Compiler Architecture](/docs/compiler.png "Compiler Architecture")

As we have discussed above, the intermediate form we choose here is the C language

Target language here is native binary code.

The difference here is that JCOSIM will not support steps that are related to code optimization like machine-independent code improvement and machine-specific code improvement.


---

# Class Diagram

![JCOSIM class diagram](/docs/all-JCOSIM_Class_Diagram.png "JCOSIM Class Diagram")

---

# Usage Requirements
Users do not need to install any software to use most of the features of JCOSIM.

The only thing that requires an external package is the option to visualize parse trees, which depends on Graphviz, a very popular software made specifically for visualizing graphs grammatically. Graphviz is supported on a lot of platforms, users can get a copy of graphviz [here](https://graphviz.org/download)

---

# Manual
```
Compile simple Java source file to C then to executables.
Usage: jcosim -i <file> [OPTIONS] 
Options:
    -i <file>,      --input <file>          input source file path and name
    -o <file>,      --output <file>         output executable path and name
    -s,             --symtable              generate symtable only
    -t,             --token                 generate tokens only
    -p,             --parsetree             generate parse tree only
    -a,             --analyzedtree          generate analyzed parse tree only
    -g,             --gencode               generate generated C code only
    -c <path>,      --clean <path>          clean all outputs in <path>
    -u,             --use-gcc               use gcc compiler specified in jcosim.config.json
    -v,             --verbose               generate all intermediate output
    -h,             --help                  display this help and exit
* NOTE: to generate parse tree, graphviz needs to be installed on the system
Examples:
    - Compile a file to exe with no intermediate output:
        jcosim -i Main.java -o Main
        jcosim --input Main.java --output Main
    - Compile a file to exe with intermediate output:
        jcosim -i Main.java -o Main -v
        jcosim --input Main.java --output Main --verbose
    - Show symtable:
        jcosim -i Main.java -s
        jcosim --input Main.java --symtable
    - Show tokens:
        jcosim -i Main.java -t
        jcosim --input Main.java --token
    - Show parse tree:
        jcosim -i Main.java -p
        jcosim --input Main.java --parsetree
    - Show analyzed parse tree:
        jcosim -i Main.java -a
        jcosim --input Main.java --analyzedtree
    - Show generated C code:
        jcosim -i Main.java -g
        jcosim --input Main.java --gencode
    - Clean outputs
        jcosim -c .
        jcosim --clean .
```

---

# Set up

## Clone Project
```
git clone https://github.com/tidunguyen/PPL-2021
cd PPL-2021
```

## Install dependencies
```
pipenv shell
pipenv install
pipenv install --dev
```

## Run using python file
```
python src/jcosim.py -i jcosim -i <file> [OPTIONS]
```
***Please follow instructions in the manual***

---

# Run With Executable
Make sure that all pipenv dependencies (including dev ones) are installed before continue.

## Build Executable


### Linux/MacOS/Other Unix based OSes
```
pipenv run build-unix
```
### Windows
```
pipenv run build-win
```

## Run Executable
```
./dist/jcosim -i jcosim -i <file> [OPTIONS]
```
***Please follow instructions in the manual***

***You may replace forward slash with backslash on Windows in case of path errors***

---

# Run tests
```
python test/organized_tests/run.py
```

***You can customize test runs as you want inside that file***

---

# Detailed report
Click [Here](https://docs.google.com/document/d/12YHBy-THlM6mBta-NcPLqHFu4nw_4xZC1VS8wH_L4YM/edit?usp=sharing)

---

# License

Apache-2.0