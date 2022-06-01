import nomk.algos


def test_neighbors_N_36_012():
    nomks = nomk.algos.get_neighbors(('N-36-012',), '100k')

    real_neighbors = ('N-36-011', 'N-36-023', 'N-36-024', 'N-37-001', 'N-37-013', 'O-36-143', 'O-36-144', 'O-37-133')

    assert len(set(nomks).difference(real_neighbors)) == 0, 'Wrong neighbors calculation'
