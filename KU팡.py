import datetime
import os
import random

# 주문 클래스
class Order:
    def __init__(self, order_id, product_name, product_price, customer_name, customer_address, order_date):
        self.order_id = order_id
        self.product_name = product_name
        self.product_price = product_price
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.order_date = order_date

    def __str__(self):
        return f"주문번호: {self.order_id}, 상품명: {self.product_name}, 가격: {self.product_price}, 고객명: {self.customer_name}, 주소: {self.customer_address}, 주문일: {self.order_date}"

    # 주문을 파일에 저장할 수 있도록 문자열로 변환
    def to_file_string(self):
        return f"{self.order_id},{self.product_name},{self.product_price},{self.customer_name},{self.customer_address},{self.order_date}\n"

    # 파일에서 읽은 문자열을 주문 객체로 변환
    @staticmethod
    def from_file_string(order_str):
        order_data = order_str.strip().split(',')
        return Order(order_data[0], order_data[1], float(order_data[2]), order_data[3], order_data[4], order_data[5])


# 쇼핑몰 클래스
class ShoppingMall:
    def __init__(self):
        self.orders = []  # 주문 목록
        self.products = {}  # 상품 목록 (상품명: 가격)
        self.current_date = None
        self.load_items()
        self.load_orders()

    # 현재 날짜 설정
    def set_date(self):
        while True:
            try:
                input_date = input("현재 날짜를 입력하세요 (YYYY-MM-DD): ")
                year, month, day = map(int, input_date.split('-'))
                self.current_date = datetime.date(year, month, day)
                if self.current_date > datetime.date.today():
                    print("미래 날짜는 설정할 수 없습니다. 다시 입력하세요.")
                else:
                    break
            except ValueError:
                print("잘못된 형식입니다. 다시 입력하세요.")

    # 상품 추가
    def add_product(self):
        product_name = input("추가할 상품명: ")
        product_price = float(input("상품 가격: "))
        self.products[product_name] = product_price
        print(f"상품 '{product_name}'이(가) 추가되었습니다.")
        self.save_items()

    # 상품 삭제
    def remove_product(self):
        product_name = input("삭제할 상품명: ")
        if product_name in self.products:
            del self.products[product_name]
            print(f"상품 '{product_name}'이(가) 삭제되었습니다.")
            self.save_items()
        else:
            print("해당 상품이 존재하지 않습니다.")

    # 상품 목록 조회 (고객/관리자 공통)
    def view_products(self):
        if not self.products:
            print("등록된 상품이 없습니다.")
        else:
            for product, price in self.products.items():
                print(f"{product}: {price}원")

    # 주문 추가 (고객용)
    def add_order(self):
        customer_name = input("고객 이름: ")
        customer_address = input("고객 주소: ")
        print("상품 목록:")
        self.view_products()

        product_name = input("주문할 상품명을 입력하세요: ")
        if product_name in self.products:
            product_price = self.products[product_name]
            order_id = f"ORD{random.randint(1000, 9999)}"
            order = Order(order_id, product_name, product_price, customer_name, customer_address, self.current_date)
            self.orders.append(order)
            print(f"주문이 추가되었습니다: \n{order}")
            self.save_orders()
        else:
            print("해당 상품이 존재하지 않습니다.")

    # 주문 삭제 (관리자용)
    def remove_order(self):
        order_id = input("삭제할 주문 번호: ")
        found = False
        for order in self.orders:
            if order.order_id == order_id:
                self.orders.remove(order)
                found = True
                print(f"주문 '{order_id}'이(가) 삭제되었습니다.")
                self.save_orders()
                break
        if not found:
            print("해당 주문이 존재하지 않습니다.")

    # 주문 목록 출력
    def view_orders(self):
        if not self.orders:
            print("등록된 주문이 없습니다.")
        else:
            for order in self.orders:
                print(order)

    # 매출 조회
    def view_sales(self):
        total_sales = sum(order.product_price for order in self.orders)
        print(f"총 매출액: {total_sales}원")

    # 파일로부터 상품 읽어오기
    def load_items(self):
        if os.path.exists('items.txt'):
            with open('items.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    product_name, product_price = line.strip().split(',')
                    self.products[product_name] = float(product_price)
            print("상품 목록을 불러왔습니다.")

    # 상품을 파일에 저장
    def save_items(self):
        with open('items.txt', 'w', encoding='utf-8') as f:
            for product_name, product_price in self.products.items():
                f.write(f"{product_name},{product_price}\n")

    # 파일로부터 주문 읽어오기
    def load_orders(self):
        if os.path.exists('orders.txt'):
            with open('orders.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    order = Order.from_file_string(line)
                    self.orders.append(order)
            print("주문 목록을 불러왔습니다.")

    # 주문을 파일에 저장
    def save_orders(self):
        with open('orders.txt', 'w', encoding='utf-8') as f:
            for order in self.orders:
                f.write(order.to_file_string())

    # 고객 메뉴
    def customer_menu(self):
        while True:
            print("\n1. 상품 조회\n2. 주문하기\n3. 종료")
            choice = input("선택: ")
            if choice == '1':
                self.view_products()
            elif choice == '2':
                self.add_order()
            elif choice == '3':
                print("고객 화면을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")

    # 관리자 메뉴
    def admin_menu(self):
        while True:
            print("\n1. 상품 목록 조회\n2. 상품 추가\n3. 상품 삭제\n4. 주문 조회\n5. 주문 삭제\n6. 매출 조회\n7. 종료")
            choice = input("선택: ")
            if choice == '1':
                self.view_products()
            elif choice == '2':
                self.add_product()
            elif choice == '3':
                self.remove_product()
            elif choice == '4':
                self.view_orders()
            elif choice == '5':
                self.remove_order()
            elif choice == '6':
                self.view_sales()
            elif choice == '7':
                print("관리자 화면을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")

    # 사용자 역할 선택
    def role_selection(self):
        while True:
            print("\n1. 고객\n2. 관리자")
            role = input("선택: ")
            if role == '1':
                self.customer_menu()
                break
            elif role == '2':
                admin_code = input("관리자 코드를 입력하세요: ")
                if admin_code == "admin123":  # 관리자 코드
                    self.admin_menu()
                else:
                    print("잘못된 관리자 코드입니다.")
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")


# 프로그램 실행
def main():
    shopping_mall = ShoppingMall()
    shopping_mall.set_date()  # 날짜 설정
    shopping_mall.role_selection()  # 역할 선택

if __name__ == "__main__":
    main()
