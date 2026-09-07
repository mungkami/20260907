# AGENTS.md

## Project Overview

-Streamlit으로 만드는 1페이지 MVP
-순수 Python, 외부 DB 없음

## Setup Commands

-의존성 설치: pip install -r requirements.txt
-앱 실행: streamlit run app.py

## Code Style

-타입 힌트 사용, 함수는 작게 분리
-@st.cache_data 로 비용 큰 연산 캐싱
-UI 텍스트는 한국어
-모든 UI에 이모지 아이콘과 짧은 설명을 붙인다
-사이드바에 필터를 배치한다
-색상은 차분한 단색 팔레트로 통일한다

## Security

-API 키/시크릿은 코드에 하드코딩 금지
-비밀은 .streamlit/secrets.toml 또는 환경변수로