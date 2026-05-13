from app.auth import hash_password, verify_password

def test_hash_is_not_plaintext():
    h = hash_password("secret123")  # On génère un hash à partir d'un mdp
    assert h != "secret123" #different du mdp original
    assert h.startswith("$2b$") #tous les bcrypt commence par "$2b$"

def test_verify_password_correct():
    h = hash_password("secret123")
    assert verify_password("secret123", h) is True

def test_verify_password_wrong():
    h = hash_password("secret123")
    assert verify_password("wrong", h) is False