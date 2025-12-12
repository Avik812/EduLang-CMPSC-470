"""CLI runner for EduLang programs.

Usage:
  python -m src.main path/to/program.edl [--var name=value ...] [--strict]

This script reads the given file, runs the lexer, parser, optional semantic
check, and then executes the program with the interpreter. Use `--var` to
provide runtime variables (e.g. `--var age=20`).

Assignment operator now works, so variables can now be defined in test code.
See test/edulang_file_test_0.txt for an example.
"""

import argparse
import sys
from typing import Dict

from .lexer import lexer
from .parser import Parser
from .semantic import SemanticAnalyzer, SemanticError
from .interpreter import interpret


def parse_vars(pairs) -> Dict[str, object]:
    env = {}
    for p in pairs:
        if "=" not in p:
            raise ValueError(f"Invalid var assignment: {p}. Expect name=value")
        name, val = p.split("=", 1)
        # try to coerce to int, else keep as string
        try:
            env[name] = int(val)
        except ValueError:
            env[name] = val
    return env


def run_file(path: str, env: Dict[str, object], strict: bool):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    tokens = lexer(code)
    ast = Parser(tokens).parse()

    analyzer = SemanticAnalyzer(strict=strict)
    try:
        analyzer.analyze(ast)
    except SemanticError as e:
        print(f"Semantic error: {e}")
        return 2

    interpret(ast, env=env, output=print)
    return 0


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser(description="Run an EduLang program")
    ap.add_argument("file", help="EduLang source file to run")
    ap.add_argument("--var", action="append", default=[], help="Provide runtime var as name=value (can repeat)")
    ap.add_argument("--strict", action="store_true", help="Enable strict semantic checking for undefined identifiers")

    args = ap.parse_args(argv)
    try:
        env = parse_vars(args.var)
    except ValueError as e:
        print(e)
        return 2

    return run_file(args.file, env=env, strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())

