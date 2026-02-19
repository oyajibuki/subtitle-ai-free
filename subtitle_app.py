import streamlit as st
import whisper
import os
from datetime import timedelta
import pandas as pd

# --- 設定とユーティリティ関数 ---

def format_timestamp(seconds):
    """秒数をSRT形式のタイムスタンプ (HH:MM:SS,mmm) に変換"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def format_timestamp_ass(seconds):
    """秒数をASS形式のタイムスタンプ (H:MM:SS.cc) に変換"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    centis = int(td.microseconds / 10000)
    return f"{hours}:{minutes:02}:{secs:02}.{centis:02}"

def create_srt_content(df):
    """データフレームからSRT形式の文字列を生成"""
    srt_content = ""
    for idx, row in df.iterrows():
        start = format_timestamp(row['start'])
        end = format_timestamp(row['end'])
        text = row['text']
        srt_content += f"{idx + 1}\n{start} --> {end}\n{text}\n\n"
    return srt_content

def create_ass_content(df, font_name="MS Gothic", font_size=40, primary_color="&H00FFFFFF", outline_color="&H00000000", outline_width=2, shadow_depth=0, alignment=2, margin_v=10):
    """データフレームからASS形式の文字列を生成"""
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
    """WEB色(#RRGGBB)をASS色(&HAABBGGRR)に変換。アルファは00(不透明)とする"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return "&H00FFFFFF"
    r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
    return f"&H00{b}{g}{r}".upper()

def save_uploaded_file(uploaded_file):
    """アップロードされたファイルを一時ファイルとして保存"""
    start_dir = os.getcwd()
    try:
        # 現在のディレクトリに一時フォルダを作成（確実にアクセス可能な場所）
        temp_dir = os.path.join(os.getcwd(), "temp_files")
        os.makedirs(temp_dir, exist_ok=True)
        
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"ファイル保存エラー: {e}")
        return None

# --- モデル読み込み (キャッシュ化) ---
@st.cache_resource
def load_model(model_size):
    """Whisperモデルをロード"""
    return whisper.load_model(model_size)

# --- アプリケーション本体 ---

st.set_page_config(page_title="AIテロップ自動生成ツール", layout="wide")

st.title("🎥 AIテロップ自動生成ツール (Pro版)")
st.markdown("""
動画や音声ファイルをアップロードすると、AI (Whisper) が文字起こしを行い、SRT/ASS字幕を生成します。  
テキストの微修正や、スタイル設定を行い、ダウンロード可能です。
""")

# サイドバー設定
with st.sidebar:
    st.header("⚙️ 音声認識設定")
    # モデル名の表示名と実体名のマッピング
    model_map = {
        "tiny (最軽量)": "tiny",
        "base (標準)": "base",
        "smart (バランス良)": "small",
        "Pro (高精度)": "medium"
    }
    
    model_label = st.selectbox(
        "AIモデルサイズ",
        list(model_map.keys()),
        index=2,
        help="""
        - tiny (最軽量): とにかく早い。動作確認用。
        - base (標準): 一般的な用途向け。
        - smart (バランス良): 精度と速度のバランスが良い (推奨)。
        - Pro (高精度): 非常に高精度だが、処理が重い。
        """
    )
    model_size = model_map[model_label]
    
    language = st.selectbox("言語", ["Japanese", "English"], index=0)
    lang_code = "ja" if language == "Japanese" else "en"

    st.divider()
    
    st.header("🎨 テロップスタイル")
    st.caption("動画に焼き込む字幕のデザインを設定します。 ※ ASS用")
    
    font_map = {
        "MS Gothic (標準)": "MS Gothic",
        "MS Mincho (明朝体)": "MS Mincho",
        "Meiryo (メイリオ)": "Meiryo",
        "Yu Gothic (游ゴシック)": "Yu Gothic",
        "Arial (英数字向け)": "Arial"
    }
    
    font_label = st.selectbox(
        "フォント選択",
        list(font_map.keys()),
        index=0,
        help="Windowsに標準インストールされているフォントです。\n日本語動画には日本語対応フォント(Gothic/Mincho/Meiryo/Yu Gothic)を選んでください。"
    )
    st.markdown("---") # 区切り線で見やすく
    font_name = font_map[font_label]
    font_size = st.slider("フォントサイズ", 10, 100, 40)
    font_color_hex = st.color_picker("文字色", "#FFFFFF")
    outline_width = st.slider("縁取りの太さ", 0, 10, 2)
    outline_color_hex = st.color_picker("縁取り色", "#000000")
    
    alignment_map = {"下中央": 2, "中中央": 5, "上中央": 8}
    position_label = st.selectbox("位置", list(alignment_map.keys()), index=0)
    alignment = alignment_map[position_label]
    
    margin_v = st.slider("垂直マージン", 0, 200, 20, help="字幕を画面端からどれくらい離すか。\n数値が大きいほど画面中央に寄ります (浮きます)。")
    
    # ASS用の色変換
    ass_primary_color = hex_to_ass_color(font_color_hex)
    ass_outline_color = hex_to_ass_color(outline_color_hex)

# メインエリア
st.caption("対応形式: mp4, mov, wav, mp3, m4a, mk4")
uploaded_file = st.file_uploader("動画または音声ファイルをドラッグ＆ドロップ", type=["mp4", "mov", "wav", "mp3", "m4a", "mk4"])

if uploaded_file is not None:
    # 一時保存
    temp_file_path = save_uploaded_file(uploaded_file)
    
    if temp_file_path:
        st.video(temp_file_path) if any(ext in uploaded_file.name for ext in ["mp4", "mov"]) else st.audio(temp_file_path)
        
        # 文字起こし実行ボタン
        if st.button("🚀 文字起こし開始", type="primary"):
            with st.spinner(f"{model_size}モデルで解析中... (GPU: {'有効' if whisper.torch.cuda.is_available() else '無効'})"):
                try:
                    model = load_model(model_size)
                    result = model.transcribe(temp_file_path, language=lang_code)
                    
                    # 結果をSession Stateに保存
                    st.session_state['segments'] = result['segments']
                    st.session_state['file_path'] = temp_file_path
                    st.success("文字起こし完了！")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

# 結果表示と編集エリア
if 'segments' in st.session_state:
    st.divider()
    st.header("📝 字幕データの編集")
    
    # データをDataFrameに変換
    df = pd.DataFrame(st.session_state['segments'])
    if 'text' not in df.columns:
         st.error("セグメントデータが不正です。")
    else:
        edit_df = df[['start', 'end', 'text']].copy()
        
        edited_df = st.data_editor(
            edit_df,
            column_config={
                "start": st.column_config.NumberColumn("開始時間 (秒)", format="%.2f"),
                "end": st.column_config.NumberColumn("終了時間 (秒)", format="%.2f"),
                "text": st.column_config.TextColumn("テロップ内容", width="large"),
            },
            num_rows="dynamic",
            use_container_width=True
        )

        st.subheader("📥 ファイルダウンロード")
        
        col1, col2 = st.columns(2)
        with col1:
            # SRT生成
            srt_content = create_srt_content(edited_df)
            st.download_button(
                label="SRT形式 (.srt) を保存",
                data=srt_content,
                file_name="subtitles.srt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            # ASS生成
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
                label="ASS形式 (.ass) を保存",
                data=ass_content,
                file_name="subtitles.ass",
                mime="text/plain",
                use_container_width=True
            )

# フッター
st.markdown("---")
st.caption("Powered by OpenAI Whisper | Created with Streamlit")
