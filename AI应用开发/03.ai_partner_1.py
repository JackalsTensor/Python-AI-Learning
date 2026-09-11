import streamlit as st
import os
from openai import OpenAI


st.set_page_config(page_title="Jackals的AI项目之DeepSeek大模型部署",
                    page_icon="🐶",
                    layout="wide",
                    initial_sidebar_state="expanded",
                    menu_items={}
                    )

st.image(image="C:\\Users\\fangkaimin\\Pictures\\联想截图\\联想截图_20260118220359.jpg", width=170)
st.title("Jackals的AI项目之DeepSeek大模型部署")
st.subheader("(注:以Python第三方库streamlit库为框架创作页面,以DeepSeek大模型作为算力支撑的人工智能小项目)")


#系统提示词
system_prompt = """你叫科比布莱恩特，现在是用户的助手，请完全代入科比牢大角色。：
规则：
1.  每次只回1条消息
2.  使用球员科比的语言风格
3.  有需要的话可以用❤️🌸等表情来彰显科比姿态
4.  用符合科比性格的方式对话
5.  顺着用户语气说话或者回答问题
6.  你无所不知能够解答各种问题,上知天文下至地理，精通高等数学，计算机科学，量子力学等领域
7. 科比通常喜欢用的语言如下请参考：曼巴Out,肘击,孩子们,坠机,孩子们我又回来了,哈哈哈Out,what can I say,man
8.  要回答学术问题时用到专业语句
9.  回答内容每个不少于20个字
助手性格：
- 具备著名NBA球员科比的性格的有广大学问的学者
你必须严格遵守上述规则来回复用户。"""

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages=[]

#展示聊天信息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
    # if message["role"]=="user":
    #     st.chat_message("user").write(message["content"])
    # else:
    #     st.chat_message("assistant").write(message["content"])

#创建AI大模型交互的客户端对象
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

#左侧侧边栏
with st.sidebar:
    st.subheader("AI助手信息")
    nick_name=st.text_input("昵称",placeholder="请输入昵称",value="科比布莱恩特(牢大)")
    animal=st.text_input("介绍",placeholder="请输入介绍",value="我是你们的牢大")
#消息输入框
prompt= st.chat_input("请输入您要问的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print("------->调用AI大模型，提示词:", prompt)
    #保存用户提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用AI大模型
    print([
        {"role": "system", "content": system_prompt},
        *st.session_state.messages,
    ])
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
        stream=True
    )

    # #输出大模型返回的结果(非流式的解析方式)
    # print("<--------大模型返回的结果：",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    # 输出大模型返回的结果(流式的解析方式)
    response_message = st.empty()  # 创建一个空对象，用于展示大模型返回的结果
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    # 保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})