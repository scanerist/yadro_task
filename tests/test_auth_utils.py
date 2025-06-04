from app.auth.utils import get_password_hash, verify_password

def test_password_hash_and_verify():
    password = "supersecret"
    hash_ = get_password_hash(password)
    assert hash_ != password
    assert verify_password(password, hash_)
    assert not verify_password("wrong", hash_)

