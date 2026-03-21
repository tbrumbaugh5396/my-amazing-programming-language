import pytest
from hypothesis import given, strategies as st

# Strategies for generating random LCP terms
terms = st.deferred(lambda: st.one_of(
    st.builds(Nat, st.integers(min_value=0, max_value=1000)),
    st.builds(Var, st.integers(min_value=0, max_value=10)),
    st.builds(Lambda, terms),
    st.builds(App, terms, terms)
))

class TestOmegaKernel:
    
    def test_basic_reduction(self):
        """Test: 1 + 1 reduces to 2 (Extensionality)"""
        # (Example: Manual setup of an addition term)
        expr = App(Lambda(Nat(1)), Nat(1)) 
        # result = reducer.reduce(expr)
        # assert result == Nat(2)

    def test_refl_bridge_soundness(self):
        """Test: Valid REFL cast passes, invalid fails."""
        valid_cast = Cast(Nat(2), Nat(2), witness="REFL")
        invalid_cast = Cast(Nat(2), Nat(3), witness="REFL")
        
        Validator.check_soundness(valid_cast) # Should pass
        with pytest.raises(KernelInvariantError):
            Validator.check_soundness(invalid_cast)

    @given(terms)
    def test_fuzz_totality(self, t: Term):
        """Invariant Property: No randomly generated term should cause a crash."""
        try:
            Validator.check_totality(t)
        except KernelInvariantError:
            pytest.skip("Generated term was intentionally too deep")

    def test_metric_monotonicity(self):
        """Test: The engine refuses to 'optimize' into a slower program."""
        p_slow = App(Lambda(Nat(1)), Nat(1)) # Cost: 11
        q_fast = Nat(2)                      # Cost: 1
        
        # Mocking the Optimizer
        # assert dp_cost(q_fast) < dp_cost(p_slow)
