import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="주사위 배틀 게임", page_icon="🎲")

# --- 게임 상태 초기화 ---
if 'player_hp' not in st.session_state:
    st.session_state.player_hp = 15
if 'bot_hp' not in st.session_state:
    st.session_state.bot_hp = 15
if 'game_log' not in st.session_state:
    st.session_state.game_log = []

# --- 함수 정의 ---
def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def reset_game():
    st.session_state.player_hp = 15
    st.session_state.bot_hp = 15
    st.session_state.game_log = []

# --- UI 레이아웃 ---
st.title("⚔️ 주사위 배틀 웹앱")
st.write("주사위 2개의 합으로 봇과 대결하세요! 먼저 HP가 0이 되면 패배합니다.")

# HP 표시부
col1, col2 = st.columns(2)
with col1:
    st.metric(label="나의 HP", value=st.session_state.player_hp, delta_color="normal")
with col2:
    st.metric(label="봇의 HP", value=st.session_state.bot_hp, delta_color="inverse")

# 배틀 진행 버튼
if st.button("주사위 던지기! 🎲", disabled=st.session_state.player_hp <= 0 or st.session_state.bot_hp <= 0):
    # 주사위 굴리기
    p1, p2 = roll_dice()
    b1, b2 = roll_dice()
    
    p_sum = p1 + p2
    b_sum = b1 + b2
    
    diff = abs(p_sum - b_sum)
    
    # 승패 판정 로직
    if p_sum > b_sum:
        result_text = f"승리! 봇에게 {diff} 데미지를 입혔습니다."
        st.session_state.bot_hp -= diff
    elif p_sum < b_sum:
        result_text = f"패배... 나에게 {diff} 데미지가 들어왔습니다."
        st.session_state.player_hp -= diff
    else:
        result_text = "무승부! 아무 일도 일어나지 않았습니다."

    # 로그 기록
    log_entry = f"나: {p_sum}({p1}+{p2}) vs 봇: {b_sum}({b1}+{b2}) | {result_text}"
    st.session_state.game_log.insert(0, log_entry)

# --- 결과 발표 ---
if st.session_state.player_hp <= 0:
    st.error("💀 당신은 패배했습니다!")
    if st.button("다시 시작하기"):
        reset_game()
        st.rerun()
elif st.session_state.bot_hp <= 0:
    st.balloons()
    st.success("🏆 축하합니다! 봇을 물리쳤습니다!")
    if st.button("다시 시작하기"):
        reset_game()
        st.rerun()

# --- 게임 로그 ---
st.divider()
st.subheader("📜 전투 기록")
for log in st.session_state.game_log:
    st.write(log)
