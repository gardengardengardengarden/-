import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="주사위 배틀", page_icon="🎲")

st.title("🎲 주사위 대결 웹앱")
st.write("세 개의 주사위를 던져 봇과 합계를 겨뤄보세요!")

# 세션 상태 초기화 (승패 기록 저장)
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'bot_score' not in st.session_state:
    st.session_state.bot_score = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# 사이드바에 전적 표시
st.sidebar.header("📊 현재 전적")
st.sidebar.write(f"플레이어: {st.session_state.user_score} 승")
st.sidebar.write(f"봇: {st.session_state.bot_score} 승")

if st.sidebar.button("전적 초기화"):
    st.session_state.user_score = 0
    st.session_state.bot_score = 0
    st.session_state.history = []
    st.rerun()

# 게임 시작 버튼
if st.button("주사위 던지기!", type="primary"):
    with st.spinner('주사위를 굴리는 중...'):
        time.sleep(0.5)
        
        # 주사위 굴리기 (1~6 사이의 숫자 2개씩)
        user_dice = [random.randint(1, 6) for _ in range(2)]
        bot_dice = [random.randint(1, 6) for _ in range(2)]
        
        user_sum = sum(user_dice)
        bot_sum = sum(bot_dice)
        
        # 결과 화면 출력
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 플레이어")
            st.write(f"결과: {user_dice[0]} + {user_dice[1]} + {user_dice[2]}")
            st.metric(label="합계", value=user_sum)
            
        with col2:
            st.subheader("🤖 봇")
            st.write(f"결과: {bot_dice[0]} + {bot_dice[1]} + {bot_dice[2]}")
            st.metric(label="합계", value=bot_sum)
            
        # 승패 판정
        st.divider()
        if user_sum > bot_sum:
            st.balloons()
            st.success(f"🎉 승리했습니다! ({user_sum} > {bot_sum})")
            st.session_state.user_score += 1
            result_text = "승리"
        elif user_sum < bot_sum:
            st.error(f"💀 패배했습니다... ({user_sum} < {bot_sum})")
            st.session_state.bot_score += 1
            result_text = "패배"
        else:
            st.warning(f"🤝 비겼습니다! ({user_sum} == {bot_sum})")
            result_text = "무승부"
            
        # 기록 추가
        st.session_state.history.insert(0, f"{result_text} (나: {user_sum} vs 봇: {bot_sum})")

# 최근 게임 기록 표시
if st.session_state.history:
    st.write("---")
    st.subheader("📜 최근 기록")
    for record in st.session_state.history[:5]: # 최신 5경기만 표시

        st.write(record)
