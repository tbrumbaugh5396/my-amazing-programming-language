## 1. The Core Calculus Specification (λ total LCP)

This section defines the mathematical bounds of the typing judgment.

```JSON
{
  "calculus_id": "lambda-total-LCP",
  "judgement_form": "Γ ; Δ ; Κ ⊢ e : T ▷ ε",
  "contexts": {
    "Γ": "Unrestricted (Intuitionistic) - Persistent types, proofs, and total functions.",
    "Δ": "Linear (Substructural) - Resources, handles, and unique capabilities.",
    "Κ": "Authority (Set) - The set of allowed effect labels."
  },
  "fragment_stratification": {
    "Total": "Structural recursion, termination guaranteed, used for Γ and Types.",
    "Partial": "General recursion allowed, Turing complete, used for runtime execution."
  }
}
```

## 2. The Effect & Capability Lattice

This defines how "Power" is checked. 
A program is sound if its internal effects ϵ are a subset of its granted capabilities $K$.

| Effect Label	| Authority Required |	Description |
|--------------|--------------------|-------------|
| Pure |	∅ |	No side effects, deterministic. |
| Read/Write	| Cap<FS> |	Access to the linear file system. |
| Net	 | Cap<Network>	| Non-deterministic socket IO. |
| Unsafe	| Cap<Machine_Root> |	FFI, raw pointers, and manual memory. |
Reflect	Cap<Type_Witness>	Runtime type inspection (Non-erased). |

## 3. The Phase Separation and Erasure Protocol

This defines the lifecycle of a term from source code to machine code. 

```JSON
{
  "stages": [
    {
      "id": "Stage-0",
      "name": "Static Analysis",
      "actions": ["Type-checking", "Constraint Solving", "Metaprogramming Splice"],
      "retention": "All metadata (Ghost + Real)"
    },
    {
      "id": "Stage-1",
      "name": "Proof Erasure",
      "actions": ["Computational Irrelevance Check", "Ghost Stripping"],
      "rule": "If t : Ghost, then delete t from AST."
    },
    {
      "id": "Stage-2",
      "name": "Codegen",
      "actions": ["Linear variable optimization", "LLVM/Assembly Emission"],
      "retention": "Real values only"
    }
  ]
}
```

## 4. Manifest of Primitive Operations (The "Safe" API)

To implement the Verified Bootloader or any app, the compiler provides these primitives:
```
reify<T>()
```
: Converts a Stage-0 Type into a Stage-2 TypeToken.

```
split(linear Δ):
```

The core logic for context splitting ($Δ=Δ_1⊎Δ_2$).
```
borrow(linear T)
```
: Temporarily treats a linear resource as unrestricted within a scope (Region-based).

```
quote/splice
```
: The entry points for the Metaprogramming engine.

## 5. Soundness Verification Checklist (The "Kernel" Goals)

As you build the compiler, each module must satisfy these formal lemmas:
- Progress: A well-typed term is either a value or can take a step.
- Preservation: If $t:T$ and $t→t$, then $t:T$.
- Linearity Preservation: Context splitting never duplicates a resource.
- Authority Monotonicity: Subtyping never increases the effect set $ϵ$.
- Termination: All Stage-0 computations land on a value (No compiler hangs).

## Final Implementation Summary

By following this manifest, you are creating a language where:
- Safety is not a feature; it is the Type.
- Security is not a policy; it is the Capability.
- Performance is not an optimization; it is the Erasure.

Would you like me to generate a "Reference Implementation" of the Type-Checker's core check function for the Linear Context Splitting (Δ)? This is the single most important algorithm in the entire system.
