def dp_cost(term: Term) -> int:
    """Computational complexity metric."""
    if isinstance(term, Nat): return 1
    if isinstance(term, App): return 10
    if isinstance(term, Lambda): return 5
    if isinstance(term, Cast): return 0 # Proofs are truncated
    return 1

def dh_cost(term: Term) -> int:
    """Human cognitive load metric (AST complexity)."""
    # Simple node count
    return 1 # (Recursive implementation here)
