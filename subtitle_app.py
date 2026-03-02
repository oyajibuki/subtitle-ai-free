import streamlit as st
import sys
import os

# PyInstallerの --noconsole 時における sys.stdout / sys.stderr の None エラー対策
class DummyStream:
    def write(self, *args, **kwargs): pass
    def flush(self, *args, **kwargs): pass

if sys.stdout is None:
    sys.stdout = DummyStream()
if sys.stderr is None:
    sys.stderr = DummyStream()

from datetime import timedelta
from moviepy import VideoFileClip
import streamlit.components.v1 as components
import license_manager
from translations import get_text

# --- FFmpegのパス設定 ---
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    os.environ["PATH"] = base_path + os.pathsep + os.environ["PATH"]
else:
    os.environ["PATH"] = os.getcwd() + os.pathsep + os.environ["PATH"]

# --- 設定とユーティリティ関数 ---

def format_timestamp(seconds):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def format_timestamp_ass(seconds):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    centis = int(td.microseconds / 10000)
    return f"{hours}:{minutes:02}:{secs:02}.{centis:02}"

def create_srt_content(df, is_pro: bool):
    srt_content = ""
    offset = 1
        
    for idx, row in df.iterrows():
        start = format_timestamp(row['start'])
        end = format_timestamp(row['end'])
        text = row['text']
        srt_content += f"{idx + offset}\n{start} --> {end}\n{text}\n\n"
    return srt_content

def create_ass_content(df, font_name="MS Gothic", font_size=40, primary_color="&H00FFFFFF", outline_color="&H00000000", outline_width=2, shadow_depth=0, alignment=2, margin_v=10):
    header = f"""[Script Info]
Title: Streamlit Auto Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},{font_size},{primary_color},&H000000FF,{outline_color},&H00000000,0,0,0,0,100,100,0,0,1,{outline_width},{shadow_depth},{alignment},10,10,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = ""
    for idx, row in df.iterrows():
        start = format_timestamp_ass(row['start'])
        end = format_timestamp_ass(row['end'])
        text = row['text'].replace('\n', '\\N')
        events += f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n"
    
    return header + events

def hex_to_ass_color(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return "&H00FFFFFF"
    r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
    return f"&H00{b}{g}{r}".upper()

def get_app_dir():
    import sys
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def save_uploaded_file(uploaded_file, lang_code):
    try:
        app_dir = get_app_dir()
        temp_dir = os.path.join(app_dir, "temp_files")
        os.makedirs(temp_dir, exist_ok=True)
        
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(get_text(lang_code, "err_analysis", e=e))
        return None

def get_video_duration(file_path):
    try:
        with VideoFileClip(file_path) as clip:
            return clip.duration
    except Exception as e:
        return 0

@st.cache_resource
def load_model(model_size):
    import whisper
    return whisper.load_model(model_size)

# --- Application Main ---

st.set_page_config(page_title="AI Subtitle Generator", layout="wide")

# 言語切り替え設定
LANGUAGES = {
    "🇯🇵 日本語": "ja",
    "🇺🇸 English": "en",
    "🇨🇳 中文": "zh",
    "🇰🇷 한국어": "ko",
    "🇧🇷 Português": "pt"
}

# ヘッダー右上に言語選択を配置
col_spacer, col_lang = st.columns([8, 2])
with col_lang:
    selected_lang_label = st.selectbox(
        "🌐 Language",
        list(LANGUAGES.keys()),
        index=0,
        label_visibility="collapsed"
    )
    ui_lang = LANGUAGES[selected_lang_label]

is_pro = license_manager.is_pro_mode()

with st.spinner("..."):
    import whisper
    import pandas as pd

if is_pro:
    st.title(get_text(ui_lang, "app_title_pro"))
    st.markdown(get_text(ui_lang, "pro_desc"))
else:
    st.title(get_text(ui_lang, "app_title_free"))
    st.info(get_text(ui_lang, "free_desc"))
    st.markdown(get_text(ui_lang, "free_limits_title"))
    st.markdown(get_text(ui_lang, "free_limits"))

# サイドバー設定
with st.sidebar:
    license_manager.render_license_ui(ui_lang)
    st.divider()

    st.header(get_text(ui_lang, "settings_title"))
    if is_pro:
        model_map = {
            "tiny": "tiny",
            "base": "base",
            "smart": "small",
            "Pro": "medium"
        }
    else:
        model_map = {
            "tiny": "tiny",
            "base": "base"
        }
        
    model_label = st.selectbox(
        get_text(ui_lang, "model_label"),
        list(model_map.keys()),
        index=1 if not is_pro else 2,
        help=get_text(ui_lang, "model_help_pro")
    )
    model_size = model_map[model_label]
    
    # 解析言語（Whisper用）
    audio_lang_map = {
        get_text(ui_lang, "lang_ja"): "ja",
        get_text(ui_lang, "lang_en"): "en",
        get_text(ui_lang, "lang_zh"): "zh",
        get_text(ui_lang, "lang_ko"): "ko",
        get_text(ui_lang, "lang_pt"): "pt"
    }
    
    default_lang_idx = 0
    lang_values = list(audio_lang_map.values())
    if ui_lang in lang_values:
        default_lang_idx = lang_values.index(ui_lang)

    audio_lang_label = st.selectbox(
        get_text(ui_lang, "lang_label"),
        list(audio_lang_map.keys()),
        index=default_lang_idx
    )
    audio_lang = audio_lang_map[audio_lang_label]

    st.divider()
    
    if is_pro:
        st.header(get_text(ui_lang, "style_title"))
        st.caption(get_text(ui_lang, "style_desc"))
        
        font_map = {
            "Arial": "Arial",
            "MS Gothic": "MS Gothic",
            "Meiryo": "Meiryo",
            "Times New Roman": "Times New Roman"
        }
        
        font_label = st.selectbox(get_text(ui_lang, "font_label"), list(font_map.keys()), index=0)
        st.markdown("---")
        font_name = font_map[font_label]
        font_size = st.slider(get_text(ui_lang, "font_size"), 10, 100, 40)
        font_color_hex = st.color_picker(get_text(ui_lang, "font_color"), "#FFFFFF")
        outline_width = st.slider(get_text(ui_lang, "outline_width"), 0, 10, 2)
        outline_color_hex = st.color_picker(get_text(ui_lang, "outline_color"), "#000000")
        
        # 簡易的に固定マップ
        alignment_map = {"▼": 2, "■": 5, "▲": 8}
        position_label = st.selectbox(get_text(ui_lang, "position"), list(alignment_map.keys()), index=0)
        alignment = alignment_map[position_label]
        
        margin_v = st.slider(get_text(ui_lang, "margin_v"), 0, 200, 20)
        
        ass_primary_color = hex_to_ass_color(font_color_hex)
        ass_outline_color = hex_to_ass_color(outline_color_hex)
    else:
        st.caption(get_text(ui_lang, "pro_features_title"))
        st.markdown(get_text(ui_lang, "pro_features"))

    st.divider()
    
    if 'visitor_count' not in st.session_state:
        try:
            import urllib.request
            import json
            import ssl
            import urllib.parse

            # --- 訪問者情報の取得 ---
            headers = getattr(st, "context", {}).headers
            user_ip = headers.get("x-forwarded-for", "unknown").split(",")[0]
            user_agent = headers.get("user-agent", "unknown")
            safe_ua = urllib.parse.quote(user_agent)
            
            # ユーザー指定のURL。パラメータを追加して詳細ログを試みる
            gas_url = f"https://script.google.com/macros/s/AKfycbznxYkj5ixnK_pHkGR8LUYhEYdvSYpaiF3x4LaZy964wlu068oak1X1uuIiyqCEtGWF/exec?page=AI-Subtitle&ip={user_ip}&ua={safe_ua}"
            
            # SSL検証をスキップ (環境によるエラー対策)
            ctx = ssl._create_unverified_context()
            with urllib.request.urlopen(gas_url, timeout=10, context=ctx) as response:
                res_body = response.read().decode('utf-8')
                data = json.loads(res_body)
                st.session_state['visitor_count'] = data.get('count', 0)
                st.session_state['visitor_log_status'] = "✅ Connected"
        except Exception as e:
            st.session_state['visitor_count'] = None
            st.session_state['visitor_log_status'] = f"❌ Error: {str(e)}"

    if st.session_state.get('visitor_count') is not None:
        st.caption(f"👀 Visitors: {st.session_state['visitor_count']}")
    
    # デバッグ用：エラーがある場合のみ表示
    if st.session_state.get('visitor_log_status') and "❌" in st.session_state['visitor_log_status']:
        st.caption(st.session_state['visitor_log_status'])

if not is_pro:
    components.html(
        """
        <script>
        function hideLimitText() {
            const elements = window.parent.document.querySelectorAll('*');
            elements.forEach(el => {
                if (el.tagName !== 'BODY' && el.tagName !== 'HTML' && el.children.length === 0) {
                     if (el.textContent && (el.textContent.includes('Limit') && (el.textContent.includes('MB') || el.textContent.includes('GB')))) {
                        el.style.display = 'none';
                        el.style.visibility = 'hidden';
                        el.innerHTML = '';
                    }
                }
            });
            const uploaders = window.parent.document.querySelectorAll('[data-testid="stFileUploader"] small');
            uploaders.forEach(el => el.style.display = 'none');
        }
        hideLimitText();
        setInterval(hideLimitText, 500);
        </script>
        """,
        height=0,
        width=0
    )

    st.markdown(
        """
        <style>
        .watermark-bg {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-35deg);
            font-size: 6vw;
            color: rgba(150, 150, 150, 0.12);
            z-index: 999999;
            pointer-events: none;
            white-space: nowrap;
            user-select: none;
            font-weight: 900;
            letter-spacing: 5px;
        }
        [data-testid="stFileUploader"] small {
            display: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
            font-size: 0 !important;
        }
        [data-testid="stFileUploader"] section > div > div > small {
            display: none !important;
        }
        [data-testid="stFileUploader"] span {
            font-size: 14px !important;
        }
        </style>
        <div class="watermark-bg">Created by AI Subtitle Free</div>
        """,
        unsafe_allow_html=True
    )

ul_label = get_text(ui_lang, "upload_label_free") if not is_pro else get_text(ui_lang, "upload_label_pro")

st.caption(get_text(ui_lang, "supported_formats"))
uploaded_file = st.file_uploader(ul_label, type=["mp4", "mov", "wav", "mp3", "m4a", "mk4"])

if uploaded_file is not None:
    if not is_pro and uploaded_file.size > 100 * 1024 * 1024:
        st.error(get_text(ui_lang, "err_size"))
    else:
        temp_file_path = save_uploaded_file(uploaded_file, ui_lang)
        
        if temp_file_path:
            st.markdown(get_text(ui_lang, "preview"))
            col_preview, col_empty = st.columns([1, 2])
            with col_preview:
                if any(ext in uploaded_file.name for ext in ["mp4", "mov"]):
                    st.video(temp_file_path)
                else:
                    st.audio(temp_file_path)
            
            st.markdown("---")
            
            duration = get_video_duration(temp_file_path)
            
            if not is_pro and duration > 300:
                st.error(get_text(ui_lang, "err_duration", sec=int(duration)))
            else:
                if st.button(get_text(ui_lang, "btn_start"), type="primary"):
                    gpu_state = "True" if whisper.torch.cuda.is_available() else "False"
                    analyzing_msg = get_text(ui_lang, "sp_analyzing", model=model_size, gpu=gpu_state)
                    
                    with st.spinner(analyzing_msg):
                        try:
                            model = load_model(model_size)
                            result = model.transcribe(temp_file_path, language=audio_lang)
                            
                            st.session_state['segments'] = result['segments']
                            st.session_state['file_path'] = temp_file_path
                            st.success(get_text(ui_lang, "msg_complete"))
                        except Exception as e:
                            st.error(get_text(ui_lang, "err_analysis", e=e))

# 結果表示と編集エリア
if 'segments' in st.session_state:
    st.divider()
    st.header(get_text(ui_lang, "edit_title"))
    
    df = pd.DataFrame(st.session_state['segments'])
    if 'text' not in df.columns:
         st.error(get_text(ui_lang, "err_invalid_data"))
    else:
        edit_df = df[['start', 'end', 'text']].copy()
        
        edited_df = st.data_editor(
            edit_df,
            column_config={
                "start": st.column_config.NumberColumn(get_text(ui_lang, "col_start"), format="%.2f"),
                "end": st.column_config.NumberColumn(get_text(ui_lang, "col_end"), format="%.2f"),
                "text": st.column_config.TextColumn(get_text(ui_lang, "col_text"), width="large"),
            },
            num_rows="dynamic",
            use_container_width=True
        )

        st.subheader(get_text(ui_lang, "dl_title"))
        
        if is_pro:
            col1, col2 = st.columns(2)
            with col1:
                srt_content = create_srt_content(edited_df, True)
                st.download_button(
                    label=get_text(ui_lang, "btn_srt"),
                    data=srt_content,
                    file_name="subtitles.srt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col2:
                ass_content = create_ass_content(
                    edited_df, 
                    font_name=font_name,
                    font_size=font_size, 
                    primary_color=ass_primary_color, 
                    outline_color=ass_outline_color, 
                    outline_width=outline_width,
                    alignment=alignment,
                    margin_v=margin_v
                )
                st.download_button(
                    label=get_text(ui_lang, "btn_ass"),
                    data=ass_content,
                    file_name="subtitles.ass",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            srt_content = create_srt_content(edited_df, False)
            st.download_button(
                label=get_text(ui_lang, "btn_srt"),
                data=srt_content,
                file_name="subtitles_free.srt",
                mime="text/plain",
                use_container_width=True
            )
            st.info(get_text(ui_lang, "hint_upgrade"))

st.markdown("---")
st.caption(get_text(ui_lang, "footer"))
