from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class Type: pass

@dataclass(frozen=True)
class NatType(Type): pass

@dataclass(frozen=True)
class FunType(Type):
    arg_type: Type
    ret_type: Type

@dataclass(frozen=True)
class IdType(Type):
    left: Term
    right: Term

class Context:
    def __init__(self, types: List[Type] = None):
        # We use a stack for De Bruijn indices
        self.stack = types or []

    def extend(self, t: Type) -> Context:
        """Returns a NEW context with the type pushed (immutability)."""
        return Context(self.stack + [t])

    def lookup(self, index: int) -> Type:
        """Look up by De Bruijn index (0 is the most recent)."""
        try:
            # Indices count from the right of the stack
            return self.stack[-(index + 1)]
        except IndexError:
            raise ValueError(f"Unbound variable at index {index}")
