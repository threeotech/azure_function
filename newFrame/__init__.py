import os
import pyodbc
import json
import azure.functions as func
import logging
cnxn = pyodbc.connect(os.environ['SQLConnectionString'])
cursor = cnxn.cursor()


def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    word_id = req_body.get("word_id")
    frame = req_body.get("frame")
    if not word_id or not frame:
        return func.HttpResponse("Missing json body request", status_code=400)
    delete_frame = 'DELETE FROM [dbo].[Frame] WHERE Word_ID = ?' 
    cursor.execute(delete_frame,word_id)
    cnxn.commit()
    video_frame = []
    animation_frame = []
    for item in frame:
        video_frame.append(item["video_frame"])
        animation_frame.append(item["animation_frame"])
    insert_frame = f'INSERT INTO [dbo].[Frame] (Word_ID,Video_Frame,Animation_Frame) VALUES (?,?,?)' 
    value_list = [(word_id,v,a) for v,a in zip(video_frame,animation_frame)]
    cursor.fast_executemany = True
    cursor.executemany(insert_frame,value_list)
    cnxn.commit()
    return func.HttpResponse("DONE",status_code=200)
