import streamlit as st
import google.generativeai as genai

# 페이지 설정 및 타이틀 (주제 변경 시 이 부분을 수정하세요)
st.set_page_config(page_title="연애 카운셀러 제미니", page_icon="💖")
st.title("💖 연애 상담소")
st.caption("Gemini-2.5-Flash-Lite가 전하는 따뜻하고 솔직한 연애 조언")

# 1. API Key 불러오기 및 설정 (Streamlit Secrets)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("오류: Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

# 2. 채팅 기록(Chat Session) 초기화
if "chat_session" not in st.session_state:
    try:
        # 모델 설정 (gemini-2.5-flash-lite 지정)
        # 주제를 바꾸려면 아래 system_instruction의 내용을 변경하면 됩니다.
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=(
                "당신은 공감 능력이 뛰어나고 다정한 연애 카운셀러입니다. "
                "사용자의 연애 고민(짝사랑, 이별, 썸, 연애 중 갈등 등)을 진지하게 들어주고, "
                "친구처럼 따뜻하면서도 현실적인 조언을 제공하세요. 이모지를 적절히 섞어 친근하게 답변하세요."
            )
        )
        # 대화 기록 유지를 위해 비어있는 히스토리로 챗 세션 시작
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"모델 초기화 중 오류가 발생했습니다: {e}")
        st.stop()

# 3. 기존 대화 기록 화면에 출력
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 4. 사용자 입력 및 AI 응답 처리
if user_input := st.chat_input("연애 고민이나 궁금한 점을 편하게 이야기해주세요..."):
    # 사용자가 입력한 메시지 화면에 표시
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # AI 응답 생성 및 예외 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            with st.spinner("생각 중... 💬"):
                # 대화 기록이 유지된 채로 메시지 전송
                response = st.session_state.chat_session.send_message(user_input)
                message_placeholder.markdown(response.text)
        except genai.types.generation_types.BlockedPromptException:
            message_placeholder.error("안전 정책에 위배되는 입력 내용입니다. 다른 방식으로 표현해주세요.")
        except Exception as e:
            message_placeholder.error(f"응답을 생성하는 중 오류가 발생했습니다: {e}")
