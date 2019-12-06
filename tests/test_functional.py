import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/coverage'),
        ('get_html', '/parameters/GB020'),
        ('get_json', '/parameters/GB020.geojson'),
        ('get_json', '/parameters/GB020.geojson?domainelement=GB020-1'),
        ('get_html', '/languages/nene1249'),
        ('get_html', '/contributions'),
        ('get_html', '/familys'),
        ('get_dt', '/contributions'),
        ('get_dt', '/familys'),
        ('get_dt', '/values'),
        ('get_html', '/contributors/ML'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
