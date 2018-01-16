import pytest

pytest_plugins = ['clld']


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
