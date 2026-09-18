from scipy import sparse


def to_dense(X):
    """Convert a sparse matrix to dense format when necessary."""
    if sparse.issparse(X):
        return X.toarray()

    return X