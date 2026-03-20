import pytest

def test_variable_scope_lookup():
    """Verify that a variable is only accessible if it exists in Г."""
    empty_ctx = Context([])
    
    # In an empty context, Var(0) must fail
    with pytest.raises(ValueError, match="Unbound variable"):
        infer_type(Var(0), empty_ctx)
    
    # In a context with one Nat, Var(0) should be a Nat
    nat_ctx = empty_ctx.extend(NatType())
    assert infer_type(Var(0), nat_ctx) == NatType()

def test_nested_context_growth():
    """Verify λ-abstraction correctly pushes to the context stack."""
    # Syntax: λx. λy. x
    # Context should be [Nat(x), Nat(y)] -> Var(1) refers to x
    inner_body = Var(1) 
    outer_lambda = Lambda(Lambda(inner_body))
    
    res_type = infer_type(outer_lambda, Context())
    
    # Result should be Nat -> (Nat -> Nat)
    assert isinstance(res_type, FunType)
    assert isinstance(res_type.ret_type, FunType)
    assert res_type.ret_type.ret_type == NatType()

def test_shadowing_logic():
    """Verify that new variables shadow older ones correctly (De Bruijn)."""
    # Context: [NatType(older), NatType(newer)]
    # Var(0) should be 'newer', Var(1) should be 'older'
    ctx = Context().extend(NatType()).extend(NatType())
    
    # This is less about the type and more about index mapping
    assert ctx.lookup(0) == ctx.stack[-1]
    assert ctx.lookup(1) == ctx.stack[-2]

def test_cast_context_consistency():
    """Verify that the Bridge preserves the type across the context."""
    p = Nat(10)
    q = Nat(10)
    # A valid cast shouldn't change the underlying type of the term
    term = Cast(source=p, target=q, witness=Nat(0)) # Mock witness
    assert infer_type(term, Context()) == NatType()
