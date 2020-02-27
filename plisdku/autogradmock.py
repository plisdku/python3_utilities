import autograd.extend

def mock(f, *dfs):
    """
    Create an autograd primitive returning f, with a vjp returning df.
    
    Args:
        f: scalar returned by function.
        *df: vectors returned by VJPs of function.
    Returns:
        callable: stub function, autograd enabled
    """
    @autograd.extend.primitive
    def primitive(*x):
        return f
    
    def make_make_vjp(df):
        def make_vjp(ans, *x):
            @autograd.extend.primitive
            def vjp(g):
                return df
            return vjp
        return make_vjp
    
    make_vjp_list = [make_make_vjp(df) for df in dfs]
    
    autograd.extend.defvjp(primitive, *make_vjp_list)
    return primitive