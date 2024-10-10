import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import os


# 초기 데이터 설정
companies = ['Be;Worth', 'Studio DoDam', 'oh!Meal, Joy Meal', 'ByunchaeZIP', 'HUMM', 'shelwe?', 'Urban+', 'DMZon', 'Dtour', 'Polipocker', 'IPDOONG', 'Onsaemiro', 'ANTOPIA', 'PURIP', 'Edgee', 'zip', 'workzz', 'TaekwonDO', 'odd&ordinary', 'NAR-M', 'Hanno Farm', 'fair:ing', '4D TRAIL', 'Greenip', 'Miliax', 'cultiverse', 'Beingtz', 'Artvi', 'Oppenground', 'Market-in', 'MASKOREA', 'Valim', '@hanji', 'Reside', 'UGYOVERSIAL']
initial_user_coins = 500

# 세션 상태 초기화
if 'data' not in st.session_state:
    st.session_state.data = {company: 0 for company in companies}
if 'coins_history' not in st.session_state:
    st.session_state.coins_history = {company: [0] for company in companies}
if 'user_coins' not in st.session_state:  # 이 부분이 중요합니다.
    st.session_state.user_coins = initial_user_coins

# Streamlit 애플리케이션
st.title('Coin Investment App')

# 사용자 입력
selected_company = st.selectbox('Select a company to invest in:', companies)

# 두 개의 컬럼을 생성하여 버튼과 남은 코인 개수를 나란히 배치
col1, col2 = st.columns([2, 1])
with col1:
    invest_button = st.button('Invest 1 Coin')

# 코인 투자 로직
if invest_button:
    if st.session_state.user_coins > 0:
        st.session_state.data[selected_company] += 1
        st.session_state.coins_history[selected_company].append(st.session_state.data[selected_company])
        st.session_state.user_coins -= 1
    else:
        st.warning("You don't have any coins left to invest.")

with col2:
    st.write(f'You have {st.session_state.user_coins} coins left.')

# 각 리스트의 길이를 동일하게 맞추기
max_length = max(len(lst) for lst in st.session_state.coins_history.values())
for company in companies:
    while len(st.session_state.coins_history[company]) < max_length:
        st.session_state.coins_history[company].append(st.session_state.coins_history[company][-1])

# 실시간 데이터 프레임
df = pd.DataFrame(st.session_state.coins_history)

# 투자 변화 그래프
st.subheader('Investment Changes Over Time')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df)
ax.set_ylim(0, 200)
ax.set_xticks([])
ax.set_yticks(range(0, 201, 10))
ax.legend(df.columns, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small')
st.pyplot(fig)

# 현재 코인 분포 막대 그래프
st.subheader('Current Coin Distribution')
fig, ax = plt.subplots()
ax.bar(st.session_state.data.keys(), st.session_state.data.values())
ax.set_ylim(0, 200)
ax.tick_params(axis='x', rotation=90)
st.pyplot(fig)

# 데이터 테이블
st.subheader('Investment Data Table')
styled_df = df.style.set_properties(**{'max-height': '200px'})
st.dataframe(styled_df)

# 상위 4개 기업 랭킹 가로로 배열하여 표시
st.subheader('Top 4 Companies by Coins')
sorted_data = sorted(st.session_state.data.items(), key=lambda x: x[1], reverse=True)[:4]

cols = st.columns(4)
for idx, (company, coins) in enumerate(sorted_data):
    with cols[idx]:
        st.markdown(f"### {idx + 1}위:")
        st.markdown(f'{company}')
        st.write(f"Coins: {coins}")
        st.write("---")
        
        
   
    