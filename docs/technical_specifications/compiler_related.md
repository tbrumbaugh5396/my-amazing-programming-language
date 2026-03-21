# related

## IR Representations
```
AST / Rich IR Nodes (High-Level / Semantic IR)
<Expr> ::= <Var>
         | <Literal>
         | <Lambda>
         | <Application>
         | <Let>
         | <If>
         | <DependentTypeAnnotation>
         | <ProofTerm>

<Var> ::= identifier
<Literal> ::= int | bool | string | float
<Lambda> ::= "λ" <Var> ":" <Type> "." <Expr>
<Application> ::= <Expr> <Expr>
<Let> ::= "let" <Var> "=" <Expr> "in" <Expr>
<If> ::= "if" <Expr> "then" <Expr> "else" <Expr>
<DependentTypeAnnotation> ::= <Expr> ":" <Type>
<ProofTerm> ::= "proof" <Expr>
Semantic IR / Rich IR (OCaml-style)
type ir_expr =
  | Var of string
  | Lit of literal
  | Lambda of string * ir_type * ir_expr
  | App of ir_expr * ir_expr
  | Let of string * ir_expr * ir_expr
  | If of ir_expr * ir_expr * ir_expr
  | DepType of ir_expr * ir_type
  | Proof of ir_expr
and ir_type =
  | TInt
  | TBool
  | TString
  | TFun of ir_type * ir_type
  | TDependent of ir_type * (ir_expr -> ir_type)
```

## Core IR (Low-Level / Backend-Friendly)

Only runtime-relevant nodes: Var, Lit, Lambda, App, Let, If

Proofs, dependent types, contracts erased during lowering

## Context
```
type context = {
  types: (string, ir_type) Hashtbl.t;          (* Type environment *)
  values: (string, ir_expr) Hashtbl.t;        (* Value environment *)
  proofs: (ir_expr, proof_term) Hashtbl.t;    (* Proof obligations *)
  namespaces: namespace_graph;                 (* Graph of overlapping namespaces *)
  capabilities: (string, capability) Hashtbl.t; (* Authority / capability info *)
}
```

Context is first-class

Provides type checking, proof validation, authority enforcement, and namespace resolution

## Compiler / Elaboration Functions (Inference Rules)
```
Type Inference Function
val infer_type : context -> ir_expr -> ir_type
```

Example rules:
```
(* Variable *)
infer_type ctx (Var x) = lookup ctx.types x

(* Lambda *)
infer_type ctx (Lambda (x, t, body)) =
  let ctx' = add_binding ctx x t in
  let t_body = infer_type ctx' body in
  TFun(t, t_body)

(* Application *)
infer_type ctx (App (f, arg)) =
  match infer_type ctx f with
  | TFun(t_param, t_ret) ->
      let t_arg = infer_type ctx arg in
      if equal_types t_param t_arg then t_ret
      else raise TypeError
  | _ -> raise TypeError

(* Dependent type annotation *)
infer_type ctx (DepType (e, t_expected)) =
  let t_actual = infer_type ctx e in
  if provably_equal ctx t_actual t_expected then t_actual
  else raise TypeError
```

## Elaboration Function
```val elaborate : context -> ast -> rich_ir```

Fills in type annotations, contracts, proofs, and morphisms

Prepares AST for semantic optimization

## Lowering / Erasing Function
```
val lower : rich_ir -> core_ir
```

Removes compile-time-only information (proofs, dependent types)

Produces backend-friendly Core IR

## Semantic Optimizer
```
val apply_rewrites : context -> rich_ir -> rich_ir
```

Uses E-Graph equivalences, dependent types, and namespace morphisms

Produces optimized semantic IR before lowering

5. Key Concepts Summary

| Concept	       | Defined By                    | Role                                                                   |
|------------------------|-------------------------------|------------------------------------------------------------------------|
| IR Nodes               | BNF / Algebraic data types    | Syntax-level and semantic representation                               |
| Context                | Data structures               | Stores types, proofs, namespaces, authority                            |
| Namespace Graph        | Graph structure               | Resolves overlapping namespaces, supports morphisms                    |
| Compiler / Elaboration | Functions over IR and context | Implements type inference, proof checking, elaboration                 |
| Semantic Optimizer     | Functions + E-Graph           | Performs equivalence rewrites using HoTT, dependent types, and context |
| Rich IR	       | Semantic IR                   | Proof-aware, optimizer-friendly                                        |
| Core IR	       | Low-level IR                  | Backend-friendly, runtime-efficient                                    |
| Lowering / Erasing     | Function	                     | Converts Rich IR → Core IR                                             |
