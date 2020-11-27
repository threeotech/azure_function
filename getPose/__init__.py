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
    word_list = tuple(words)
    pose_dict = {}
    frame_dict = {}
    if len(words) == 1:
        word_list = f'(\'{words[0]}\')'
    cnxn = pyodbc.connect(os.environ['SQLConnectionString'])
    cursor = cnxn.cursor()
    find_word = f'SELECT w.Word, f.*  FROM [dbo].[FullPose] f JOIN [dbo].[Word] w ON f.Word_ID = w.Word_ID WHERE w.Word IN {word_list} order by w.Word asc , f.Frame asc' 
    word = cursor.execute(find_word)
    word_list = tuple(words)
    for name in word_list:
        pose_dict[name] = []
        frame_dict[name] = []
    for w in word:
        data = (np.array(w[4:]).reshape((-1,4))).tolist()
        pose_dict[w.Word.strip()].append(data)
        frame_dict[w.Word.strip()].append(w.Frame)
    return func.HttpResponse(json.dumps({"frame": frame_dict, "result": pose_dict, "word": word_list}))
    # else:
        

# logging.info('Python HTTP trigger function processed a request.')