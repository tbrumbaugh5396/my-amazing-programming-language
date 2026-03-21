class KernelInvariantError(Exception): pass

class Validator:
    @staticmethod
    def check_totality(term: Term, depth: int = 0, max_depth: int = 100):
        """Invariant: Every term must be finite and structurally sound."""
        if depth > max_depth:
            raise KernelInvariantError("Non-termination detected: Max recursion depth exceeded.")
        # Recursive check of sub-terms...
        
    @staticmethod
    def check_soundness(cast: Cast):
        """Invariant: The witness must prove equivalence."""
        # This will eventually call the Elaborator logic
        if cast.witness == "REFL" and cast.source != cast.target:
            raise KernelInvariantError(f"Soundness Violation: {cast.source} != {cast.target} under REFL")
