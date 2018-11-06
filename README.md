# sports-analyzer
Link para o escopo e planejamento (cronograma, telas, etc.): https://docs.google.com/document/d/1J_PDWDxSJx3tki_QZ6zik9amBylsWvAucZb4UlRAkbo/edit?usp=sharing




## Para executar updates do flask-sqlalchemy na base de dados:
* executar o terminal python3
* $ from main import db, app
* $ app.app_context().push()
* $ db.init_app(app)
* $ db.create_all()

