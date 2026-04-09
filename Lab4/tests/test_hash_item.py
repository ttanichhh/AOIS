from hash_item import HashItem


def test_hash_item_defaults_to_empty_and_not_deleted():
    item = HashItem()

    assert item.key is None
    assert item.data is None
    assert item.value is None
    assert item.hash_address is None
    assert item.is_deleted is False
    assert item.is_empty() is True
    assert item.is_active() is False


def test_hash_item_active_state_changes_after_deletion():
    item = HashItem(key="АТОМ", data="desc", value=42, hash_address=2)

    assert item.is_empty() is False
    assert item.is_active() is True

    item.is_deleted = True

    assert item.is_active() is False
