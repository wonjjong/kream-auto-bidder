#!/bin/bash

# KREAM 자동 입찰 프로그램 - 웹 UI 실행 (개발 모드)

echo "╔════════════════════════════════════════════╗"
echo "║   KREAM 자동 입찰 - 개발 모드            ║"
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

# Streamlit 개발 모드 실행
echo "🚀 개발 모드로 웹 UI를 시작합니다..."
echo ""
echo "✨ 개발 모드 기능:"
echo "   - 📝 코드 수정 시 자동 반영"
echo "   - 🔄 빠른 리런 (Fast Rerun)"
echo "   - 🐛 디버그 모드"
echo ""
echo "📱 브라우저에서 자동으로 열립니다"
echo "🌐 주소: http://localhost:8501"
echo ""
echo "💡 팁: 파일을 저장하면 자동으로 페이지가 새로고침됩니다"
echo "⏹️  종료하려면 Ctrl+C를 누르세요"
echo ""

# 개발 모드 옵션으로 실행
streamlit run app.py \
  --server.runOnSave true \
  --server.fileWatcherType auto \
  --runner.fastReruns true \
  --logger.level debug

