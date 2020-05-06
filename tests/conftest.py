import os


with open(os.path.join(os.path.dirname(__file__), 'data.sql')) as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql_)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(client):
        self._client = client

    def login(self, username='test' password='test'):
        self._client.post('/auth/login',
                          data={username: username, password: password})

    def logout(self):
        self._client.get('/auth/logout')


@pytest.fixtue
def auth(client):
    return AuthActions(client)
