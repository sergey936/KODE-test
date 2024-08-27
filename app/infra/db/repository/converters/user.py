from domain.entities.user import User
from domain.values.user import Email, Password
from infra.db.models.user import UserModel


def convert_user_db_model_to_entity(user: UserModel) -> User:
    return User(
        oid=user.id,
        email=Email(user.email),
        password=Password(user.password),
        created_at=user.created_at,
    )


def convert_entity_to_user_db_model(user: User) -> UserModel:
    return UserModel(
        id=user.oid,
        email=user.email.as_generic_type(),
        password=user.password.as_generic_type(),
        created_at=user.created_at,
    )
