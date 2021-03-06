import yaml
import marshmallow as ma

from utils.errors import ImproperlyConfigured


class AppSection(ma.Schema):
    environment = ma.fields.String(
        required=True,
        validate=ma.validate.OneOf(("development", "production")),
    )
    debug = ma.fields.Boolean(missing=False)


class PostgresSection(ma.Schema):
    database = ma.fields.String(required=True)
    user = ma.fields.String(required=True)
    password = ma.fields.String(required=True)
    host = ma.fields.String(required=True)
    port = ma.fields.Integer(required=True)
    minsize = ma.fields.Integer(required=False)
    maxsize = ma.fields.Integer(required=False)


class ConfigSchema(ma.Schema):
    app = ma.fields.Nested(AppSection, required=True)
    postgres = ma.fields.Nested(PostgresSection, required=True)


def load_config(path):
    """ Load configuration from given path and validate it with ConfigSchema.
        All errors will be reported as ImproperlyConfigured exception
    """

    with open(path) as config_file:
        raw_config = yaml.load(config_file)

    if raw_config is None:
        raise ImproperlyConfigured('Missing configuration')

    schema = ConfigSchema(strict=True)
    try:
        return schema.load(raw_config).data
    except ma.ValidationError as exc:
        raise ImproperlyConfigured(str(exc))
