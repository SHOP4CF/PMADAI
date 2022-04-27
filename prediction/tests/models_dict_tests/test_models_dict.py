import pytest


@pytest.mark.models_specific_keys
def test_specific_painting_type_key(key_1, key_2):
    assert not (key_1 == key_2)
    assert key_1 == key_1
    assert key_2 == key_2


@pytest.mark.general_models_dict
def test_general_models_dict(general_dict, key_1, key_2, not_existing_key):
    assert general_dict[key_1] == 'key_1'
    assert general_dict[key_2] == 'key_2'
    assert general_dict[not_existing_key] == 'general_model'
