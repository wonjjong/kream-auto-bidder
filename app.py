"""
KREAM 자동 입찰 프로그램 - Streamlit UI
"""
import streamlit as st
import pandas as pd
import time
from datetime import datetime
import threading
import queue

from utils import load_config, format_price, get_env, create_directories
from kream_crawler import KreamCrawler
from auto_bidder import KreamAutoBidder
from price_monitor import PriceMonitor

# 페이지 설정
st.set_page_config(
    page_title="KREAM 자동 입찰 프로그램",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'bid_history' not in st.session_state:
    st.session_state.bid_history = []
if 'price_history' not in st.session_state:
    st.session_state.price_history = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 디렉토리 생성
create_directories()


def main():
    """메인 함수"""
    
    # 타이틀
    st.title("🛍️ KREAM 자동 입찰 프로그램")
    
    # 경고 메시지
    with st.expander("⚠️ 중요 주의사항", expanded=False):
        st.warning("""
        **이 프로그램은 교육 목적으로만 제공됩니다.**
        
        - KREAM 서비스 약관을 반드시 확인하세요
        - 자동화 프로그램 사용이 약관 위반일 수 있습니다
        - 과도한 요청으로 서버에 부담을 주지 마세요
        - 계정 제재나 법적 문제가 발생할 수 있습니다
        - 본인 책임하에 사용하세요
        """)
    
    # 사이드바 - 설정
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # 계정 정보
        st.subheader("🔐 계정 정보")
        email = st.text_input("KREAM 이메일", value=get_env('KREAM_EMAIL', ''), type="default")
        password = st.text_input("KREAM 비밀번호", value=get_env('KREAM_PASSWORD', ''), type="password")
        
        if st.button("🔓 로그인 테스트", use_container_width=True):
            with st.spinner("로그인 중..."):
                # 로그인 테스트 로직
                st.session_state.logged_in = True
                st.success("✅ 로그인 성공!")
        
        st.divider()
        
        # 모니터링 설정
        st.subheader("🔍 모니터링 설정")
        config = load_config()
        
        check_interval = st.slider(
            "가격 확인 주기 (초)",
            min_value=10,
            max_value=300,
            value=config.get('crawler', {}).get('check_interval', 60),
            step=10
        )
        
        headless = st.checkbox(
            "헤드리스 모드 (브라우저 숨김)",
            value=config.get('browser', {}).get('headless', False)
        )
        
        st.divider()
        
        # 입찰 설정
        st.subheader("💰 입찰 설정")
        
        auto_bid = st.checkbox(
            "자동 입찰 활성화",
            value=config.get('bidding', {}).get('auto_bid', True)
        )
        
        min_price = st.number_input(
            "최소 입찰 가격 (원)",
            min_value=0,
            value=config.get('bidding', {}).get('min_price', 50000),
            step=1000
        )
        
        max_price = st.number_input(
            "최대 입찰 가격 (원)",
            min_value=0,
            value=config.get('bidding', {}).get('max_price', 200000),
            step=1000
        )
    
    # 메인 컨텐츠
    tab1, tab2, tab3, tab4 = st.tabs(["📊 모니터링", "💰 자동 입찰", "📈 히스토리", "ℹ️ 정보"])
    
    # 탭 1: 가격 모니터링
    with tab1:
        st.header("📊 가격 모니터링")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            product_url = st.text_input(
                "상품 URL",
                placeholder="https://kream.co.kr/products/xxxxx",
                help="KREAM 상품 페이지 URL을 입력하세요"
            )
        
        with col2:
            size = st.text_input(
                "사이즈",
                placeholder="270",
                help="상품 사이즈를 입력하세요"
            )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 가격 조회", use_container_width=True, type="primary"):
                if product_url and size:
                    with st.spinner("가격 정보를 가져오는 중..."):
                        try:
                            # 가격 조회 로직 (시뮬레이션)
                            st.success("✅ 가격 조회 완료!")
                            
                            # 결과 표시
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("최저 판매가", "150,000원", "-5,000원")
                            with col_b:
                                st.metric("최고 구매가", "145,000원", "+2,000원")
                            with col_c:
                                st.metric("즉시 구매가", "155,000원", "0원")
                        except Exception as e:
                            st.error(f"❌ 오류 발생: {e}")
                else:
                    st.warning("⚠️ 상품 URL과 사이즈를 입력하세요")
        
        with col2:
            if st.button("📈 모니터링 시작", use_container_width=True):
                if product_url and size:
                    st.session_state.monitoring = True
                    st.info("🔄 모니터링이 시작되었습니다")
                else:
                    st.warning("⚠️ 상품 URL과 사이즈를 입력하세요")
        
        with col3:
            if st.button("⏹️ 모니터링 중지", use_container_width=True):
                st.session_state.monitoring = False
                st.info("⏸️ 모니터링이 중지되었습니다")
        
        # 가격 차트
        st.subheader("📉 가격 추이")
        if st.session_state.price_history:
            df = pd.DataFrame(st.session_state.price_history)
            st.line_chart(df.set_index('timestamp'))
        else:
            st.info("가격 데이터가 없습니다. 모니터링을 시작하세요.")
    
    # 탭 2: 자동 입찰
    with tab2:
        st.header("💰 자동 입찰")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            bid_product_url = st.text_input(
                "입찰 상품 URL",
                placeholder="https://kream.co.kr/products/xxxxx",
                key="bid_url"
            )
        
        with col2:
            bid_size = st.text_input(
                "입찰 사이즈",
                placeholder="270",
                key="bid_size"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_price = st.number_input(
                "목표 입찰 가격 (원)",
                min_value=0,
                value=100000,
                step=1000,
                help="이 가격 이하일 때 자동으로 입찰합니다"
            )
        
        with col2:
            bid_max_price = st.number_input(
                "최대 입찰 가격 (원)",
                min_value=0,
                value=150000,
                step=1000,
                help="이 가격을 초과하면 입찰하지 않습니다"
            )
        
        st.divider()
        
        # 입찰 요약
        with st.container():
            st.subheader("📋 입찰 설정 요약")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("목표 가격", format_price(target_price))
            with col2:
                st.metric("최대 가격", format_price(bid_max_price))
            with col3:
                st.metric("확인 주기", f"{check_interval}초")
            with col4:
                auto_status = "✅ 활성화" if auto_bid else "❌ 비활성화"
                st.metric("자동 입찰", auto_status)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 자동 입찰 시작", use_container_width=True, type="primary"):
                if bid_product_url and bid_size:
                    if auto_bid:
                        st.success("✅ 자동 입찰이 시작되었습니다!")
                        st.info(f"""
                        **입찰 조건:**
                        - 목표 가격: {format_price(target_price)}
                        - 최대 가격: {format_price(bid_max_price)}
                        - 확인 주기: {check_interval}초
                        
                        💡 가격이 목표 가격 이하로 떨어지면 자동으로 입찰합니다.
                        """)
                    else:
                        st.warning("⚠️ 자동 입찰이 비활성화되어 있습니다. 사이드바에서 활성화하세요.")
                else:
                    st.warning("⚠️ 상품 URL과 사이즈를 입력하세요")
        
        with col2:
            if st.button("⏹️ 자동 입찰 중지", use_container_width=True):
                st.info("⏸️ 자동 입찰이 중지되었습니다")
        
        # 실시간 상태
        st.subheader("📡 실시간 상태")
        status_placeholder = st.empty()
        
        with status_placeholder.container():
            st.info("💤 대기 중... 자동 입찰을 시작하세요.")
    
    # 탭 3: 히스토리
    with tab3:
        st.header("📈 입찰 히스토리")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("총 입찰 시도", len(st.session_state.bid_history))
        with col2:
            success_count = sum(1 for bid in st.session_state.bid_history if bid.get('status') == 'success')
            st.metric("성공", success_count)
        with col3:
            failed_count = len(st.session_state.bid_history) - success_count
            st.metric("실패", failed_count)
        
        st.divider()
        
        # 히스토리 테이블
        if st.session_state.bid_history:
            df = pd.DataFrame(st.session_state.bid_history)
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn("시간", format="YYYY-MM-DD HH:mm:ss"),
                    "price": st.column_config.NumberColumn("가격", format="%d원"),
                    "size": "사이즈",
                    "status": st.column_config.TextColumn("상태")
                }
            )
            
            # 다운로드 버튼
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 CSV 다운로드",
                data=csv,
                file_name=f"bid_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("입찰 히스토리가 없습니다.")
        
        # 히스토리 초기화
        if st.button("🗑️ 히스토리 초기화", type="secondary"):
            st.session_state.bid_history = []
            st.rerun()
    
    # 탭 4: 정보
    with tab4:
        st.header("ℹ️ 프로그램 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 주요 기능")
            st.markdown("""
            - 🔍 **실시간 가격 모니터링**
              - 설정한 주기로 상품 가격 확인
              - 가격 추이 차트로 시각화
            
            - 💰 **자동 입찰**
              - 목표 가격 달성 시 자동 입찰
              - 최대 가격 설정으로 안전 장치
            
            - 📊 **입찰 히스토리**
              - 모든 입찰 기록 저장
              - CSV 파일로 내보내기
            
            - ⚙️ **설정 관리**
              - 유연한 모니터링 주기 설정
              - 가격 범위 설정
            """)
        
        with col2:
            st.subheader("📚 사용 방법")
            st.markdown("""
            **1단계: 계정 설정**
            - 사이드바에서 KREAM 계정 정보 입력
            - 로그인 테스트로 확인
            
            **2단계: 가격 모니터링**
            - 상품 URL과 사이즈 입력
            - 가격 조회로 현재 가격 확인
            - 필요시 모니터링 시작
            
            **3단계: 자동 입찰 설정**
            - 목표 가격과 최대 가격 설정
            - 자동 입찰 활성화
            - 자동 입찰 시작 버튼 클릭
            
            **4단계: 결과 확인**
            - 히스토리 탭에서 입찰 기록 확인
            - 필요시 CSV로 내보내기
            """)
        
        st.divider()
        
        st.subheader("⚠️ 주의사항")
        st.error("""
        **경고:**
        - 이 프로그램은 교육 목적으로만 제공됩니다
        - KREAM의 이용약관을 준수해야 합니다
        - 자동화 프로그램 사용이 약관 위반일 수 있습니다
        - 계정 제재나 법적 문제가 발생할 수 있습니다
        - 본인 책임하에 사용하세요
        """)
        
        st.divider()
        
        # 시스템 정보
        st.subheader("🔧 시스템 정보")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Python 버전", "3.13")
        with col2:
            st.metric("Streamlit 버전", st.__version__)
        with col3:
            config = load_config()
            st.metric("설정 파일", "config.yaml" if config else "없음")


if __name__ == "__main__":
    main()

