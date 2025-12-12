"""Simple semantic analysis for EduLang.

This module implements a small, conservative semantic checker that walks the
AST produced by the parser and performs basic checks:

- Literal typing (number vs string)
- Binary operator type checking (arithmetic, comparisons, equality)
- `if` condition must be boolean (comparisons/equality produce booleans)
- Optional strict name-resolution: detect use of identifiers that aren't in
  a provided known-names set.

The analyzer is intentionally small and educational. It returns simple type
strings like `'number'`, `'string'`, `'bool'` or `'unknown'` for nodes, and
raises `SemanticError` for definite problems.
"""

from typing import Optional, Set

from .ast_nodes import (
	BlockNode,
	IfNode,
	PrintNode,
	BinaryOpNode,
	LiteralNode,
	IdentifierNode,
)


class SemanticError(Exception):
	pass


class SemanticAnalyzer:
	"""Walk AST and perform lightweight semantic checks.

	Parameters
	- known_globals: optional set of identifier names that are considered
	  defined (e.g., provided by the runtime). If omitted, undefined
	  identifiers are allowed but reported as type `'unknown'` unless
	  `strict=True`.
	- strict: when True, references to unknown identifiers raise
	  `SemanticError`.
	"""

	def __init__(self, known_globals: Optional[Set[str]] = None, strict: bool = False):
		self.known_globals = set(known_globals or [])
		self.strict = strict

	def analyze(self, node):
		"""Analyze `node` and return its type as a string.

		Raises `SemanticError` on definite semantic errors.
		"""
		if isinstance(node, BlockNode):
			for stmt in node.statements:
				self.analyze(stmt)
			return None

		if isinstance(node, PrintNode):
			self.analyze(node.expr)
			return None

		if isinstance(node, IfNode):
			cond_type = self.analyze(node.condition)
			if cond_type != "bool":
				raise SemanticError(f"If condition must be boolean, got '{cond_type}'")
			self.analyze(node.then_block)
			if node.else_block:
				self.analyze(node.else_block)
			return None

		if isinstance(node, BinaryOpNode):
			left_t = self.analyze(node.left)
			right_t = self.analyze(node.right)
			op = node.op

			# arithmetic
			if op in {"+", "-", "*", "/"}:
				if left_t != "number" or right_t != "number":
					raise SemanticError(f"Operator '{op}' requires numeric operands; got {left_t}, {right_t}")
				return "number"

			# comparisons (numeric)
			if op in {">", "<", ">=", "<="}:
				if left_t != "number" or right_t != "number":
					raise SemanticError(f"Comparison '{op}' requires numeric operands; got {left_t}, {right_t}")
				return "bool"

			# equality can compare any two values but types should match when known
			if op in {"==", "!="}:
				if left_t != "unknown" and right_t != "unknown" and left_t != right_t:
					raise SemanticError(f"Equality '{op}' between incompatible types: {left_t} vs {right_t}")
				return "bool"

			# assignment token '=' may appear in parser as OP, but parser doesn't
			# construct an assignment node yet; if encountered here, be conservative.
			if op == "=":
				raise SemanticError("Assignment operator encountered in expression context")

			# unknown operator
			raise SemanticError(f"Unknown operator: {op}")

		if isinstance(node, LiteralNode):
			v = node.value
			if isinstance(v, int):
				return "number"
			if isinstance(v, str):
				# lexer leaves quotes on strings, e.g. '"hi"'
				if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
					return "string"
				# otherwise unknown string-like
				return "string"
			return "unknown"

		if isinstance(node, IdentifierNode):
			name = node.name
			if name in self.known_globals:
				# we don't know the exact type of globals, treat as unknown
				return "unknown"
			if self.strict:
				raise SemanticError(f"Undefined identifier: {name}")
			# permissive mode: allow unknown identifiers (they may be provided
			# at runtime); return 'unknown' so type checks involving them are
			# conservative.
			return "unknown"

		# fallback: unrecognized node
		raise SemanticError(f"Unrecognized AST node: {node!r}")

