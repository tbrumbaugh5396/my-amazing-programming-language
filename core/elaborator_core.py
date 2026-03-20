def infer_type(term: Term, ctx: Context) -> Type:
    if isinstance(term, Nat):
        return NatType()
    
    if isinstance(term, Var):
        return ctx.lookup(term.index)
    
    if isinstance(term, Lambda):
        # Lambda changes the context! 
        # For the prototype, we assume the lambda defines its input type
        # In λ_total^LCP, this is inferred from the environment
        arg_type = NatType() # Placeholder: usually provided by the user
        inner_ctx = ctx.extend(arg_type)
        ret_type = infer_type(term.body, inner_ctx)
        return FunType(arg_type, ret_type)

    if isinstance(term, App):
        f_type = infer_type(term.func, ctx)
        if not isinstance(f_type, FunType):
            raise TypeError("Attempted to apply a non-function")
        # In a real kernel, we'd check if term.arg matches f_type.arg_type
        return f_type.ret_type

    if isinstance(term, Cast):
        # The Bridge Rule verification
        src_type = infer_type(term.source, ctx)
        # Verify witness α proves equivalence in this context
        # (This is where HoTT logic lives)
        return src_type

    raise NotImplementedError(f"Cannot infer type for {type(term)}")
