import pytest


class TestInt:
    @pytest.mark.parametrize(
        'x, y, res',
        [
            (1, 2, 3),
            (5, -5, 0),
            (-5000, -1000, -6000),
        ]
    )
    def test_sum(self, x, y, res):
        assert x + y == res

    @pytest.mark.parametrize(
        'x, y, error',
        [
            (5, ' ', TypeError),
            (5, (5, 1), TypeError),
        ]
    )
    def test_sum_error(self, x, y, error):
        with pytest.raises(error):
            assert x + y


class TestList:
    def test_list_append(self):
        test_list = [1, '2', 3]
        test_list.append(4)
        assert test_list == [1, '2', 3, 4]

    def test_list_remove(self):
        test_list = [1, 2, 3, (4, '')]
        test_list.remove(3)
        assert test_list == [1, 2, (4, '')]


class TestSet:
    def test_set_add(self):
        test_set = set('hello world')
        test_set.add('!')
        assert '!' in test_set

    def test_set_remove(self):
        test_set = {1, 2, 3}
        test_set.remove(2)
        assert test_set == {1, 3}
