import os
import pyodbc
import json
import azure.functions as func
import logging
cnxn = pyodbc.connect(os.environ['SQLConnectionString'])
cursor = cnxn.cursor()

def main(req: func.HttpRequest) -> func.HttpResponse:
    find_word = f'SELECT Word_ID,Word FROM [dbo].[Word]' 
    all_word = cursor.execute(find_word)
    word_dict = []
    for word in all_word:
        word_dict.append({"id": word[0], "word": word[1].strip()})
    return func.HttpResponse(json.dumps({"result" : word_dict}),mimetype="application/json")