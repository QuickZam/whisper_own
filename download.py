import whisper
import torch

def download_model():
    model = whisper.load_model("large")

if __name__ == "__main__":
    download_model()