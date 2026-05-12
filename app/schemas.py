from marshmallow import Schema, fields, validate, ValidationError
 
 
# --- Authentification ---
#Schéma utilisé pour valider les données envoyées à /api/login

class LoginSchema(Schema):
    username = fields.Str(
        required=True,  # Champ "username" obligatoire
        validate=validate.Length(min=3, max=80) # ongueur entre 3 et 80 
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
 
 
# --- Requêtes sur les données /api/data---
# pour valider les params de /api/data; protège API contre les valeurs incorrectes ou dangereuses 
class DataQuerySchema(Schema):
    limit = fields.Int(
        load_default=50,
        validate=validate.Range(min=1, max=200)
    )
    offset = fields.Int(load_default=0) #valeur par défaut = 0
    artist = fields.Str(load_default=None)
 
 
# --- Ajout d'une chanson /api/add---
#garantit que les champs essentiels sont présent et valides 
class AddSongSchema(Schema):
    Track = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    Artist = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    Album_Name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    Spotify_Streams = fields.Int(required=True, validate=validate.Range(min=0))
