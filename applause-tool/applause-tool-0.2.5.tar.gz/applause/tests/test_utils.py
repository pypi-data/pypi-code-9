from applause.utils import get_emails


def test_get_emails():
    emails = [
        "test1@example.com",
        b"""
            test2@example.com 
                test3@example.com
    
    test4@example.com    
        """,
        "test5@example.com",
    ]
    assert get_emails(emails) == [
        "test1@example.com",
        "test2@example.com",
        "test3@example.com",
        "test4@example.com",
        "test5@example.com",
    ]

