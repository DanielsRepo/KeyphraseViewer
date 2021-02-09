from . import db


text_keyphrase = db.Table(
    "text_keyphrase",
    db.Column("text_id", db.Integer, db.ForeignKey("text.id")),
    db.Column("keyphrase_id", db.Integer, db.ForeignKey("keyphrase.id")),
)


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True, nullable=False)
    keyphrases = db.relationship("Keyphrase", secondary=text_keyphrase)

    @staticmethod
    def create(text):
        text_obj = Text(text=text)
        db.session.add(text_obj)
        db.session.commit()
        return text_obj

    @staticmethod
    def get_all():
        return Text.query.all()

    @staticmethod
    def get_text_obj_by_id(text_id):
        return Text.query.get(text_id)

    @staticmethod
    def get_text_id_by_text(text):
        return db.session.query(Text.id).filter_by(text=text).scalar()

    def append_keyphrase(self, keyphrase):
        self.keyphrases.append(keyphrase)
        db.session.commit()


class Keyphrase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyphrase = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, nullable=False, default="")
    disambiguation = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def top_keyphrases():
        return (
            db.session.query(Keyphrase)
            .join(text_keyphrase)
            .group_by(Keyphrase.id)
            .order_by(db.func.count(text_keyphrase.c.keyphrase_id).desc())[:10]
        )

    @staticmethod
    def get_keyphrase_obj(keyphrase):
        return db.session.query(Keyphrase).filter_by(keyphrase=keyphrase).scalar()

    @staticmethod
    def create(keyphrase):
        keyphrase_obj = Keyphrase(**keyphrase)
        db.session.add(keyphrase_obj)
        db.session.commit()
        return keyphrase_obj
