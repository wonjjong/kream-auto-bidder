"""
KREAM 자동 판매 입찰 프로그램 메인
"""
import sys
from utils import create_directories, setup_logger, load_config, get_env
from auto_bidder import KreamAutoBidder


def print_banner():
    """배너 출력"""
    banner = """
    ╔════════════════════════════════════════════╗
    ║   KREAM 자동 판매 입찰 프로그램           ║
    ║   Auto Bidding System for KREAM           ║
    ╚════════════════════════════════════════════╝
    
    ⚠️  중요 주의사항:
    - 이 프로그램은 교육 목적으로만 제공됩니다
    - 서비스 약관을 반드시 확인하세요
    - 본인 책임하에 사용하세요
    """
    print(banner)


def get_user_input():
    """사용자 입력 받기"""
    print("\n=== 입찰 설정 ===\n")
    
    product_url = input("상품 URL: ").strip()
    if not product_url:
        print("❌ 상품 URL을 입력해주세요")
        sys.exit(1)
    
    size = input("사이즈 (예: 270): ").strip()
    if not size:
        print("❌ 사이즈를 입력해주세요")
        sys.exit(1)
    
    try:
        target_price = int(input("목표 입찰 가격 (원): ").strip())
        max_price = int(input("최대 입찰 가격 (원): ").strip())
    except ValueError:
        print("❌ 올바른 가격을 입력해주세요")
        sys.exit(1)
    
    if target_price > max_price:
        print("❌ 목표 가격이 최대 가격보다 클 수 없습니다")
        sys.exit(1)
    
    return {
        'product_url': product_url,
        'size': size,
        'target_price': target_price,
        'max_price': max_price
    }


def confirm_settings(settings):
    """설정 확인"""
    print("\n=== 입찰 설정 확인 ===")
    print(f"상품 URL: {settings['product_url']}")
    print(f"사이즈: {settings['size']}")
    print(f"목표 가격: {settings['target_price']:,}원")
    print(f"최대 가격: {settings['max_price']:,}원")
    
    confirm = input("\n이 설정으로 진행하시겠습니까? (y/n): ").strip().lower()
    return confirm == 'y'


def main():
    """메인 함수"""
    # 배너 출력
    print_banner()
    
    # 필요한 디렉토리 생성
    create_directories()
    
    # 로거 설정
    logger = setup_logger('Main', 'logs/main.log')
    logger.info("프로그램 시작")
    
    # 환경 변수 확인
    email = get_env('KREAM_EMAIL')
    password = get_env('KREAM_PASSWORD')
    
    if not email or not password:
        print("\n⚠️  경고: .env 파일에 계정 정보가 설정되지 않았습니다")
        print("자동 로그인이 불가능할 수 있습니다\n")
    
    try:
        # 사용자 입력
        settings = get_user_input()
        
        # 설정 확인
        if not confirm_settings(settings):
            print("\n입찰이 취소되었습니다")
            sys.exit(0)
        
        # 자동 입찰 시작
        print("\n" + "="*50)
        print("자동 입찰을 시작합니다...")
        print("중단하려면 Ctrl+C를 누르세요")
        print("="*50 + "\n")
        
        bidder = KreamAutoBidder()
        bidder.monitor_and_bid(
            product_url=settings['product_url'],
            size=settings['size'],
            target_price=settings['target_price'],
            max_price=settings['max_price']
        )
        
    except KeyboardInterrupt:
        print("\n\n프로그램이 사용자에 의해 중단되었습니다")
        logger.info("사용자가 프로그램을 중단했습니다")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        logger.error(f"프로그램 오류: {e}", exc_info=True)
    finally:
        logger.info("프로그램 종료")
        print("\n프로그램을 종료합니다\n")


if __name__ == "__main__":
    main()

