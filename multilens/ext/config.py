def init_app(app):
    app.config["SECRET_KEY"] = "\xc5\x03?\xa3\\\xc6%I\r\xf3\xbbe\xfa\x9d\xa9\x06"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///multilens.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
