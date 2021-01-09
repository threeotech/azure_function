import os
import pyodbc
import json
import pyodbc
from collections import defaultdict
import azure.functions as func

cnxn = pyodbc.connect(os.environ['SQLConnectionString'])
cursor = cnxn.cursor()

def main(req: func.HttpRequest) -> func.HttpResponse:
    sentence = req.params.get('sentence')
    if not sentence:
        return func.HttpResponse("Missing sentence", status_code=400)
    data_dict = defaultdict(list)
    word = []

    find_word = f'SELECT Word_ID,Word FROM [dbo].[Word]'
    all_word = cursor.execute(find_word)
    word_dict = {}
    for word in all_word:
        word_dict[word.Word.strip()] = word[0]

    tmp = ''
    found_words = []
    found_id = []
    i = 0
    j = len(sentence) - 1
    while i != len(sentence):
        current = sentence[i:j+1]
        if current in word_dict.keys():
            if tmp != '':
                found_words.append(tmp)
                tmp = ''
            found_id.append(word_dict[current])
            found_words.append(current)    
            i = j+1
            j = len(sentence) - 1
        elif i == j:
            tmp += sentence[i]
            i = j+1
            j = len(sentence) - 1
        else:
            j = j - 1

    if tmp != '':
        found_words.append(tmp)

    print(found_words)
    print(found_id)
    found_id_param = tuple(found_id)
    if len(found_id) == 1:
        found_id_param = f'(\'{found_id[0]}\')'
    found_words_param = tuple(found_words)
    if len(found_words) == 1:
        found_words_param = f'(\'{found_words[0]}\')'

    if len(found_words) != 0:
        all_meaning = {}
        if len(found_id) != 0:
            query = f'SELECT Word_ID,Word,POS,Meaning FROM [dbo].[Word] WHERE Word_ID IN {found_id_param}'
            meaning_query = cursor.execute(query)
            for meaning in meaning_query:
                all_meaning[meaning.Word.strip()] = {"word_id": meaning.Word_ID,"meaning": meaning.Meaning, "POS":meaning.POS} 
        query = f'SELECT s.Synonym_Word,w.Word_ID,w.Word,w.POS,w.Meaning  FROM [dbo].[Word] w JOIN [dbo].[Synonym] s ON s.Word_ID = w.Word_ID WHERE s.Synonym_Word IN {found_words_param}'
        synonym_query = cursor.execute(query)
        all_synonym = defaultdict(list)
        for synonym in synonym_query:
            all_synonym[synonym.Synonym_Word].append({"word_id": synonym.Word_ID,"meaning": synonym.Meaning, "POS":synonym.POS})
        result = []
        for word in found_words:
            if word in all_meaning:
                info = {"original_word": word,
                        "word_id": all_meaning[word]["word_id"],
                        "meaning": all_meaning[word]["meaning"],
                        "pos": all_meaning[word]["POS"],
                        }
            else:
                info = {"original_word": word}
            if word in all_synonym:
                info["alternative"] = all_synonym[word]
            result.append(info)    
        return func.HttpResponse(json.dumps({"result": result}),mimetype="application/json")
    else:
        return func.HttpResponse(json.dumps({"result": {}}),mimetype="application/json")



