from flask import jsonify
 
 
def error_response(error_code: str, message, status: int):
    """
    Retourne une réponse d'erreur JSON structurée et cohérente.
 
    Paramètres :
        error_code (str) : Code lisible identifiant le type d'erreur 
        message          : Message lisible pour le client (str ou dict pour les erreurs de validation)
        status (int)     : Code HTTP à renvoyer
 
    """
    return jsonify({
        "error": error_code,
        "message": message,
        "code": status
    }), status
