# EduLang-CMPSC-470
This is the repository for the CMPSC 470: Compilers Final project by Avik Bhuiyan, Samuel Shtrambrand, Victor Liu, and Laurence Orji.

This repository contains a small educational language (EduLang) with a
tokenizer, parser, semantic analyzer, and a tiny interpreter. It's designed
for learning compiler construction concepts.

Quick start
-----------

Prerequisites: Python 3.8+.

Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pytest
```

Run the test suite:

```powershell
python -m pytest -q
```

Run an example EduLang program using the bundled CLI:

```powershell
python -m src.main test\edulang_file_test_0.txt
```
OR
```powershell
python -m src.main examples\complex_bmi.edl
```

You can pass runtime variables to the program with `--var name=value`:

```powershell
python -m src.main examples\assignments.edl --var eggs=8
```

Files of interest
- `src/lexer.py` — tokenizer
- `src/parser.py` — recursive-descent parser producing AST nodes
- `src/ast_nodes.py` — AST node definitions
- `src/semantic.py` — simple semantic checks (type checks, name-resolution)
- `src/interpreter.py` — minimal interpreter (evaluation)
- `src/main.py` — CLI runner that lexes/parses/checks and interprets files

Extending the language
----------------------

1. Update `doc/grammar.ebnf` to reflect new syntax.
2. Add AST node classes to `src/ast_nodes.py`.
3. Update `src/parser.py` to emit the new nodes.
4. Add semantic checks in `src/semantic.py` as needed.
5. Implement runtime behavior in `src/interpreter.py` and add tests.

Examples
--------
- `examples/eggs.edl` — simple program showing assignment and if/print.
- `examples/assignments.edl` — shows variable updates and arithmetic.
- `examples/complex_bmi.edl` — utilizes comments and shows of most of EduLang's current functionality.

License
-------
This project is for teaching/demo purposes.
