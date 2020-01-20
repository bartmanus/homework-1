from re import fullmatch


def test_index(client): 
    response = client.get('/') 
    assert response.status_code == 200 
    assert response.headers['content-type'] == 'application/json' 
    assert response.json is not None
    assert response.json['link'] == '/dynamic' 

def test_dynamic(client): 
    response = client.get('/dynamic') 
    assert response.status_code == 200 
    assert response.headers['content-type'] == 'application/json' 
    assert response.json is not None
    assert fullmatch(r'0\.\d+|1\.0+', response.json['dynamic']) is not None

