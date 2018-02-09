import pytest

pytest_plugins = ['clld']


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/coverage'),
        ('get_html', '/parameters/GB020'),
        ('get_json', '/parameters/GB020.geojson'),
        ('get_html', '/dependencys'),
        ('get_html', '/contributions'),
        #('get_html', '/deepfamilys'),
        ('get_html', '/familys'),
        ('get_dt', '/dependencys'),
        ('get_dt', '/contributions'),
        #('get_dt', '/deepfamilys'),
        ('get_dt', '/familys'),
        ('get_dt', '/values'),
        ('get_html', '/contributors/bakkernancy'),
        ('get_html', '/stabilitys/S165'),
        #('get_html', '/deepfamilys/proto-Andoque x proto-Burmeso'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
