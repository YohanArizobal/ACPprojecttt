import pytest
from unittest.mock import patch
from io import StringIO
from FamilyTree import Person, FamilyTree # type: ignore


@pytest.fixture
def family_tree():
    """Fixture to initialize a FamilyTree instance."""
    return FamilyTree()


def test_person_initialization():
    person = Person("Alice", 30, True)
    assert person.name == "Alice"
    assert person.age == 30
    assert person.gender is True
    assert person.child is None
    assert person.sibling is None


def test_person_input_data():
    person = Person()
    mock_inputs = ["Alice", "30", "f"]
    with patch("builtins.input", side_effect=mock_inputs):
        person.input_data()

    assert person.name == "Alice"
    assert person.age == 30
    assert person.gender is False


def test_family_tree_add_root(family_tree):
    mock_inputs = ["Alice", "30", "f"]
    with patch("builtins.input", side_effect=mock_inputs):
        family_tree.add_person()

    assert family_tree.root is not None
    assert family_tree.root.name == "Alice"
    assert family_tree.root.age == 30
    assert family_tree.root.gender is False


def test_family_tree_add_child(family_tree):

    root_inputs = ["Alice", "40", "f"]
    with patch("builtins.input", side_effect=root_inputs):
        family_tree.add_person()

    child_inputs = ["Bob", "10", "m", "Alice", "1"]
    with patch("builtins.input", side_effect=child_inputs):
        family_tree.add_person()

    assert family_tree.root.child is not None
    assert family_tree.root.child.name == "Bob"
    assert family_tree.root.child.age == 10
    assert family_tree.root.child.gender is True


def test_family_tree_add_sibling(family_tree):

    root_inputs = ["Alice", "40", "f"]
    with patch("builtins.input", side_effect=root_inputs):
        family_tree.add_person()

    sibling_inputs = ["Eve", "35", "f", "Alice", "2"]
    with patch("builtins.input", side_effect=sibling_inputs):
        family_tree.add_person()

    assert family_tree.root.sibling is not None
    assert family_tree.root.sibling.name == "Eve"
    assert family_tree.root.sibling.age == 35
    assert family_tree.root.sibling.gender is False


def test_family_tree_search(family_tree):

    root_inputs = ["Alice", "40", "f"]
    with patch("builtins.input", side_effect=root_inputs):
        family_tree.add_person()

    child_inputs = ["Bob", "10", "m", "Alice", "1"]
    with patch("builtins.input", side_effect=child_inputs):
        family_tree.add_person()

    bob = family_tree.search("Bob")
    assert bob is not None
    assert bob.name == "Bob"
    assert bob.age == 10
    assert bob.gender is True

    non_existent = family_tree.search("Charlie")
    assert non_existent is None


def test_display_tree(family_tree, capsys):

    root_inputs = ["Alice", "40", "f"]
    with patch("builtins.input", side_effect=root_inputs):
        family_tree.add_person()

    child_inputs = ["Bob", "10", "m", "Alice", "1"]
    with patch("builtins.input", side_effect=child_inputs):
        family_tree.add_person()

    family_tree.display_tree()
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "Bob" in captured.out


def test_remove_person(family_tree):

    root_inputs = ["Alice", "40", "f"]
    with patch("builtins.input", side_effect=root_inputs):
        family_tree.add_person()

    child_inputs = ["Bob", "10", "m", "Alice", "1"]
    with patch("builtins.input", side_effect=child_inputs):
        family_tree.add_person()

    family_tree.remove_person("Bob")
    assert family_tree.root.child is None

    family_tree.remove_person("Alice")
    assert family_tree.root is None
