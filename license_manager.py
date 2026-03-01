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

def verify_license_key(session_id: str) -> bool:
    """StripeのCheckout Session IDを検証し、支払い済みかチェックする"""
    if not session_id:
        return False
        
    # 特別なテスト用キーを追加 (Stripe設定なしでも通るようにする)
    if session_id == "test_key_123":
        return True
    
    if not session_id.startswith("cs_"):
        return False
    
    # 実際のStripeチェック
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
                if not stripe.api_key and license_key != "test_key_123":
                    st.error(get_text(lang, "auth_no_key"))
                else:
                    st.error(get_text(lang, "auth_failed"))
                 
    return False

def is_pro_mode():
    """現在のセッションがPro版かどうかを返す"""
    return st.session_state.get("is_pro", False)
