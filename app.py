import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="주사위 배틀 수정본", page_icon="🎲")

# --- 1. 세션 상태 초기화 (더 깔끔하게) ---
if 'init' not in st.session_state:
    st.session_state.player_hp = 15
    st.session_state.bot_hp = 15
    st.session_state.game_log = []
    st.session_state.game_over = False
    st.session_state.init = True

def reset_game():
    st.session_state.player_hp = 15
    st.session_state.bot_hp = 15
    st.session_state.game_log = []
    st.session_state.game_over = False

# --- 2. 배틀 로직 함수 ---
def play_round():
    p1, p2 = random.randint(1, 6), random.randint(1, 6)
    b1, b2 = random.randint(1, 6), random.randint(1, 6)
    
    p_sum = p1 + p2
    b_sum = b1 + b2
    diff = abs(p_sum - b_sum)
    
    if p_sum > b_sum:
        st.session_state.bot_hp -= diff
        res = f"승리! 봇에게 {diff} 데미지"
    elif p_sum < b_sum:
        st.session_state.player_hp -= diff
        res = f"패배... 나에게 {diff} 데미지"
    else:
        res = "무승부!"

    # 로그 기록
    log_text = f"나: {p_sum}({p1}+{p2}) vs 봇: {b_sum}({b1}+{b2}) | {res}"
    st.session_state.game_log.insert(0, log_text)

    # HP가 0 이하인지 즉시 체크
    if st.session_state.player_hp <= 0 or st.session_state.bot_hp <= 0:
        st.session_state.game_over = True

# --- 3. UI 레이아웃 ---
st.title("🎲 주사위 배틀 V2")

# 상황판
c1, c2 = st.columns(2)
# HP가 음수로 표시되지 않게 처리
disp_p_hp = max(0, st.session_state.player_hp)
disp_b_hp = max(0, st.session_state.bot_hp)

c1.metric("나의 HP", f"{disp_p_hp} / 15")
c2.metric("봇의 HP", f"{disp_b_hp} / 15")

# --- 4. 게임 판정 및 버튼 ---
if not st.session_state.game_over:
    if st.button("주사위 던지기 ⚔️"):
        play_round()
        st.rerun() # 중요: 값이 변하자마자 화면을 다시 그려서 즉시 반영
else:
    # 게임 종료 시 결과 출력
    if st.session_state.player_hp <= 0:
        st.error("💀 당신의 패배입니다!")
    else:
        st.balloons()
        st.success("🏆 당신의 승리입니다!")
    
    if st.button("새 게임 시작하기"):
        reset_game()
        st.rerun()

# --- 5. 기록 관리 ---
st.divider()
st.caption("최근 전투 기록")
for log in st.session_state.game_log:
    st.write(log)
