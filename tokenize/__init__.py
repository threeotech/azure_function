import os
import pyodbc
import json
from attacut import tokenize, Tokenizer
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    sentence = req.params.get('sentence')
    if not sentence:
        return func.HttpResponse("Missing sentence", status_code=400)
    words = tokenize(sentence)
    return func.HttpResponse(json.dumps({"word": words}),mimetype="application/json")