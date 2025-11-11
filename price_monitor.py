"""
가격 모니터링 모듈
"""
import time
import argparse
from datetime import datetime
import pandas as pd
from kream_crawler import KreamCrawler
from utils import setup_logger, load_config, save_to_csv, format_price


class PriceMonitor:
    """가격 모니터링 클래스"""
    
    def __init__(self, product_url, size=None):
        """
        초기화
        
        Args:
            product_url (str): 상품 URL
            size (str): 사이즈
        """
        self.logger = setup_logger('PriceMonitor', 'logs/price_monitor.log')
        self.config = load_config()
        self.product_url = product_url
        self.size = size
        self.crawler = KreamCrawler()
        self.price_history = []
        
    def start_monitoring(self, duration=None):
        """
        모니터링 시작
        
        Args:
            duration (int): 모니터링 지속 시간 (초), None이면 무한 실행
        """
        try:
            self.crawler.setup_driver()
            self.crawler.login()
            
            # 상품 정보 가져오기
            product_info = self.crawler.get_product_info(self.product_url)
            if not product_info:
                self.logger.error("상품 정보를 가져올 수 없습니다")
                return
            
            self.logger.info(f"모니터링 시작: {product_info['name']}")
            self.logger.info(f"사이즈: {self.size or '전체'}")
            
            check_interval = self.config.get('crawler', {}).get('check_interval', 60)
            start_time = time.time()
            
            while True:
                try:
                    # 가격 정보 가져오기
                    bid_info = self.crawler.get_bid_prices(self.size)
                    
                    if bid_info:
                        # 가격 기록
                        price_data = {
                            'timestamp': datetime.now(),
                            'buy_now_price': bid_info['buy_now_price'],
                            'highest_bid': bid_info['highest_bid'],
                            'lowest_ask': bid_info['lowest_ask'],
                            'size': self.size
                        }
                        self.price_history.append(price_data)
                        
                        # 콘솔 출력
                        print(f"\n[{price_data['timestamp'].strftime('%H:%M:%S')}] 가격 업데이트")
                        print(f"  즉시 구매가: {format_price(bid_info['buy_now_price'])}")
                        print(f"  최고 입찰가: {format_price(bid_info['highest_bid'])}")
                        print(f"  최저 판매가: {format_price(bid_info['lowest_ask'])}")
                        
                        # 가격 변동 알림
                        self._check_price_change(bid_info)
                        
                        # 주기적으로 데이터 저장
                        if len(self.price_history) % 10 == 0:
                            self._save_history()
                    
                    # 지속 시간 체크
                    if duration and (time.time() - start_time) >= duration:
                        self.logger.info("모니터링 시간 종료")
                        break
                    
                    # 대기
                    self.logger.info(f"{check_interval}초 후 다시 확인...")
                    time.sleep(check_interval)
                    
                except KeyboardInterrupt:
                    self.logger.info("사용자가 모니터링을 중단했습니다")
                    break
                except Exception as e:
                    self.logger.error(f"모니터링 중 오류: {e}")
                    time.sleep(check_interval)
            
        except Exception as e:
            self.logger.error(f"모니터링 실패: {e}")
        finally:
            self._save_history()
            self.crawler.close()
    
    def _check_price_change(self, current_bid):
        """
        가격 변동 체크
        
        Args:
            current_bid (dict): 현재 입찰 정보
        """
        if len(self.price_history) < 2:
            return
        
        prev_price = self.price_history[-2]['buy_now_price']
        curr_price = current_bid['buy_now_price']
        
        if curr_price < prev_price:
            change = prev_price - curr_price
            self.logger.info(f"🔔 가격 하락! {format_price(change)} 감소")
            print(f"  ⬇️  가격 하락: {format_price(change)}")
        elif curr_price > prev_price:
            change = curr_price - prev_price
            self.logger.info(f"가격 상승: {format_price(change)}")
            print(f"  ⬆️  가격 상승: {format_price(change)}")
    
    def _save_history(self):
        """가격 이력 저장"""
        if not self.price_history:
            return
        
        try:
            df = pd.DataFrame(self.price_history)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'data/price_history_{timestamp}.csv'
            save_to_csv(df, filename)
            self.logger.info(f"가격 이력 저장 완료 ({len(self.price_history)}건)")
        except Exception as e:
            self.logger.error(f"가격 이력 저장 실패: {e}")
    
    def get_statistics(self):
        """
        가격 통계 반환
        
        Returns:
            dict: 통계 정보
        """
        if not self.price_history:
            return {}
        
        df = pd.DataFrame(self.price_history)
        
        stats = {
            'count': len(df),
            'avg_price': df['buy_now_price'].mean(),
            'min_price': df['buy_now_price'].min(),
            'max_price': df['buy_now_price'].max(),
            'std_price': df['buy_now_price'].std()
        }
        
        return stats


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='KREAM 가격 모니터링')
    parser.add_argument('--product-url', type=str, required=True, help='상품 URL')
    parser.add_argument('--size', type=str, help='사이즈 (예: 270)')
    parser.add_argument('--duration', type=int, help='모니터링 시간 (초)')
    
    args = parser.parse_args()
    
    monitor = PriceMonitor(args.product_url, args.size)
    monitor.start_monitoring(args.duration)
    
    # 통계 출력
    stats = monitor.get_statistics()
    if stats:
        print("\n=== 가격 통계 ===")
        print(f"측정 횟수: {stats['count']}회")
        print(f"평균 가격: {format_price(int(stats['avg_price']))}")
        print(f"최저 가격: {format_price(int(stats['min_price']))}")
        print(f"최고 가격: {format_price(int(stats['max_price']))}")


if __name__ == "__main__":
    main()

