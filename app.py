from flask import Flask, request, send_file 
from utils import TranscriptGiver
import whisper 

app = Flask(__name__) 
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