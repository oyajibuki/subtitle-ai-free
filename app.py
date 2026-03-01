from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import whisper
import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
import pandas as pd
from datetime import timedelta

app = FastAPI()

# Store loaded models to avoid reloading
loaded_models = {}

def get_model(model_name: str):
    if model_name not in loaded_models:
        loaded_models[model_name] = whisper.load_model(model_name)
    return loaded_models[model_name]

# Helper for SRT formatting
def format_timestamp(seconds: float) -> str:
    delta = timedelta(seconds=seconds)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Helper for ASS formatting (H:MM:SS.CC)
def format_timestamp_ass(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours}:{minutes:02}:{secs:05.2f}"

# Temporary directory for processing
TEMP_DIR = Path("/tmp/ai_subtitle")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Serve the React/HTML frontend
    html_path = Path("landing.html")
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return "<h1>Landing page not found</h1>"

@app.post("/transcribe")
def transcribe_audio(
    file: UploadFile = File(...),
    target_lang: str = Form("auto"),
    model_size: str = Form("base")
):
    """
    Handles file upload, runs Whisper, and returns SRT and ASS content.
    """
    try:
        # Save temp file
        temp_file_path = TEMP_DIR / file.filename
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"Processing {file.filename} with {model_size} model...")
        
        # Load model & transcribe
        model = get_model(model_size)
        
        transcribe_args = {
            "fp16": False, # Ensure stability on varying hardware
        }
        
        if target_lang != "auto":
            transcribe_args["language"] = target_lang

        result = model.transcribe(str(temp_file_path), **transcribe_args)
        
        # Format SRT & ASS
        srt_content = []
        ass_header = [
            "[Script Info]", "ScriptType: v4.00+", "Timer: 100.0000", "",
            "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
            "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1", "",
            "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
        ]
        ass_content = ass_header.copy()

        for i, segment in enumerate(result["segments"], start=1):
            # SRT
            start_srt = format_timestamp(segment["start"])
            end_srt = format_timestamp(segment["end"])
            text = segment["text"].strip()
            srt_content.append(f"{i}\n{start_srt} --> {end_srt}\n{text}\n")
            
            # ASS
            start_ass = format_timestamp_ass(segment["start"])
            end_ass = format_timestamp_ass(segment["end"])
            ass_content.append(f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{text}")
            
        srt_text = "\n".join(srt_content)
        ass_text = "\n".join(ass_content)
        
        # Cleanup
        temp_file_path.unlink()
        
        base_name = file.filename.rsplit('.', 1)[0]
        return JSONResponse({
            "success": True, 
            "srt_content": srt_text,
            "ass_content": ass_text,
            "srt_filename": f"{base_name}.srt",
            "ass_filename": f"{base_name}.ass"
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860)