import os
import streamlit as st
from openai import AzureOpenAI

# ---- Azure OpenAI Client ----
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-10-21",
)

MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # summarizer

st.set_page_config(page_title="超かんたん要約メモ", page_icon="📝")
st.title("📝 超かんたん要約メモ（Azure OpenAI）")

# Debug (削除してもOK)
st.caption(f"MODEL: {MODEL}")
st.caption(f"ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")

# 入力UI
src = st.text_area("ここにテキストを貼り付けてください", height=220)

uploaded = st.file_uploader("または .txt ファイルをアップロード", type=["txt"])
if uploaded:
    src = uploaded.read().decode("utf-8")

col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("出力言語", ["日本語", "English"], index=0)
with col2:
    max_bullets = st.slider("要約の箇条書き数", 3, 7, 3)

# 実行
if st.button("要約する", type="primary") and src.strip():
    sys = f"You are a concise assistant. Output in {lang}."
    user = f"Summarize this in {max_bullets} bullet points and give 3 actions & 3 tags:\n\n{src}"

    try:
        rsp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": sys},
                {"role": "user", "content": user},
            ],
            temperature=0.3,
        )
        st.markdown(rsp.choices[0].message.content)

    except Exception as e:
        st.error(f"呼び出しに失敗しました: {str(e)}\n\n"
                 "以下を確認してください：\n"
                 "・デプロイ名（AZURE_OPENAI_DEPLOYMENT）が正しいか\n"
                 "・エンドポイントURLが正しいか\n"
                 "・api-version が最新か（例: 2024-10-21）\n"
        )
