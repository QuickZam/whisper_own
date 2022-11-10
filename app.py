from flask import Flask, request, send_file 
# from utils import TranscriptGiver
# import whisper 
from pytube import YouTube 
import os, whisper 
from datetime import timedelta 


app = Flask(__name__) 


class TranscriptGiver: 
    def __init__(self, link, model): 
        self.link = link 
        self.model = model 

    def path_giver(self) -> str:
        yt = YouTube(self.link)
        path = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

        return path

    def inference(self) -> dict: 
        path = self.path_giver()
        audio = whisper.load_audio(path)
        translate_options = dict(task="translate")
        result = self.model.transcribe(audio, **translate_options)
        os.remove(path)

        return result 

    def create_subtitle(self) -> None:
        data = self.inference()
        all = []
        for idx in range(len(data['segments'])):
            start = str(timedelta(seconds=data['segments'][idx]['start']))
            end = str(timedelta(seconds=data['segments'][idx]['end']))
            text = data['segments'][idx]['text']
            final = str(idx+1)+'\n'+start+' --> '+end+'\n'+text+'\n\n'
            all.append(final)


        file_path = f'{self.video_name}.txt'
        with open(file_path, 'w') as file: 
            for it in all: 
                file.write(it)

        return file_path 

def init():
    global model
    model = whisper.load_model("large")




@app.route('/')
def intro_page(): 
    return "Everything is working! 😏"

    
@app.route('/give_files/<link>')
def give_files(link):
    obj = TranscriptGiver(link, model)

    file_path = obj.create_subtitle()
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)