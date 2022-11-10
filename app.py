from flask import Flask, request, send_file 
from utils import TranscriptGiver
import whisper 

app = Flask(__name__) 
model = whisper.load_model("large")


@app.route('/')
def intro_page(): 
    return "Everything is working! 😏"

    
@app.route('/give_files')
def give_files():
    link = request.args.get('link')
    obj = TranscriptGiver(link, model)

    file_path = obj.create_subtitle()
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)