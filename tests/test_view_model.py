from datetime import datetime

from todo_app.constants import NOT_STARTED, COMPLETED
from todo_app.data.item import Item
from todo_app.data.view_model import ViewModel


def test_done_items_returns_all_done_items():
    # Arrange
    test_items = []
    for i in range(1, 5):
        status = COMPLETED if i % 2 == 0 else NOT_STARTED
        item = Item(
            card_id=i,
            title=f"card-{i}",
            description=f"desc-{i}",
            due_date="2099-01-01T00:00:00",
            last_modified="2024-01-01T00:00:00",
            status=status
        )
        test_items.append(item)
    view_model = ViewModel(test_items)

    # Act
    done_items = view_model.done_items

    # Assert
    assert len(done_items) == 2
    assert done_items[0].id == 2
    assert done_items[0].title == "card-2"
    assert done_items[0].description == "desc-2"
    assert done_items[1].id == 4
    assert done_items[1].title == "card-4"
    assert done_items[1].description == "desc-4"


def test_not_started_items_returns_all_not_started_items():
    # Arrange
    test_items = []
    for i in range(1, 6):
        status = COMPLETED if i % 2 == 0 else NOT_STARTED
        item = Item(
            card_id=i,
            title=f"card-{i}",
            description=f"desc-{i}",
            due_date="2099-01-01T00:00:00",
            last_modified="2024-01-01T00:00:00",
            status=status
        )
        test_items.append(item)
    view_model = ViewModel(test_items)

    # Act
    not_started_items = view_model.not_started_items

    # Assert
    assert len(not_started_items) == 3
    assert not_started_items[0].id == 1
    assert not_started_items[0].title == "card-1"
    assert not_started_items[0].description == "desc-1"
    assert not_started_items[1].id == 3
    assert not_started_items[1].title == "card-3"
    assert not_started_items[1].description == "desc-3"
    assert not_started_items[2].id == 5
    assert not_started_items[2].title == "card-5"
    assert not_started_items[2].description == "desc-5"


def test_should_show_all_done_items_returns_true_for_5_done_items():
    # Arrange
    test_items = []
    for i in range(1, 6):
        status = COMPLETED
        item = Item(
            card_id=i,
            title=f"card-{i}",
            description=f"desc-{i}",
            due_date="2099-01-01T00:00:00",
            last_modified="2024-01-01T00:00:00",
            status=status
        )
        test_items.append(item)
    view_model = ViewModel(test_items)

    # Act
    should_show_all_done_items = view_model.should_show_all_done_items

    # Assert
    assert should_show_all_done_items is True


def test_should_show_all_done_items_returns_true_for_more_than_5_done_items_but_no_older_items():
    # Arrange
    test_items = []
    for i in range(1, 7):
        status = COMPLETED
        item = Item(
            card_id=i,
            title=f"card-{i}",
            description=f"desc-{i}",
            due_date="2099-01-01T00:00:00",
            last_modified=datetime.today().isoformat(),
            status=status
        )
        test_items.append(item)
    view_model = ViewModel(test_items)

    # Act
    should_show_all_done_items = view_model.should_show_all_done_items

    # Assert
    assert should_show_all_done_items is True


def test_should_show_all_done_items_returns_false_for_more_than_5_done_items():
    # Arrange
    test_items = []
    for i in range(1, 7):
        status = COMPLETED
        item = Item(
            card_id=i,
            title=f"card-{i}",
            description=f"desc-{i}",
            due_date="2099-01-01T00:00:00",
            last_modified="2023-01-01T00:00:00",
            status=status
        )
        test_items.append(item)
    view_model = ViewModel(test_items)

    # Act
    should_show_all_done_items = view_model.should_show_all_done_items

    # Assert
    assert should_show_all_done_items is False


def test_recent_done_items_includes_only_completed_items_modified_today():
    # Arrange
    test_items = []
    for i in range(1, 5):
        status = COMPLETED if i % 2 == 0 else NOT_STARTED
        last_modified = datetime.today().isoformat() if i % 4 == 0 else "2023-01-01T00:00:00"
        item = Item(
            card_id=i,
            title=f"card-{i}",
            description=f"desc-{i}",
            due_date="2099-01-01T00:00:00",
            last_modified=last_modified,
            status=status
        )
        test_items.append(item)
    view_model = ViewModel(test_items)

    # Act
    recent_done_items = view_model.recent_done_items

    # Assert
    assert len(recent_done_items) == 1
    assert recent_done_items[0].title == "card-4"


def test_older_done_items_includes_only_completed_items_not_modified_today():
    # Arrange
    test_items = []
    for i in range(1, 5):
        status = COMPLETED if i % 2 == 0 else NOT_STARTED
        last_modified = datetime.today().isoformat() if i % 4 == 0 else "2023-01-01T00:00:00"
        item = Item(
            card_id=i,
            title=f"card-{i}",
            description=f"desc-{i}",
            due_date="2099-01-01T00:00:00",
            last_modified=last_modified,
            status=status
        )
        test_items.append(item)
    view_model = ViewModel(test_items)

    # Act
    older_done_items = view_model.older_done_items

    # Assert
    assert len(older_done_items) == 1
    assert older_done_items[0].title == "card-2"
