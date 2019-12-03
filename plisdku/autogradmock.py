import autograd.extend

def mock(f, df):
    """
    Create an autograd primitive returning f, with a vjp returning df.
    
    Args:
        f: scalar returned by function.
        df: vector returned by VJP of function.
    Returns:
        callable: stub function, autograd enabled
    """
    @autograd.extend.primitive
    def primitive(x):
        return f
    
    def make_vjp(ans, x):
        @autograd.extend.primitive
        def vjp(g):
            return df
        return vjp
    
    autograd.extend.defvjp(primitive, make_vjp)
    return primitive

