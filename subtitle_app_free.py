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

import whisper
import pandas as pd
from datetime import timedelta
from moviepy import VideoFileClip
import streamlit.components.v1 as components

# --- FFmpegのパス設定 (Pro版と同じ) ---
# カレントディレクトリのffmpeg.exeを優先的に使用
os.environ["PATH"] = os.getcwd() + os.pathsep + os.environ["PATH"]

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

def create_srt_content(df):
    """データフレームからSRT形式の文字列を生成"""
    # 無料版用の透かし広告を先頭に強制追加
    srt_content = "1\n00:00:00,000 --> 00:00:05,000\n[Created by AI Subtitle Free]\n\n"
    
    for idx, row in df.iterrows():
        start = format_timestamp(row['start'])
        end = format_timestamp(row['end'])
        text = row['text']
        # 連番を+2する（1番目は透かし用）
        srt_content += f"{idx + 2}\n{start} --> {end}\n{text}\n\n"
    return srt_content

def save_uploaded_file(uploaded_file):
    """アップロードされたファイルを一時ファイルとして保存"""
    try:
        temp_dir = os.path.join(os.getcwd(), "temp_files")
        os.makedirs(temp_dir, exist_ok=True)
        
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"ファイル保存エラー: {e}")
        return None

def get_video_duration(file_path):
    """動画/音声ファイルの長さを取得 (秒)"""
    try:
        # moviepyを使って長さを取得
        with VideoFileClip(file_path) as clip:
            return clip.duration
    except Exception as e:
        # 音声ファイルなどVideoFileClipで開けない場合のフォールバックは省略(簡易実装)
        return 0

# --- モデル読み込み (キャッシュ化) ---
@st.cache_resource
def load_model(model_size):
    return whisper.load_model(model_size)

# --- アプリケーション本体 ---

st.set_page_config(page_title="AIテロップ自動生成ツール (Free Edition)", layout="centered")

st.title("🎥 AIテロップ自動生成ツール\n(Free Edition)")
st.info("これは**無料体験版**です。機能制限があります。[Pro版へのお問い合わせはこちら](https://oyajibuki.github.io/form/)")

st.markdown("""
### ⚠️ 制限事項
- **動画の長さ**: 5分 (300秒) まで
- **ファイルサイズ**: 100MB まで
- **AIモデル**: tiny, base のみ
- **出力形式**: SRT (字幕ファイル) のみ
""")

# サイドバー設定
with st.sidebar:
    st.header("⚙️ 音声認識設定")
    # Free版は tiny, base のみ
    model_map = {
        "tiny (最軽量)": "tiny",
        "base (標準)": "base"
    }
    model_label = st.selectbox(
        "AIモデルサイズ",
        list(model_map.keys()),
        index=1,
        help="""
        - tiny (最軽量): 最軽量・最速。精度は低め。
        - base (標準): 標準的な速度と精度。
        
        ※Free版ではSmart/Proモデルは選択できません。
        """
    )
    model_size = model_map[model_label]
    
    language = st.selectbox("言語", ["Japanese", "English"], index=0)
    lang_code = "ja" if language == "Japanese" else "en"

    st.divider()
    st.caption("🔒 Pro版機能")
    st.markdown("""
    - 高精度モデル (Smart/Pro)
    - フォント/色などのスタイル編集
    - ASS形式 (派手な字幕) 出力
    - 動画の長さ・サイズ無制限
    """)

    st.divider()
    
    # ---------------------------
    # GAS Visitor Counter
    # ---------------------------
    # セッション内で1回だけカウントアップ＆取得
    if 'visitor_count' not in st.session_state:
        try:
            import urllib.request
            import json
            # ユーザー提供のGAS URL
            url = "https://script.google.com/macros/s/AKfycbznxYkj5ixnK_pHkGR8LUYhEYdvSYpaiF3x4LaZy964wlu068oak1X1uuIiyqCEtGWF/exec?page=subtitle-ai-free"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                st.session_state['visitor_count'] = data['count']
        except Exception:
            st.session_state['visitor_count'] = None

    if st.session_state['visitor_count'] is not None:
        st.caption(f"👀 Visitors: {st.session_state['visitor_count']}")

# メインエリア
# メインエリア


# ファイルアップローダーの「Limit ...」表記を消すJS (DOM全探索・強力版)
components.html(
    """
    <script>
    function hideLimitText() {
        // 全要素を対象に検索
        const elements = window.parent.document.querySelectorAll('*');
        elements.forEach(el => {
            // タグに関係なく、中身に "Limit" かつ "GB" か "MB" が含まれていたら消す
            // ただし body や html は消さない
            if (el.tagName !== 'BODY' && el.tagName !== 'HTML' && el.children.length === 0) {
                 if (el.textContent && (el.textContent.includes('Limit') && (el.textContent.includes('MB') || el.textContent.includes('GB')))) {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                    el.innerHTML = ''; // 中身も空にする
                }
            }
        });
        
        // 特定のクラス構造に対しても念のためCSS操作
        const uploaders = window.parent.document.querySelectorAll('[data-testid="stFileUploader"] small');
        uploaders.forEach(el => el.style.display = 'none');
    }
    // 初回実行
    hideLimitText();
    // 0.5秒ごとに監視
    setInterval(hideLimitText, 500);
    </script>
    """,
    height=0,
    width=0
)

# CSSバックアップ (多重指定) と ウォーターマークの追加
st.markdown(
    """
    <style>
    /* 画面全体に斜めのウォーターマークを表示 */
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
    
    /* 小さい文字をとにかく消す */
    [data-testid="stFileUploader"] small {
        display: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
        font-size: 0 !important;
    }
    /* 親要素の構造ごと消す試み */
    [data-testid="stFileUploader"] section > div > div > small {
        display: none !important;
    }
    /* テキストを含むspanの可能性 */
    [data-testid="stFileUploader"] span {
        font-size: 14px !important; /* 通常テキスト用 */
    }
    </style>
    <div class="watermark-bg">Created by AI Subtitle Free</div>
    """,
    unsafe_allow_html=True
)

st.caption("対応形式: mp4, mov, wav, mp3, m4a, mk4")
uploaded_file = st.file_uploader("動画または音声ファイルをドラッグ＆ドロップ (5分以内 / 100MBまで)", type=["mp4", "mov", "wav", "mp3", "m4a", "mk4"])

if uploaded_file is not None:
    # サイズチェック (100MB)
    if uploaded_file.size > 100 * 1024 * 1024:
        st.error("⚠️ ファイルサイズが制限 (100MB) を超えています。\nFree版では100MB以下のファイルのみ利用可能です。")
    else:
        temp_file_path = save_uploaded_file(uploaded_file)
    
    if temp_file_path:
        # 動画プレビュー
        st.markdown("### 確認用プレビュー")
        # プレビュー画面を小さく表示するためにカラム分割を使用
        col_preview, col_empty = st.columns([1, 2])
        with col_preview:
            if any(ext in uploaded_file.name for ext in ["mp4", "mov"]):
                st.video(temp_file_path)
            else:
                st.audio(temp_file_path)

        st.markdown("### 文字起こし開始")
        
        # 長さチェック
        duration = get_video_duration(temp_file_path)
        if duration > 300: # 5分 = 300秒
            st.error(f"⚠️ 動画の長さが制限を超えています ({int(duration)}秒)。\nFree版では5分 (300秒) 以内の動画のみ処理可能です。")
        else:
            # 文字起こし実行ボタン
            if st.button("🚀 文字起こし開始 (Free)", type="primary"):
                with st.spinner(f"{model_size}モデルで解析中..."):
                    try:
                        model = load_model(model_size)
                        result = model.transcribe(temp_file_path, language=lang_code)
                        
                        st.session_state['free_segments'] = result['segments']
                        st.success("文字起こし完了！")
                    except Exception as e:
                        st.error(f"エラーが発生しました: {e}")

# 結果表示と編集エリア
if 'free_segments' in st.session_state:
    st.divider()
    st.header("📝 字幕データの確認")
    
    df = pd.DataFrame(st.session_state['free_segments'])
    if 'text' not in df.columns:
         st.error("データが不正です。")
    else:
        # Free版は簡易編集のみ提供 (DataEditorは使えるようにしておく)
        edit_df = df[['start', 'end', 'text']].copy()
        
        edited_df = st.data_editor(
            edit_df,
            column_config={
                "start": st.column_config.NumberColumn("開始", format="%.2f"),
                "end": st.column_config.NumberColumn("終了", format="%.2f"),
                "text": st.column_config.TextColumn("内容", width="large"),
            },
            num_rows="dynamic",
            use_container_width=True
        )

        st.subheader("📥 ダウンロード")
        srt_content = create_srt_content(edited_df)
        
        st.download_button(
            label="SRTファイルを保存",
            data=srt_content,
            file_name="subtitles_free.srt",
            mime="text/plain",
            use_container_width=True
        )
        
        st.info("💡 ヒント: ASS形式での出力や詳細なスタイル設定を行いたい場合は Pro版 をご利用ください。")
