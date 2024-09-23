from hubmap_template_helper import uuids as hth_uuids


def test_get_all_uuids():
    uuids = hth_uuids.get_all_uuids()
    assert len(uuids) > 0


def test_get_uuid_to_hubmap_mapping():
    uuids = ['69c70762689b20308bb049ac49653342', 'a1d17fdd270a69c813b872a927dfa5f3']
    mapping = hth_uuids.get_uuid_to_hubmap_mapping(uuids)
    mapping_true = {
        'a1d17fdd270a69c813b872a927dfa5f3': 'HBM232.MBNR.586',
        '69c70762689b20308bb049ac49653342': 'HBM926.SHNZ.594'
    }
    assert mapping == mapping_true


def test_get_hubmap_to_uuid_mapping():
    hubmap_ids = ['HBM232.MBNR.586', 'HBM926.SHNZ.594']
    mapping = hth_uuids.get_hubmap_to_uuid_mapping(hubmap_ids)
    mapping_true = {
        'HBM232.MBNR.586': 'a1d17fdd270a69c813b872a927dfa5f3',
        'HBM926.SHNZ.594': '69c70762689b20308bb049ac49653342'
    }
    assert mapping == mapping_true
