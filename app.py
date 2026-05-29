import streamlit as st
import random

st.title("🔮 오늘의 운세")

fortunes = [
    "오늘은 기분 좋은 일이 생길 것 같아요!",
    "작은 행운이 찾아올 거예요 😊",
    "새로운 기회가 열릴 수 있어요!",
    "주변 사람들과 좋은 일이 생길 것 같아요!",
    "오늘은 평온하고 안정적인 하루가 될 거예요.",
    "노력한 만큼 결과가 찾아오는 날이에요!",
]

if st.button("운세 뽑기 🎉"):
    st.write(random.choice(fortunes))
