from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

st.title("ちょこっとマネー相談室")
st.subheader("日常のちょっとしたお金の悩みを解決します。相談内容を選んでください。")
selected_item = st.radio(
    "相談内容を選んでください。",
    ["A: お金を増やしたい", "B: お金を節約したい"]
)

system_prompts = {
    "A": "あなたは経験豊富なファイナンシャルプランナーです。投資・保険・ライフプランなど資産形成の観点から、分かりやすく具体的に理由も添えて400字以内に簡潔にアドバイスしてください。",
    "B": "あなたは生活費の節約に詳しいアドバイザーです。日常生活の工夫やコスト削減の方法を中心に、分かりやすく具体的に理由も添えて400字以内に簡潔にアドバイスしてください。"
}

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

def get_advice(choice: str, user_question: str):
    system_message = SystemMessage(content=system_prompts[choice])
    human_message = HumanMessage(content=user_question)
    response = llm([system_message, human_message])
    return response.content

choice = selected_item.split(":")[0]

if choice == "A":
    st.info("【ファイナンシャルプランナー】に相談中できます。投資や保険、資産形成のことを質問してください。")
    user_question = st.text_area("相談内容を100字以内で入力してください。", height=100)
elif choice == "B":
    st.info("【節約アドバイザー】に相談中できます。日常の節約術やコストカットについて質問してください。")
    user_question = st.text_area("相談内容を100字以内で入力してください。", height=100)
else:
    st.warning("選択が正しくありません。")
    user_question = ""

if st.button("アドバイスをもらう"):
    if user_question.strip() == "":
        st.warning("質問を入力してください！")
    else:
        try:
            answer = get_advice(choice, user_question)
            st.divider()
            st.subheader("🔎 回答")
            st.write(answer)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")