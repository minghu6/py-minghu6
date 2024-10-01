from doctest import run_docstring_examples


def test_iterator_same():
    from minghu6.itertools import iterator_same

    run_docstring_examples(iterator_same, locals())


def test_iterator_zip_eq():
    from minghu6.itertools import iterator_zip_eq

    def gen1():
        yield from [11, 12, 13]

    assert iterator_zip_eq([11, 12, 13], iter((11, 12, 13)), gen1())
    assert iterator_zip_eq([11, 12, 13], [11, 12, 14]) == False


if __name__ == "__main__":
    test_iterator_zip_eq()
    test_iterator_same()
