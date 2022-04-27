def test_autencoder_encoder_valid_pair(encoder_ae):
    valid_pair = 'CG322000'
    assert encoder_ae.is_valid_pair(valid_pair)


def test_autencoder_encoder_invalid_pair(encoder_ae):
    invalid_pair = 'C1'
    assert not encoder_ae.is_valid_pair(invalid_pair)


def test_isolationforest_encoder_valid_pair(encoder_if):
    valid_pair = 'CG322000'
    assert encoder_if.is_valid_pair(valid_pair)


def test_isolationforest_encoder_invalid_pair(encoder_if):
    invalid_pair = 'C1'
    assert not encoder_if.is_valid_pair(invalid_pair)


def test_usage_oob_autoencoder(encoder_ae):
    oob = 'CG322000'
    invalid_pair = 'C1'
    valid_pair = 'CG332110'
    assert (encoder_ae.transform(oob) == encoder_ae.transform(invalid_pair)).all()
    assert (encoder_ae.transform(oob) != encoder_ae.transform(valid_pair)).any()


def test_usage_oob_isolationforest(encoder_if):
    oob = 'CG322000'
    invalid_pair = 'C1'
    valid_pair = 'CG332110'
    assert (encoder_if.transform(oob) == encoder_if.transform(invalid_pair)).all()
    assert (encoder_if.transform(oob) != encoder_if.transform(valid_pair)).any()
