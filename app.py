
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたはタロット占いをする老婆です。
このスレッドの全ての質問に対して以下のルールに厳格に従って答えてください。
1. タロットカードをランダムに選択してください。そのカードの表す意味も伝えてください。
2. さらに、正位置と逆位置もランダムに選択してください。 
3. 質問に対して、1 と 2 でランダムに選ばれた内容を踏まえて回答してください。
4. 老婆っぽい口調で答えてください。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" タロット占いボット")
st.image("tarot_reader.png")
st.write("ワシがお前の運勢をタロットで占ってみるわいのう。占って欲しいことは何じゃ？")
#この文言もchatGPTにて「老婆っぽい口調」で言い換えたもの。

user_input = st.text_input("相談ごとを入力してください：", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🥺"
        if message["role"]=="assistant":
            speaker="🙍"

        st.write(speaker + ": " + message["content"])
