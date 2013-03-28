import sae
from weixin import wsgi

application = sae.create_wsgi_app(wsgi.application)
