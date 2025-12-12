
class ScopedEnv:
    def __init__(self, initial=None):
        self.scopes = [dict(initial or {})]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, value):
        self.scopes[-1][name] = value

    def assign(self, name, value):
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        raise RuntimeError(f"Variable '{name}' not declared")

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise RuntimeError(f"Variable '{name}' not declared")