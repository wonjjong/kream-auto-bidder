"""
자동 입찰 모듈
"""
import time
import argparse
from datetime import datetime
from kream_crawler import KreamCrawler
from price_monitor import PriceMonitor
from utils import setup_logger, load_config, format_price, get_env


class KreamAutoBidder:
    """KREAM 자동 입찰 클래스"""
    
    def __init__(self):
        """초기화"""
        self.logger = setup_logger('AutoBidder', 'logs/auto_bidder.log')
        self.config = load_config()
        self.crawler = KreamCrawler()
        self.bid_history = []
        
    def setup(self):
        """초기 설정"""
        self.crawler.setup_driver()
        if not self.crawler.login():
            raise Exception("로그인에 실패했습니다")
    
    def place_bid(self, product_url, size, price):
        """
        입찰하기
        
        Args:
            product_url (str): 상품 URL
            size (str): 사이즈
            price (int): 입찰 가격
            
        Returns:
            bool: 입찰 성공 여부
        """
        try:
            self.logger.info(f"입찰 시도: {format_price(price)}, 사이즈: {size}")
            
            # 상품 페이지로 이동
            self.crawler.driver.get(product_url)
            time.sleep(2)
            
            # ⚠️ 여기에 실제 입찰 로직 구현 필요
            # KREAM의 실제 입찰 프로세스에 맞게 구현
            # 1. 사이즈 선택
            # 2. 판매 버튼 클릭
            # 3. 가격 입력
            # 4. 입찰 확인
            
            self.logger.warning("⚠️  실제 입찰 로직은 구현되지 않았습니다")
            self.logger.warning("실제 사용을 위해서는 KREAM의 HTML 구조에 맞게 구현이 필요합니다")
            
            # 입찰 기록
            bid_record = {
                'timestamp': datetime.now(),
                'product_url': product_url,
                'size': size,
                'price': price,
                'status': 'test'  # success, failed, test
            }
            self.bid_history.append(bid_record)
            
            return False  # 테스트 모드에서는 False 반환
            
        except Exception as e:
            self.logger.error(f"입찰 실패: {e}")
            return False
    
    def monitor_and_bid(self, product_url, size, target_price, max_price=None):
        """
        가격 모니터링 후 자동 입찰
        
        Args:
            product_url (str): 상품 URL
            size (str): 사이즈
            target_price (int): 목표 가격
            max_price (int): 최대 가격
        """
        try:
            self.setup()
            
            # 설정값 가져오기
            if max_price is None:
                max_price = self.config.get('bidding', {}).get('max_price', target_price)
            
            check_interval = self.config.get('crawler', {}).get('check_interval', 60)
            
            self.logger.info(f"자동 입찰 시작")
            self.logger.info(f"목표 가격: {format_price(target_price)}")
            self.logger.info(f"최대 가격: {format_price(max_price)}")
            
            # 상품 정보 조회
            product_info = self.crawler.get_product_info(product_url)
            if not product_info:
                self.logger.error("상품 정보를 가져올 수 없습니다")
                return
            
            print(f"\n{'='*50}")
            print(f"상품: {product_info['name']}")
            print(f"사이즈: {size}")
            print(f"목표 가격: {format_price(target_price)}")
            print(f"{'='*50}\n")
            
            while True:
                try:
                    # 현재 가격 조회
                    bid_info = self.crawler.get_bid_prices(size)
                    
                    if not bid_info:
                        self.logger.warning("가격 정보를 가져올 수 없습니다")
                        time.sleep(check_interval)
                        continue
                    
                    current_price = bid_info['lowest_ask']
                    
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 현재 최저 판매가: {format_price(current_price)}")
                    
                    # 입찰 조건 확인
                    if current_price > 0 and current_price <= target_price:
                        self.logger.info(f"🎯 목표 가격 달성! 입찰 시도...")
                        
                        # 입찰 실행
                        success = self.place_bid(product_url, size, current_price)
                        
                        if success:
                            print(f"\n✅ 입찰 성공! 가격: {format_price(current_price)}")
                            self.logger.info(f"입찰 성공: {format_price(current_price)}")
                            break
                        else:
                            print(f"\n⚠️  입찰 실패 (테스트 모드)")
                            self.logger.warning("입찰 실패 또는 테스트 모드")
                    
                    elif current_price > max_price:
                        self.logger.info(f"현재 가격({format_price(current_price)})이 최대 가격을 초과합니다")
                    
                    # 대기
                    time.sleep(check_interval)
                    
                except KeyboardInterrupt:
                    self.logger.info("사용자가 자동 입찰을 중단했습니다")
                    break
                except Exception as e:
                    self.logger.error(f"모니터링 중 오류: {e}")
                    time.sleep(check_interval)
            
        except Exception as e:
            self.logger.error(f"자동 입찰 실패: {e}")
        finally:
            self.crawler.close()
            self._print_summary()
    
    def _print_summary(self):
        """입찰 요약 출력"""
        if not self.bid_history:
            print("\n입찰 기록이 없습니다.")
            return
        
        print(f"\n{'='*50}")
        print("입찰 요약")
        print(f"{'='*50}")
        print(f"총 입찰 시도: {len(self.bid_history)}회")
        
        for i, bid in enumerate(self.bid_history, 1):
            print(f"\n{i}. {bid['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   가격: {format_price(bid['price'])}")
            print(f"   사이즈: {bid['size']}")
            print(f"   상태: {bid['status']}")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='KREAM 자동 입찰')
    parser.add_argument('--product-url', type=str, required=True, help='상품 URL')
    parser.add_argument('--size', type=str, required=True, help='사이즈')
    parser.add_argument('--target-price', type=int, help='목표 가격')
    parser.add_argument('--max-price', type=int, help='최대 가격')
    
    args = parser.parse_args()
    
    # 환경 변수에서 가격 가져오기
    target_price = args.target_price or int(get_env('TARGET_PRICE', 100000))
    max_price = args.max_price or int(get_env('MAX_PRICE', 150000))
    
    bidder = KreamAutoBidder()
    bidder.monitor_and_bid(args.product_url, args.size, target_price, max_price)


if __name__ == "__main__":
    main()

