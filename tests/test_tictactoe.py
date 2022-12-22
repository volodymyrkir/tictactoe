# pylint: disable=redefined-outer-name, import-error
"""This module tests MVC structure of tictactoe module"""
from pytest import fixture
from tictactoe_mvc import Field


@fixture
def field_object() -> Field:
    """Returns fixture for field object"""
    return Field(9)


def test_check_all(field_object: Field) -> None:
    """Tests check all function"""
    assert field_object.check_all(' ', 9)


def test_check_all_wrong(field_object: Field) -> None:
    """Tests check all function"""
    assert not field_object.check_all('X', 9)


def test_check_column(field_object) -> None:
    """Tests check all column"""
    for i in [0, 3, 6]:
        field_object.field[i] = 'X'
    assert field_object.check_column('X', 3)


def test_check_column_false(field_object) -> None:
    """Tests check column"""
    for i in [0, 3, 5]:
        field_object.field[i] = 'X'
    assert not field_object.check_column('X', 3)


def test_check_row(field_object) -> None:
    """Tests check row"""
    for i in [0, 1, 2]:
        field_object.field[i] = 'X'
    assert field_object.check_row('X', 3)


def test_check_row_false(field_object) -> None:
    """Tests check row"""
    for i in [0, 1, 3]:
        field_object.field[i] = 'X'
    assert not field_object.check_row('X', 3)


def test_check_diag_false(field_object) -> None:
    """Tests check diag function"""
    for i in [0, 4, 7]:
        field_object.field[i] = 'X'
    assert not field_object.check_diagonal('X', 3)


def test_check_diag(field_object) -> None:
    """Tests check diag function"""
    for i in [0, 4, 8]:
        field_object.field[i] = 'X'
    assert field_object.check_diagonal('X', 3)


def test_get_possible_moves(field_object) -> None:
    """Tests get possible moves function"""
    values = [0, 4, 8]
    for i in values:
        field_object.field[i] = 'X'
    assert field_object.get_possible_moves() == [' '
                                                 for _ in range(9 - len(values))]


def test_make_move(field_object: Field) -> None:
    """Tests check make_move function"""
    field_object.make_move(2, 'X')
    assert field_object.last_play == 2


def test_make_move_y(field_object: Field) -> None:
    """Tests check make_move function"""
    field_object.make_move(2, 'y')
    assert field_object.field[2] == 'y'
