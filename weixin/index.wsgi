import sae
from chenjiajie import wsgi

application = sae.create_wsgi_app(wsgi.application)
