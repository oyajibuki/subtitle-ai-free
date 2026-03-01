import streamlit as st
import os
from translations import get_text

try:
    import stripe
    # Stripe APIキーの設定
    try:
        stripe.api_key = st.secrets["STRIPE_API_KEY"]
    except (KeyError, FileNotFoundError):
        stripe.api_key = os.environ.get("STRIPE_API_KEY", "")
except ImportError:
    stripe = None

def verify_license_key(license_key: str) -> bool:
    """GASのエンドポイントにライセンスキーを検証し、払い済みかチェックする"""
    if not license_key:
        return False
        
    # 特別なテスト用キーを追加 (Stripe設定なしでも通るようにする)
    if license_key == "test_key_123":
        return True
    
    # 形式の簡易チェック (CC-TEST-XXXX-XXXX-XXXX)
    if not license_key.startswith("CC-"):
        # 古いStripeセッションID (`cs_test_...`) の下位互換性対応
        if license_key.startswith("cs_"):
            return _verify_legacy_stripe(license_key)
        return False
    
    # GASの評価
    try:
        import urllib.request
        import json
        
        # デフォルトのGAS URLを設定 (環境変数やSecretsでの上書きも可能)
        default_gas_url = "https://script.google.com/macros/s/AKfycbw-GQUSSCTIbSRLMhaItLX6GZSi0iemw5Vaxo0oKB4Rg9OOf1xJ4UEBJHczY7-3LWPj_Q/exec"
        GAS_URL = os.environ.get("GAS_LICENSE_URL", st.secrets.get("GAS_LICENSE_URL", default_gas_url))
        
        if not GAS_URL:
             st.error("設定エラー: GASの認証URL (GAS_LICENSE_URL) が設定されていません。")
             return False
             
        # GASの doGet にリクエストを送る
        url = f"{GAS_URL}?license_key={license_key}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get("status") == "success" and data.get("valid") is True:
                return True
                
        return False
    except Exception as e:
        print(f"License verification error: {e}")
        return False
        
def _verify_legacy_stripe(session_id: str) -> bool:
    """過去のStripe Session ID用の古いバリデーション"""
    if stripe is None or not stripe.api_key:
        return False
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session and session.payment_status == "paid":
            return True
        return False
    except Exception as e:
        return False

def render_license_ui(lang: str):
    """ライセンスキー入力UIと購入ボタンを表示"""
    
    is_pro = st.session_state.get("is_pro", False)
    
    if is_pro:
        # 解除ボタンは廃止し、認証済みメッセージのみ表示
        st.success("✅ " + get_text(lang, "app_title_pro"))
        return True
    
    # フリーモードの場合のUI
    st.markdown(get_text(lang, "upgrade_title"))
    
    # Stripe購入へのリンクボタン
    buy_link = get_text(lang, "buy_link")
    buy_btn_text = get_text(lang, "buy_button")
    st.link_button(buy_btn_text, buy_link, type="primary")
    
    st.info(get_text(lang, "upgrade_info"))
    
    with st.form("license_form"):
        license_key = st.text_input(get_text(lang, "license_key"), type="password")
        submit_btn = st.form_submit_button(get_text(lang, "auth_btn"))
        
        if submit_btn:
            if verify_license_key(license_key):
                st.session_state["is_pro"] = True
                st.session_state["license_key"] = license_key
                st.success(get_text(lang, "auth_success"))
                st.rerun()
            else:
                st.error(get_text(lang, "auth_failed"))
                 
    return False

def is_pro_mode():
    """現在のセッションがPro版かどうかを返す"""
    return st.session_state.get("is_pro", False)
