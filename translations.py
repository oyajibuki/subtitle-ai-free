TRANSLATIONS = {
    "ja": {
        "app_title_pro": "🎥 AIテロップ自動生成ツール (Pro版)",
        "app_title_free": "🎥 AIテロップ自動生成ツール (Free版)",
        "pro_desc": "制限なしでAI文字起こし・SRT/ASS字幕生成をご利用いただけます。",
        "free_desc": "これは無料体験モードです。制限なしの利用にはライセンスキーの認証が必要です。",
        "free_limits_title": "### ⚠️ Free版の制限事項",
        "free_limits": """
- **動画の長さ**: 5分 (300秒) まで
- **ファイルサイズ**: 100MB まで
- **AIモデル**: tiny, base のみ
- **出力形式**: SRT形式 のみ
- **透かし**: 画面上にのみ表示されます
""",
        "upgrade_title": "### 🔑 Pro版にアップグレード",
        "upgrade_info": "決済時に発行された **ライセンスキー (`cs_test_...` 等)** を入力してください。",
        "buy_button": "💳 StripeでPro版を購入する",
        "buy_link": "https://buy.stripe.com/8x228reod43s84pgTrcjS02",
        "license_key": "ライセンスキー",
        "auth_btn": "認証する",
        "auth_success": "🎉 認証成功！Pro版の機能が利用可能になりました。",
        "auth_failed": "無効なライセンスキーです。キーをご確認ください。",
        "auth_no_key": "Stripe APIキーが設定されていません。アプリの管理画面で設定してください。",
        "settings_title": "⚙️ 音声認識設定",
        "model_label": "AIモデルサイズ",
        "model_help_pro": "ProモデルなどはPro版で利用可能です。",
        "lang_label": "音声の言語",
        "lang_ja": "日本語",
        "lang_en": "英語",
        "lang_zh": "中国語",
        "lang_ko": "韓国語",
        "lang_pt": "ポルトガル語",
        "style_title": "🎨 テロップスタイル",
        "style_desc": "動画に焼き込む字幕のデザインを設定します。 ※ ASS用",
        "font_label": "フォント選択",
        "font_size": "フォントサイズ",
        "font_color": "文字色",
        "outline_width": "縁取りの太さ",
        "outline_color": "縁取り色",
        "position": "位置",
        "margin_v": "垂直マージン",
        "pro_features_title": "🔒 Pro版機能",
        "pro_features": """
- 高精度モデル (Smart/Pro)
- フォント/色などのスタイル編集
- ASS形式 (派手な字幕) 出力
- 動画の長さ・サイズ無制限
""",
        "upload_label_free": "動画または音声ファイルをドラッグ＆ドロップ (5分以内 / 100MBまで)",
        "upload_label_pro": "動画または音声ファイルをドラッグ＆ドロップ",
        "supported_formats": "対応形式: mp4, mov, wav, mp3, m4a, mk4",
        "err_size": "⚠️ ファイルサイズが制限 (100MB) を超えています。\nFree版では100MB以下のファイルのみ利用可能です。",
        "preview": "### 確認用プレビュー",
        "err_duration": "⚠️ 動画の長さが制限を超えています ({sec}秒)。\nFree版では5分 (300秒) 以内の動画のみ処理可能です。",
        "btn_start": "🚀 文字起こし開始",
        "sp_analyzing": "{model}モデルで解析中... (GPU: {gpu})",
        "msg_complete": "文字起こし完了！",
        "err_analysis": "エラーが発生しました: {e}",
        "edit_title": "📝 字幕データの編集",
        "err_invalid_data": "セグメントデータが不正です。",
        "col_start": "開始時間 (秒)",
        "col_end": "終了時間 (秒)",
        "col_text": "テロップ内容",
        "dl_title": "📥 ファイルダウンロード",
        "btn_srt": "SRT形式 (.srt) を保存",
        "btn_ass": "ASS形式 (.ass) を保存",
        "hint_upgrade": "💡 ヒント: ASS形式での出力や詳細なスタイル設定を行いたい場合は Pro版 にアップグレードしてください。",
        "footer": "Powered by OpenAI Whisper | Created with Streamlit"
    },
    "en": {
        "app_title_pro": "🎥 AI Subtitle Generator (Pro)",
        "app_title_free": "🎥 AI Subtitle Generator (Free)",
        "pro_desc": "Enjoy unlimited AI transcription and SRT/ASS subtitle generation.",
        "free_desc": "This is the Free mode. Enter a License Key to unlock unlimited usage.",
        "free_limits_title": "### ⚠️ Free Version Limits",
        "free_limits": """
- **Video duration**: Up to 5 minutes (300 sec)
- **File size**: Up to 100MB
- **AI Models**: tiny, base only
- **Output format**: SRT only
- **Watermark**: Displayed only on the UI screen
""",
        "upgrade_title": "### 🔑 Upgrade to Pro",
        "upgrade_info": "Please enter the **License Key (`cs_test_...` etc.)** issued after payment.",
        "buy_button": "💳 Purchase Pro via Stripe",
        "buy_link": "https://buy.stripe.com/8x228reod43s84pgTrcjS02",
        "license_key": "License Key",
        "auth_btn": "Authenticate",
        "auth_success": "🎉 Authentication successful! Pro features are now unlocked.",
        "auth_failed": "Invalid License Key. Please check the key and try again.",
        "auth_no_key": "Stripe API key is not configured.",
        "settings_title": "⚙️ Speech Recognition Settings",
        "model_label": "AI Model Size",
        "model_help_pro": "Pro models are available in the Pro version.",
        "lang_label": "Audio Language",
        "lang_ja": "Japanese",
        "lang_en": "English",
        "lang_zh": "Chinese",
        "lang_ko": "Korean",
        "lang_pt": "Portuguese",
        "style_title": "🎨 Subtitle Style",
        "style_desc": "Configure the design of subtitles to burn into video. ※ For ASS format",
        "font_label": "Font",
        "font_size": "Font Size",
        "font_color": "Font Color",
        "outline_width": "Outline Width",
        "outline_color": "Outline Color",
        "position": "Position",
        "margin_v": "Vertical Margin",
        "pro_features_title": "🔒 Pro Features",
        "pro_features": """
- High accuracy models (Smart/Pro)
- Subtitle style editing (fonts/colors)
- ASS format (Styled subtitles) output
- Unlimited video length and size
""",
        "upload_label_free": "Drag & drop a video or audio file (Under 5 mins / up to 100MB)",
        "upload_label_pro": "Drag & drop a video or audio file",
        "supported_formats": "Supported formats: mp4, mov, wav, mp3, m4a, mk4",
        "err_size": "⚠️ File size limit (100MB) exceeded.\nFree mode only allows files under 100MB.",
        "preview": "### Preview",
        "err_duration": "⚠️ Video length limit exceeded ({sec} sec).\nFree mode only processes videos up to 5 minutes (300 sec).",
        "btn_start": "🚀 Start Transcription",
        "sp_analyzing": "Analyzing with {model} model... (GPU: {gpu})",
        "msg_complete": "Transcription complete!",
        "err_analysis": "An error occurred: {e}",
        "edit_title": "📝 Edit Subtitle Data",
        "err_invalid_data": "Invalid segment data.",
        "col_start": "Start Time (sec)",
        "col_end": "End Time (sec)",
        "col_text": "Subtitle Text",
        "dl_title": "📥 Download Files",
        "btn_srt": "Save as SRT (.srt)",
        "btn_ass": "Save as ASS (.ass)",
        "hint_upgrade": "💡 Hint: Upgrade to Pro to output in ASS format and customize styles.",
        "footer": "Powered by OpenAI Whisper | Created with Streamlit"
    },
    "zh": {
        "app_title_pro": "🎥 AI 自动字幕生成器 (Pro版)",
        "app_title_free": "🎥 AI 自动字幕生成器 (免费版)",
        "pro_desc": "无限制使用 AI 语音转码及 SRT/ASS 字幕生成功能。",
        "free_desc": "这是免费体验模式。请输入许可证密钥解锁无限制使用。",
        "free_limits_title": "### ⚠️ 免费版限制",
        "free_limits": """
- **视频时长**: 最多 5 分钟 (300 秒)
- **文件大小**: 最多 100MB
- **AI模型**: 仅限 tiny, base
- **输出格式**: 仅限 SRT
- **水印**: 仅显示在界面上
""",
        "upgrade_title": "### 🔑 升级到 Pro 版",
        "upgrade_info": "请输入支付后收到的 **许可证密钥 (`cs_test_...` 等)**。",
        "buy_button": "💳 通过 Stripe 购买 Pro 版",
        "buy_link": "https://buy.stripe.com/8x228reod43s84pgTrcjS02",
        "license_key": "许可证密钥",
        "auth_btn": "验证",
        "auth_success": "🎉 验证成功！Pro 版功能已解锁。",
        "auth_failed": "无效的许可证密钥。请检查密钥后重试。",
        "auth_no_key": "未配置 Stripe API 密钥。",
        "settings_title": "⚙️ 语音识别设置",
        "model_label": "AI 模型大小",
        "model_help_pro": "Pro 版可使用 Pro 模型。",
        "lang_label": "音频语言",
        "lang_ja": "日语",
        "lang_en": "英语",
        "lang_zh": "中文",
        "lang_ko": "韩语",
        "lang_pt": "葡萄牙语",
        "style_title": "🎨 字幕样式",
        "style_desc": "配置烧制到视频中的字幕设计。 ※ 适用于 ASS 格式",
        "font_label": "字体",
        "font_size": "字体大小",
        "font_color": "字体颜色",
        "outline_width": "描边宽度",
        "outline_color": "描边颜色",
        "position": "位置",
        "margin_v": "垂直边距",
        "pro_features_title": "🔒 Pro 版功能",
        "pro_features": """
- 高精度模型 (Smart/Pro)
- 字幕样式编辑 (字体/颜色)
- ASS 格式 (带样式的字幕) 输出
- 无限制视频时长和大小
""",
        "upload_label_free": "拖拽视频或音频文件 (5 分钟以内 / 100MB以内)",
        "upload_label_pro": "拖拽视频或音频文件",
        "supported_formats": "支持的格式: mp4, mov, wav, mp3, m4a, mk4",
        "err_size": "⚠️ 文件大小超出限制 (100MB)。\n免费版仅支持 100MB 以下的文件。",
        "preview": "### 预览",
        "err_duration": "⚠️ 视频时长超出限制 ({sec} 秒)。\n免费版仅处理 5 分钟 (300 秒) 以内的视频。",
        "btn_start": "🚀 开始转写",
        "sp_analyzing": "正在使用 {model} 模型分析... (GPU: {gpu})",
        "msg_complete": "转写完成！",
        "err_analysis": "发生错误: {e}",
        "edit_title": "📝 编辑字幕数据",
        "err_invalid_data": "无效的片段数据。",
        "col_start": "开始时间 (秒)",
        "col_end": "结束时间 (秒)",
        "col_text": "字幕文本",
        "dl_title": "📥 下载文件",
        "btn_srt": "保存为 SRT (.srt)",
        "btn_ass": "保存为 ASS (.ass)",
        "hint_upgrade": "💡 提示：升级到 Pro 版可导出 ASS 格式并自定义样式。",
        "footer": "Powered by OpenAI Whisper | Created with Streamlit"
    },
    "pt": {
        "app_title_pro": "🎥 Gerador de Legendas por IA (Pro)",
        "app_title_free": "🎥 Gerador de Legendas por IA (Grátis)",
        "pro_desc": "Aproveite transcrição ilimitada por IA e geração de legendas SRT/ASS.",
        "free_desc": "Este é o modo gratuito. Insira uma Chave de Licença para desbloquear o uso ilimitado.",
        "free_limits_title": "### ⚠️ Limites da Versão Gratuita",
        "free_limits": """
- **Duração do vídeo**: Até 5 minutos (300 seg)
- **Tamanho do arquivo**: Até 100MB
- **Modelos de IA**: apenas tiny, base
- **Formato de saída**: apenas SRT
- **Marca d'água**: Exibida apenas na interface
""",
        "upgrade_title": "### 🔑 Atualizar para o Pro",
        "upgrade_info": "Por favor, insira a **Chave de Licença (`cs_test_...` etc.)** emitida após o pagamento.",
        "buy_button": "💳 Comprar Pro via Stripe",
        "buy_link": "https://buy.stripe.com/8x228reod43s84pgTrcjS02",
        "license_key": "Chave de Licença",
        "auth_btn": "Autenticar",
        "auth_success": "🎉 Autenticação bem-sucedida! Agora as funções Pro estão desbloqueadas.",
        "auth_failed": "Chave de Licença inválida. Por favor, verifique a chave e tente novamente.",
        "auth_no_key": "A chave da API do Stripe não está configurada.",
        "settings_title": "⚙️ Configurações de Reconhecimento de Voz",
        "model_label": "Tamanho do Modelo de IA",
        "model_help_pro": "Modelos Pro estão disponíveis na versão Pro.",
        "lang_label": "Idioma do Áudio",
        "lang_ja": "Japonês",
        "lang_en": "Inglês",
        "lang_zh": "Chinês",
        "lang_ko": "Coreano",
        "lang_pt": "Português",
        "style_title": "🎨 Estilo da Legenda",
        "style_desc": "Configure o design das legendas a serem gravadas no vídeo. ※ Para formato ASS",
        "font_label": "Fonte",
        "font_size": "Tamanho da Fonte",
        "font_color": "Cor da Fonte",
        "outline_width": "Largura da Borda",
        "outline_color": "Cor da Borda",
        "position": "Posição",
        "margin_v": "Margem Vertical",
        "pro_features_title": "🔒 Funções Pro",
        "pro_features": """
- Modelos de alta precisão (Smart/Pro)
- Edição de estilo de legenda (fontes/cores)
- Saída em formato ASS (legendas estilizadas)
- Duração e tamanho de vídeo ilimitados
""",
        "upload_label_free": "Arraste e solte um arquivo de vídeo ou áudio (Menos de 5 min / até 100MB)",
        "upload_label_pro": "Arraste e solte um arquivo de vídeo ou áudio",
        "supported_formats": "Formatos suportados: mp4, mov, wav, mp3, m4a, mk4",
        "err_size": "⚠️ O limite de tamanho do arquivo foi excedido (100MB).\nO modo gratuito só permite arquivos de até 100MB.",
        "preview": "### Visualização",
        "err_duration": "⚠️ O limite de duração do vídeo foi excedido ({sec} seg).\nO modo gratuito só processa vídeos de até 5 minutos (300 seg).",
        "btn_start": "🚀 Iniciar Transcrição",
        "sp_analyzing": "Analisando com o modelo {model}... (GPU: {gpu})",
        "msg_complete": "Transcrição concluída!",
        "err_analysis": "Ocorreu um erro: {e}",
        "edit_title": "📝 Editar Dados da Legenda",
        "err_invalid_data": "Dados de segmento inválidos.",
        "col_start": "Hora de Início (seg)",
        "col_end": "Hora de Término (seg)",
        "col_text": "Texto da Legenda",
        "dl_title": "📥 Baixar Arquivos",
        "btn_srt": "Salvar como SRT (.srt)",
        "btn_ass": "Salvar como ASS (.ass)",
        "hint_upgrade": "💡 Dica: Atualize para o Pro para gerar no formato ASS e personalizar estilos.",
        "footer": "Powered by OpenAI Whisper | Created with Streamlit"
    },
    "ko": {
        "app_title_pro": "🎥 AI 자동 자막 생성기 (Pro)",
        "app_title_free": "🎥 AI 자동 자막 생성기 (무료)",
        "pro_desc": "제한 없이 AI 전사 및 SRT/ASS 자막 생성 기능을 즐기세요.",
        "free_desc": "무료 체험 모드입니다. 무제한 사용을 위해 라이선스 키를 입력하세요.",
        "free_limits_title": "### ⚠️ 무료 버전 제한 안내",
        "free_limits": """
- **동영상 길이**: 최대 5분 (300초)
- **파일 크기**: 최대 100MB
- **AI 모델**: tiny, base 전용
- **출력 형식**: SRT 전용
- **워터마크**: 화면상에만 표시됩니다
""",
        "upgrade_title": "### 🔑 Pro 버전 업그레이드",
        "upgrade_info": "결제 후 발급된 **라이선스 키 (`cs_test_...` 등)** 를 입력해 주세요.",
        "buy_button": "💳 Stripe로 Pro 버전 구매하기",
        "buy_link": "https://buy.stripe.com/8x228reod43s84pgTrcjS02",
        "license_key": "라이선스 키",
        "auth_btn": "인증하기",
        "auth_success": "🎉 인증 성공! 이제 Pro 기능을 사용할 수 있습니다.",
        "auth_failed": "유효하지 않은 라이선스 키입니다. 키를 확인하고 다시 시도해 주세요.",
        "auth_no_key": "Stripe API 키가 설정되지 않았습니다.",
        "settings_title": "⚙️ 음성 인식 설정",
        "model_label": "AI 모델 크기",
        "model_help_pro": "Pro 버전에서는 Pro 모델을 사용할 수 있습니다.",
        "lang_label": "오디오 언어",
        "lang_ja": "일본어",
        "lang_en": "영어",
        "lang_zh": "중국어",
        "lang_ko": "한국어",
        "lang_pt": "포르투갈어",
        "style_title": "🎨 자막 스타일",
        "style_desc": "동영상에 입힐 자막의 디자인을 설정합니다. ※ ASS 형식 전용",
        "font_label": "폰트",
        "font_size": "폰트 크기",
        "font_color": "폰트 색상",
        "outline_width": "테두리 두께",
        "outline_color": "테두리 색상",
        "position": "위치",
        "margin_v": "세로 여백",
        "pro_features_title": "🔒 Pro 기능",
        "pro_features": """
- 고정밀 모델 (Smart/Pro)
- 자막 스타일 편집 (폰트/색상 등)
- ASS 형식 (스타일 자막) 출력
- 동영상 길이 및 크기 무제한
""",
        "upload_label_free": "동영상 또는 오디오 파일 드래그 & 드롭 (5분 이내 / 최대 100MB)",
        "upload_label_pro": "동영상 또는 오디오 파일 드래그 & 드롭",
        "supported_formats": "지원 형식: mp4, mov, wav, mp3, m4a, mk4",
        "err_size": "⚠️ 파일 크기 제한 (100MB) 초과.\n무료 모드에서는 100MB 이하의 파일만 사용할 수 있습니다.",
        "preview": "### 미리보기",
        "err_duration": "⚠️ 동영상 길이 제한 초과 ({sec} 초).\n무료 모드에서는 최대 5분 (300초) 이내의 동영상만 처리합니다.",
        "btn_start": "🚀 전사 시작",
        "sp_analyzing": "{model} 모델로 분석 중... (GPU: {gpu})",
        "msg_complete": "전사 완료!",
        "err_analysis": "오류가 발생했습니다: {e}",
        "edit_title": "📝 자막 데이터 편집",
        "err_invalid_data": "잘못된 세그먼트 데이터입니다.",
        "col_start": "시작 시간 (초)",
        "col_end": "종료 시간 (초)",
        "col_text": "자막 텍스트",
        "dl_title": "📥 파일 다운로드",
        "btn_srt": "SRT 파일로 저장 (.srt)",
        "btn_ass": "ASS 파일로 저장 (.ass)",
        "hint_upgrade": "💡 팁: ASS 형식으로 출력하고 스타일을 사용자 지정하려면 Pro 버전으로 업그레이드하세요.",
        "footer": "Powered by OpenAI Whisper | Created with Streamlit"
    },
}

def get_text(lang: str, key: str, **kwargs) -> str:
    """Gets the translated text for a given key and language. Formats with kwargs if provided."""
    # Fallback to English if language or key is missing
    target_lang = lang if lang in TRANSLATIONS else "en"
    text = TRANSLATIONS[target_lang].get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text
