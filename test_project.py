from project import password_validator
from project import password_generator
from project import check_username_validity
import pytest

def test_password_validator():
    assert password_validator("") == ("Invalid", 0)
    assert password_validator("123") == ("Very Weak", 0)
    assert password_validator("abc123") == ("Weak", 25)
    assert password_validator("Asd123!") == ("Medium", 45)  
    assert password_validator("CS50Harvard!") == ("Strong", 70)
    assert password_validator("!;P8mwp?J}~cW{3Y") == ("Very Strong", 90) 

def test_password_generator():
    assert len(password_generator(8)) == 8
    assert len(password_generator(16)) == 16
    assert len(password_generator(32)) == 32
    assert len(password_generator(64)) == 64

def test_check_username_validity():
    test_dict = {
        "David": {"user_id": 1},
        "Harry": {"user_id": 2}
    }

    
    assert check_username_validity("", test_dict) == "Empty"
    assert check_username_validity("David", test_dict) == "Taken"
    assert check_username_validity("Drako", test_dict) == "Valid"
    
