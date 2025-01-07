from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Add the to_dict method to convert model instance to dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
