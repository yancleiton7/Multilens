import os
from dynaconf import FlaskDynaconf


def init_app(app):
    FlaskDynaconf(app)
    app.config["SECRET_KEY"] = os.getenv(r"\xc2Q?\x9cF\xe6M[A\xda\xc5\xe7\xb2\x1e<\xa4", "multilens")
    app.config.load_extensions("EXTENSIONS")
    
    #Configuração para Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
