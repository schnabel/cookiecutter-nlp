import requests

def test_status():
    response = requests.get('http://192.168.49.2:30000/status')
    assert response.status_code == 200

def test_create_document():
    response = requests.put(
        'http://192.168.49.2:30000/documents',
        json= {
            'title': 'test title',
            'content': 'test content'
        }
    )
    assert response.status_code == 200
