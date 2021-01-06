import os
import pyodbc
import json
import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient, ContentSettings
prefix = "https://virtualsignlanguage.igat.co.th/"
cnxn = pyodbc.connect(os.environ['SQLConnectionString'])
cursor = cnxn.cursor()
service = BlobServiceClient.from_connection_string(conn_str=os.environ['StorageConnectionString'])
container_client = service.get_container_client("$web")

def main(req: func.HttpRequest) -> func.HttpResponse:
    word_id = req.params.get('word_id')
    if not word_id:
        return func.HttpResponse("Missing word id", status_code=400)
    find_word = f'SELECT w.*,f.Video_Frame,Animation_Frame  FROM [dbo].[Frame] f JOIN [dbo].[Word] w ON f.Word_ID = w.Word_ID WHERE w.Word_ID = ?' 
    word_frame = cursor.execute(find_word,word_id).fetchall()
    selected_frame_list = []
    animation_frame_list = []
    frame = []
    video_url = ""
    word = ""
    if len(word_frame) != 0:
        for w in word_frame:
            word = w.Word.strip()
            video_url = w.TTRS if w.TTRS else w.Setsatian 
            selected_frame_list.append(w.Video_Frame)
            animation_frame_list.append(w.Animation_Frame)
    else:
        find_word = f'SELECT w.* FROM  [dbo].[Word] w WHERE w.Word_ID = ?' 
        word_frame = cursor.execute(find_word,word_id).fetchall()
        if len(word_frame) != 0:
            for w in word_frame:
                word = w.Word.strip()
                video_url = w.TTRS if w.TTRS else w.Setsatian 
        else:
            return func.HttpResponse(json.dumps({}),mimetype="application/json")
    folder = container_client.list_blobs(name_starts_with=f"openpose/{word}/images/")
    for image in folder:
        use = False
        selected_frame = image["name"].split('/')[3].split('.')[0].split('_')[1].lstrip("0") 
        selected_frame = int(selected_frame) if selected_frame != "" else 0
        animation_frame = selected_frame
        if selected_frame in selected_frame_list:
            use = True
            animation_frame = animation_frame_list[selected_frame_list.index(selected_frame)]
        frame.append({"image_path": prefix + image["name"], "video_frame": selected_frame, "use": use, "animation_frame": animation_frame})
    return func.HttpResponse(json.dumps({"word_id" : word_id, "word": word, "video_url": video_url, "frame" : frame}),mimetype="application/json")