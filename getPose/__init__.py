import os
import pyodbc
import numpy as np
import json
from attacut import tokenize, Tokenizer

import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    sentence = req.params.get('sentence')
    if not sentence:
        return func.HttpResponse("Missing sentence", status_code=400)

    words = tokenize(sentence)
    return func.HttpResponse(str(words))

    cnxn = pyodbc.connect(os.environ['SQLConnectionString'])
    cursor = cnxn.cursor()
    find_word = 'SELECT w.Word, f.*  FROM [dbo].[FullPose] f JOIN [dbo].[Word] w ON f.Word_ID = w.Word_ID WHERE w.Word IN (?) order by w.Word asc , f.Frame asc'
    #     word = cursor.execute(find_word, (sentence, ))
    #     result = []
    #     frame = []
    #     for w in word:
    #         data = (np.array(w[3:]).reshape((-1,4))).tolist()
    #         frame.append(w.Frame)
    #         result.append(data)
    #     return func.HttpResponse(json.dumps({"frame": frame, "result": result}))
    # else:
        

# logging.info('Python HTTP trigger function processed a request.')