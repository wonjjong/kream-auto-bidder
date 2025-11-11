#!/bin/bash

# KREAM 자동 입찰 프로그램 - 웹 UI 실행 스크립트

echo "╔════════════════════════════════════════════╗"
echo "║   KREAM 자동 입찰 프로그램 (Web UI)      ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# 가상환경 활성화
if [ -d "venv" ]; then
    echo "🔧 가상환경 활성화 중..."
    source venv/bin/activate
else
    echo "❌ 가상환경이 없습니다. setup.sh를 먼저 실행하세요."
    exit 1
fi

# Streamlit 실행
echo "🚀 웹 UI를 시작합니다..."
echo ""
echo "📱 브라우저에서 자동으로 열립니다"
echo "🌐 주소: http://localhost:8501"
echo ""
echo "⏹️  종료하려면 Ctrl+C를 누르세요"
echo ""

streamlit run app.py

