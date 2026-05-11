from marshmallow import Schema, fields, validate, ValidationError
 
 
# --- Authentification ---
 
class LoginSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80)
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=200)
    )
 
 
class RegisterSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80)
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=200)
    )
    email = fields.Email(required=True)
 
 
# --- Requêtes sur les données ---
 
class DataQuerySchema(Schema):
    limit = fields.Int(
        load_default=50,
        validate=validate.Range(min=1, max=200)
    )
    offset = fields.Int(load_default=0)
    artist = fields.Str(load_default=None)
 
 
# --- Ajout d'une chanson ---
 
class AddSongSchema(Schema):
    Track = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    Artist = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    Album_Name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    Spotify_Streams = fields.Int(required=True, validate=validate.Range(min=0))
