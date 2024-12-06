import datetime
import random
import re
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict

# 주문 클래스
class Order:
    def __init__(self, order_id, product_id, product_name, product_price, quantity, customer_phone, order_date):
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity
        self.customer_phone = customer_phone
        self.order_date = order_date


    def __str__(self):
        return (f"주문번호: {self.order_id}, 상품번호: {self.product_id}, 상품명: {self.product_name}, 가격: {self.product_price}원, 수량: {self.quantity},"
                f"전화번호: {self.customer_phone}, 주문일: {self.order_date}")

    def to_file_string(self):
        return (f"{self.order_id},{self.product_id},{self.product_name},{self.product_price},{self.quantity},"
                f"{self.customer_phone},{self.order_date}\n")

    @staticmethod
    def from_file_string(order_str):
        order_data = order_str.strip().split(',')
        return Order(order_data[0], order_data[1], order_data[2], int(order_data[3]), int(order_data[4]), order_data[5], order_data[6])

# 쇼핑몰 클래스
class ShoppingMall:
    def __init__(self):
        self.orders = []  # 주문 목록
        self.products = {}  # 상품 목록 (상품명: (가격, 수량))
        self.load_items()
        self.load_orders()

    def sign_up(self):
        is_first_user = not os.path.exists('users.txt') # Check if it's the first user
        while True:
            name = input("이름을 입력하세요: ")
            if not re.match(r'^[a-zA-Z가-힣\s]+$', name):
                print("오류: 잘못된 입력입니다.")
                continue

            passport = input("비밀번호를 입력하세요 (4-8개 숫자): ")
            if not passport.isdigit() or not (4 <= len(passport) <= 8):
                print("불가능한 비밀번호입니다. 다시 입력하세요.")
                continue

            phone = input("전화번호를 입력하세요 (010-xxxx-xxxx): ")
            if not re.match(r"010-\d{4}-\d{4}", phone):
                print("불가능한 전화번호입니다. 다시 입력하세요.")
                continue

            if not is_first_user:
                # Check for duplicate phone numbers
                with open('users.txt', 'r', encoding='utf-8') as f:
                    users = f.readlines() # Skip header line, if present
                if any(phone == user.strip().split(',')[2] for user in users):
                    print("이미 등록된 전화번호입니다. 다른 번호를 입력하세요.")
                    continue

            address = input("주소를 입력하세요: ").strip()
            if address.isdigit():
                print("오류: 주소는 숫자로만 입력할 수 없습니다.")
                continue
            if not re.match(r'^[a-zA-Z0-9가-힣\s\-]+$', address):
                print("오류: 잘못된 입력입니다.")
                continue

            # Append the new user to the file
            with open('users.txt', 'a', encoding='utf-8') as f:
                f.write(f"{name},{passport},{phone},{address}\n")
            print("회원가입 완료됐습니다!")


    def login(self):
        phone = input("아이디를 입력하세요 (010-xxxx-xxxx): ")
        passport = input("비밀번호를 입력하세요: ")
        with open('users.txt', 'r', encoding='utf-8') as f:
            users = f.readlines()  # Skip header
        for user in users:
            name, saved_passport, saved_phone, saved_address = user.strip().split(',')
            if phone == saved_phone and passport == saved_passport:
                print(f"환영합니다, {name}!")
                self.current_user = {
                'name': name,
                'passport': saved_passport,
                'phone': saved_phone,
                'address': saved_address
                }
                self.get_current_date()
                return True
        print("아이디 또는 비밀번호가 틀렸습니다.")
        return False

    def check_id(self, product_id):
        #상품 번호가 이미 등록된 상품 번호와 중복되는지 확인하는 함수
        if product_id in self.products:
            print(f"오류: 상품 번호 '{product_id}'는 이미 존재합니다.")
            return False  # 중복된 상품번호가 있으면 False 반환
        return True  # 중복되지 않으면 True 반환

    def add_product(self):
        while True:
            product_name = input("상품명: ")

            if product_name == "0":
                    return

            # Validate the product name, and re-prompt until valid
            while not self.is_valid_product_name(product_name):
                product_name = input("상품명: ")

            try:
                # Ensure the price is a positive integer
                product_price = int(input("가격 (원): "))
                if product_price < 0:
                    print("가격은 음수일 수 없습니다. 다시 입력해주세요.")
                    continue

                # Ensure the quantity is a positive integer
                product_quantity = int(input("수량 (개): "))
                if product_quantity < 0:
                    print("수량은 음수일 수 없습니다. 다시 입력해주세요.")
                    continue


                product_id = f"PROD{random.randint(1000, 9999)}"
                if not self.check_id(product_id):
                    break  # Unique ID found, break the loop

                # Register the product
                self.products[product_id] = (product_name, product_price, product_quantity)
                print(f"상품 번호 '{product_id}'")
                print("상품 등록이 완료되었습니다.")

                # Save the product information to file
                self.save_items()
                break  # Exit the loop after successful registration

            except ValueError:
                print("\n입력 오류: 가격과 수량은 정수만 입력 가능합니다. 다시 시도해주세요.")


    def is_valid_product_name(self, product_name):
        # If the product name is '0', show a return message without error
        if product_name == "0":
            print("\n이전 화면으로 돌아갑니다.")
            return False
        # If the product name is any other number, show an error message
        if product_name.isdigit():
            print("\n오류: 잘못된 입력입니다.")
            return False

        if not re.search(r'[a-zA-Z0-9가-힣]', product_name):
            print("\n오류: 상품명은 특수문자나 공백만으로 이루어질 수 없습니다.")
            return False
        return True

    def update_product_by_name(self, product_name):
        # Find products matching the given name

            self.load_items()
            matching_products = {
                product_id: (name, price, quantity)
                for product_id, (name, price, quantity) in self.products.items()
                if product_name.lower() in name.lower()
            }

            # Check if there are matching products
            if not matching_products:
                print("해당 이름의 상품이 없습니다. 다시 확인해 주세요.")
                return
            if len(matching_products) == 1:
                product_id, (product_name, price, quantity) = next(iter(matching_products.items()))
            else:
                # Display the matching products
                print("\n[ 검색 결과 ]")
                print(f"\n{'상품번호':<15} {'상품명':<15} {'가격(단위: 원)':<15} {'수량(단위: 개)':<10}")
                for product_id, (name, price, quantity) in matching_products.items():
                    print(f"{product_id:<15} {name:<15} {price:<15} {quantity:<10}")

                # Ask for the specific product ID to edit
                product_id = input("\n수정할 상품번호를 입력하세요: ")

                if len(product_id) == 4 and product_id.isdigit():
                    product_id = 'PROD' + product_id

                if product_id not in matching_products:
                    print("유효하지 않은 상품 번호입니다.")
                    return


                # Display options for the user to choose what to update
            while True:
                print("\n수정할 사항")
                print("\n(1) 상품명")
                print("(2) 가격")
                print("(3) 수량")
                print("(0) 뒤로 가기")
                choice = input("\n메뉴 번호 입력 (0~3): ")

                if choice == '1':

                    try:
                        # Update name
                        print(f"현재 상품명: {matching_products[product_id][0]}")
                        new_name = input("새로운 상품명 (변경하지 않으려면 Enter): ")
                        if new_name:
                            if not self.is_valid_product_name(new_name):
                                continue  # Invalid name, loop back to the options
                            product_name = new_name
                            self.products[product_id] = (product_name, price, quantity)
                            self.save_items()
                            print("수정이 완료되었습니다.")

                    except ValueError:
                        print("상품명은 문자열만 입력 가능합니다.")

                elif choice == '2':

                    # Update price with non-negative check
                    try:
                        print(f"현재 가격: {matching_products[product_id][1]}")
                        new_price = input("새로운 가격 (변경하지 않으려면 Enter): ")
                        if new_price:
                            new_price = int(new_price)
                            if new_price < 0:
                                print("가격은 음수일 수 없습니다. 다시 입력해주세요.")
                                continue
                            price = new_price
                            self.products[product_id] = (product_name, price, quantity)
                            self.save_items()

                            print("수정이 완료되었습니다.")

                    except ValueError:
                        print("가격은 숫자만 입력 가능합니다.")

                elif choice == '3':

                    # Update quantity with non-negative check
                    try:
                        print(f"현재 수량: {matching_products[product_id][2]}")
                        new_quantity = input("새로운 수량 (변경하지 않으려면 Enter): ")
                        if new_quantity:
                            new_quantity = int(new_quantity)
                            if new_quantity < 0:
                                print("수량은 음수일 수 없습니다. 다시 입력해주세요.")
                                continue
                            quantity = new_quantity
                            self.products[product_id] = (product_name, price, quantity)
                            self.save_items()
                            print("수정이 완료되었습니다.")
                    except ValueError:
                        print("수량은 숫자만 입력 가능합니다.")

                elif choice == '0':
                    print("이전 화면으로 돌아갑니다.")
                    break


                else:
                    print("잘못된 입력입니다. 다시 선택하세요.")
                    break


    def remove_product_by_name(self, product_name):
        # Find products matching the given name
        matching_products = {
            product_id: (name, price, quantity)
            for product_id, (name, price, quantity) in self.products.items()
            if product_name.lower() in name.lower()
        }

        # Check if there are matching products
        if not matching_products:
            print("상품이 존재하지 않습니다. 이전 화면으로 돌아갑니다.")
            return

        # Display the matching products
        print("\n< 검색 결과 >")
        print(f"{'상품번호':<15} {'상품명':<15} {'가격(단위: 원)':<15} {'수량(단위: 개)':<10}")
        for product_id, (name, price, quantity) in matching_products.items():
            print(f"{product_id:<15} {name:<15} {price:<15} {quantity:<10}")

        # Ask for the specific product ID to delete
        product_id = input("\n단종할 상품번호를 입력하세요(뒤로가기 0): ")

        if len(product_id) == 4 and product_id.isdigit():
            product_id = 'PROD' + product_id

        if product_id == '0':
            print("\n이전 화면으로 돌아갑니다.")
            return

        if product_id not in matching_products:
            print("\n해당 상품이 존재하지 않습니다. 이전 화면으로 돌아갑니다.")
            return

        #Delete the product

        del self.products[product_id]
        print(f"단종 등록 완료하였습니다.")
        self.save_items()  # Save the updated product list to file


    # 상품 목록 조회
    def view_products(self):
        if not self.products:
            print("등록된 상품이 없습니다.")
        else:
            print("\n[상품 목록]")
            print(f"\n{'상품 번호':<15} {'상품명':<15} {'가격 (단위 : 원)':<15} {'수량(단위 : 개)':<10}")

            for product_id, (product_name, price, quantity) in self.products.items():
                print(f"{product_id:<15} {product_name:<15} {price:<15} {quantity:<10}")

    def remove_space(self, query):
    # 공백만 있는 경우 검사
        if query.strip() == '':
            return None, "empty"

        # 특수문자 검사 (알파벳, 숫자, 한글, 공백 제외한 문자)
        if re.search(r'[^\w\s가-힣]', query):
            return None, "special"

        # 검색 가능한 경우
        return query, "valid"


    def search_products(self, query):
        query, signal = self.remove_space(query)

        if signal == "empty":
            print("\n검색어가 비어 있습니다. 다시 입력하세요.")
            return None
        elif signal == "special":
            print("\n특수문자를 입력할 수 없습니다.")
            return None

        # 검색 로직
        results = {
            product_id: (name, price, quantity)
            for product_id, (name, price, quantity) in self.products.items()
            if query.lower() in name.lower() or query.lower() in name.lower().replace(' ', '')
        }

        return results


    # 관리자용 상품 관리
    def manage_products(self):
        while True:
            self.view_products()
            print("\n(1) 상품 등록\n(2) 상품 수정\n(3) 단종 등록\n(0) 뒤로가기")
            choice = input("메뉴 번호 입력 (0~3): ")
            if choice == '1':
                print("\n[ 상품 등록 ]")
                self.add_product()  # 상품 추가
            elif choice == '2':
                print("\n[ 상품 수정 ]")
                product_name = input("수정할 상품명을 입력하세요 : ")
                self.update_product_by_name(product_name)  # 상품 수정
            elif choice == '3':
                print("[ 단종 등록 ]")
                product_name = input("단종할 상품명을 입력하세요 : ")
                self.remove_product_by_name(product_name)  # 상품 삭제
            elif choice == '0':
                print("이전 화면으로 돌아갑니다.")
                return
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")

    # 주문 추가 (고객용)
    def add_order(self):
        product_id = input("\n주문할 상품 번호를 입력해 주세요: ")

        if len(product_id) == 4 and product_id.isdigit():
            product_id = 'PROD' + product_id

        if product_id == '0':
            print("주문을 종료합니다.")
            return  # 주문 종료

        if product_id in self.products:
            product_name, product_price, product_quantity = self.products[product_id]

            if product_quantity == 0:
                print("주문 수량이 없어 주문이 불가합니다. 다른 상품을 선택하세요.")
                # 상품을 다시 선택하도록 루프의 시작으로 돌아감
                return

            while True:
                try:
                    quantity_input = input("\n주문할 수량 (0을 입력하면 종료): ").strip()
                    if not quantity_input or quantity_input.isspace():
                        print("오류: 수량은 공백만 입력할 수 없습니다. 다시 입력하세요.")
                        continue
                    if quantity_input == '0':
                        print("\n주문을 종료합니다. 이전 화면으로 돌아갑니다.")
                        return  # 검색 메뉴로 돌아감
                    if not quantity_input.isdigit() or int(quantity_input) <= 0:
                        print("오류: 수량은 1 이상의 정수만 입력 가능합니다. 다시 입력하세요.")
                        continue

                    quantity = int(quantity_input)
                    if quantity > product_quantity:
                        print("\n주문이 불가능합니다. 수량을 다시 입력해 주세요.")
                        continue
                    break
                except ValueError:
                    print("\n수량은 정수로 입력해주세요.")


            order_id = f"ORD{random.randint(1000, 9999)}"  # 고유 주문 ID 생성
            # 주문 번호 중복 검사
            if not self.check_id(order_id):
            # 주문 번호가 중복되면 주문을 종료하거나 다시 입력받도록 처리
                print("주문 번호가 중복되었습니다")
                return
            order_date = self.current_user.get('order_date')
            order = Order(order_id, product_id, product_name, product_price, quantity, self.current_user['phone'], order_date)
            self.orders.append(order)

            # 상품 수량 업데이트
            new_quantity = product_quantity - quantity
            self.products[product_id] = (product_name, product_price, new_quantity)  # 수량 업데이트
            print(f"주문이 완료되었습니다. 주문 완료 페이지로 넘어갑니다.")

            # 파일에 주문과 상품 정보 저장
            self.save_orders()
            self.save_items()  # 상품 정보도 함께 저장
            self.save_sales(order)  # 매출 정보 저장
            # 주문 추가 완료 후 루프 종료
            print("\n[ 주문 완료 ]")
            print(f"주문번호: {order_id}")
            print(f"상품명: {product_name}")
            print(f"수량: {quantity}")
            print(f"금액: {product_price * quantity}원")
            print("\n이용해주셔서 감사합니다.")
            choice = input("처음으로 돌아가려면 아무 키나 눌러주세요: ")
            if choice:
                self.giving_order_page()

        else:
            print("유효하지 않은 상품번호 입니다.")
            #다시 입력하도록 함
            self.add_order()


    # 매출 정보 저장
    def save_sales(self, order):
        with open('sales.txt', 'a', encoding='utf-8') as f:
            total_price = order.product_price * order.quantity
            f.write(f"{order.product_id},{order.product_name},{order.quantity},{total_price}원\n")


    # 주문 목록 출력
    def view_orders(self):
        print("\n[ 주문 조회 ]")

        # Check if there are any orders
        if not self.orders:
            print("등록된 주문이 없습니다.")
            return

        # Load return counts from returns.txt
        returned_counts = {}
        try:
            with open('returns.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    order_id, _, quantity, _, _ = line.strip().split(',')
                    returned_counts[order_id] = returned_counts.get(order_id, 0) + int(quantity)
        except FileNotFoundError:
            pass  # If returns.txt doesn't exist, all return counts are assumed to be 0

        # Display the header
        print(f"{'주문번호':<15} {'주문상품명':<15} {'상품번호':<15} {'가격(원)':<15} {'수량':<10} {'주문일':<15} {'고객 아이디':<15} {'반품 회수':<10}")

        # Display each order with its return count
        for order in self.orders:
            # Get the return count from returned_counts, defaulting to 0 if not found
            return_count = returned_counts.get(order.order_id, 0)
            print(f"{order.order_id:<15} {order.product_name:<15} {order.product_id:<15} {order.product_price:<15} "
                f"{order.quantity:<10} {order.order_date:<15} {order.customer_phone:<15} {return_count:<10}")

        # Wait for user input to return to the previous screen
        input_key = input("\n뒤로가기 (아무 키나 입력하세요): ")
        if input_key:
            print("\n이전 화면으로 돌아갑니다.")
            self.admin_menu()



    # 매출 조회
    def view_sales(self):
        total_sales = 0
        sales_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0, 'returns': 0})

        print("\n[ 매출 조회 ]")

        # Load returned quantities from returns.txt
        try:
            with open('returns.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    order_id, product_name, quantity, return_date, customer_phone = line.strip().split(',')
                    # Find the product_id for the returned product
                    product_id = next((order.product_id for order in self.orders if order.order_id == order_id), None)
                    if product_id:
                        sales_data[product_id]['returns'] += int(quantity)
        except FileNotFoundError:
            pass  # No returns, continue

        # Process each order
        for order in self.orders:
            product_id = order.product_id
            returned_quantity = sales_data[product_id]['returns']
            net_quantity = order.quantity
            if net_quantity > 0 or returned_quantity > 0:  # Include products with sales or returns
                revenue = (net_quantity - returned_quantity) * order.product_price
                sales_data[product_id]['quantity'] += net_quantity
                sales_data[product_id]['revenue'] += revenue
                total_sales += revenue

        # Display the sales table
        print(f"{'상품번호':<15} {'상품명':<15} {'판매량(개)':<15} {'반품량(개)':<15} {'매출(원)':<10}")
        for product_id, data in sales_data.items():
            product_name = next((order.product_name for order in self.orders if order.product_id == product_id), "N/A")
            print(f"{product_id:<15} {product_name:<15} {data['quantity']:<15} {data['returns']:<15} {data['revenue']:<10}원")

        print(f"\n총매출(원): {total_sales}")

        # Wait for user input to return to the previous menu
        input_key = input("\n뒤로가기 (아무 키나 입력하세요): ")
        if input_key:
            print("\n이전 화면으로 돌아갑니다.")


    # 파일로부터 상품 읽어오기
    def load_items(self):
        self.products.clear()
        try:
            with open('products.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():  # Check if the line is not empty
                        product_id, product_name, product_price, product_quantity,  = line.strip().split(',')
                        self.products[product_id] = (product_name, int(product_price), int(product_quantity))

        except FileNotFoundError:
            pass  # File not found, do nothing
        except ValueError:
            print("파일 형식이 잘못되었습니다. 상품 정보를 확인하세요.")  # Handle incorrect format

    def save_items(self):
        with open("products.txt", "w", encoding="utf-8") as file:
            for product_id, (name, price, quantity) in self.products.items():
                #상품 이름에 공백이 포함되어 있으면 없어버리고 저장
                file.write(f"{product_id},{name},{price},{quantity}\n")

    # 파일로부터 주문 읽어오기
    def load_orders(self):
        try:
            with open('orders.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        order = Order.from_file_string(line)  # Parse each order
                        self.orders.append(order)
        except FileNotFoundError:
            pass
        except ValueError:
            print("파일 형식이 잘못되었습니다. 주문 정보를 확인하세요.")


    # 주문 정보를 파일에 저장
    def save_orders(self):
        with open('orders.txt', 'w', encoding='utf-8') as f:
            for order in self.orders:
                f.write(order.to_file_string())

    # 고객 메뉴
    def customer_menu(self):
        print("\n[고객]")
        while True:
            print("\n(1) 회원가입\n(2) 로그인\n(0) 이전 화면으로 돌아가기")
            choice = input("\n메뉴 번호 입력 (0~2): ")
            if choice == '1':
                self.sign_up()
            elif choice == '2':
                if self.login():
                    while True:
                        print(f"\n(1) 주문하기\n(2) 반품하기\n(0) 이전 화면으로 돌아가기")
                        choice = input("선택: ")
                        if choice == '1':
                            self.giving_order_page()
                        elif choice == '2':
                            self.return_product()
                        elif choice == '0':
                            print("이전 화면으로 돌아갑니다.")
                            break
                        else:
                            print("잘못된 입력입니다. 다시 선택하세요.")
            elif choice == '0':
                print("첫 화면으로 돌아갑니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")

    def get_current_date(self):
        #날짜를 orders.txt 파일에 저장된 마지막 주문일 이후로만 입력받도록 함
        last_order_date = Order.from_file_string(self.orders[-1].to_file_string()).order_date if self.orders else None
        if last_order_date is None:
            # 첫 주문일 경우, 아무 날짜나 입력받도록 허용
            while True:
                user_date = input("날짜를 입력하세요 (YYYY-MM-DD): ")
                if re.match(r"^\d{4}-\d{2}-\d{2}$", user_date):
                    self.current_user['order_date'] = user_date
                    break
                else:
                    print("오류: 날짜는 'YYYY-MM-DD' 형식이어야 합니다. 다시 입력하세요.")
            print(f"입력이 완료되었습니다.")
        else:
            # 마지막 주문일이 있을 경우, 그 날짜 이후로만 입력받도록 함, orders.txt 파일에 저장된 마지막 주문일을 읽어옴
            while True:
                user_date = input("이전 날짜 (" + str(last_order_date) + "~): ")
                if re.match(r"^\d{4}-\d{2}-\d{2}$", user_date):
                    # 입력된 주문일이 마지막 주문일 이전이면 오류 처리
                    if user_date < last_order_date:
                        print("오류: 주문일은 마지막 주문일 이후여야 합니다.")
                    else:
                        # 유효한 날짜 입력되었으면 last_order_date 갱신
                        self.current_user['order_date'] = user_date
                        break
                else:
                    print("오류: 날짜는 'YYYY-MM-DD' 형식이어야 합니다. 다시 입력하세요.")
            print(f"입력이 완료되었습니다.")

    def giving_order_page(self):

        # Load return attempts from returns.txt
        return_attempts = []
        try:
            with open('returns.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    order_id, _, quantity, return_date, customer_phone = line.strip().split(',')
                    if customer_phone == self.current_user['phone']:
                        return_attempts.append(datetime.strptime(return_date, "%Y-%m-%d"))
        except FileNotFoundError:
            pass  # No return attempts if returns.txt doesn't exist

        # Parse the current user's order date into a datetime object
        current_date_str = self.current_user.get('order_date')
        try:
            current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        except (TypeError, ValueError):
            print("유효하지 않은 날짜 형식입니다. 관리자에게 문의하세요.")
            return

         # Filter return attempts within the last 7 days
        recent_returns = [date for date in return_attempts if (current_date - date).days < 7]

        # Check if the customer has exceeded the limit
        if len(recent_returns) > 3:
            print("\n[ 오류 ]")
            print("최근 7일 동안 3회 이상의 반품 기록이 있습니다. 주문이 제한됩니다.")
            print("이전 화면으로 돌아갑니다.")
            return  # Exit to the previous menu

        # Step 1: Ask if the customer wants to view products
        print("\n상품 목록을 조회하시겠습니까? \n\n(1) YES \n(2) NO")

        view_choice = input("\n선택: ")
        if view_choice == '1':
            self.view_products()  # Show products if they choose "YES"
        elif view_choice == '2':
            print("이전 화면으로 돌아갑니다.")
            # return to the role selection menu
            return
        else:
            print("오류 잘못된 입력입니다.")  # Prompt again for valid input

        # Step 2: Only view_choice 1 will proceed to the next step
        if view_choice == '1':
            while True:
                print("\n(1) 상품 검색\n(2) 상품 선택\n(0) 종료")
                choice = input("선택: ")

                if choice == '1':
                    self.load_items()
                    search_choice_save = ''
                    while True:
                        if search_choice_save == '0':
                            break
                        print("상품 검색 화면으로 넘어갑니다.")
                        print("\n[상품 검색]")

                        search_query = input("\n검색어를 입력하세요: ")
                        search_results = self.search_products(search_query)
                    # while True:
                        if search_results == None:
                            print("\n(1) 다시 검색하기 \n(0) 검색 종료")
                            search_choice = input("선택: ")
                            if search_choice == '1':
                                continue  # Restart search input
                            elif search_choice == '0':
                                self.view_products()
                                search_choice_save = search_choice
                                break  # Go back to main menu
                            else:
                                print("잘못된 입력입니다. 다시 선택하세요.")
                                continue
                        if search_results:
                            print(f"\n해당되는 데이터가 {len(search_results)}개 있습니다.")
                            print(f"\n{'상품 번호':<15} {'상품명':<15} {'가격 (단위 : 원)':<15} {'수량 (단위 : 개)':<10}")
                            for product_id, (name, price, quantity) in search_results.items():
                                print(f"{product_id:<15} {name:<15} {price:<15} {quantity:<10}")

                            print("\n(1) 상품 주문하기 \n(2) 다시 검색하기 \n(0) 검색 종료")
                            search_choice = input("선택: ")
                            if search_choice == '1':
                                self.add_order()
                                break  # Exit to main menu after order
                            elif search_choice == '2':
                                continue  # Restart search input
                            elif search_choice == '0':
                                self.view_products()
                                break  # Go back to main menu
                            else:
                                print("잘못된 입력입니다. 다시 선택하세요.")
                        else:
                            print("\n해당되는 데이터가 없습니다.")
                            search_choice = ''
                            while search_choice != '1' or '0':
                                print("\n(1) 다시 검색하기 \n(0) 검색 종료")
                                search_choice = input("선택: ")
                                if search_choice == '1':
                                    search_choice_save = '1';
                                    break  # Restart search input
                                elif search_choice == '0':
                                    search_choice_save = '0'
                                    self.view_products()
                                    break
                                else:
                                    print("잘못된 입력입니다. 다시 선택하세요.")
                                    continue
                elif choice == '2':
                    print("상품 선택 화면으로 넘어갑니다.")
                    print("\n[상품 선택]")
                    self.view_products()
                    self.add_order()  # Proceed to order selection

                elif choice == '0':
                    print("이전 화면으로 돌아갑니다.")
                    break
                else:
                    print("잘못된 입력입니다. 다시 선택하세요.")

    def return_product(self):
        print("\n[반품 가능한 주문 목록]")
        # Parse the current user's return date as a datetime object
        return_date_str = self.current_user.get('order_date')
        try:
            return_date = datetime.strptime(return_date_str, "%Y-%m-%d")
        except (TypeError, ValueError):
            print("유효하지 않은 날짜 형식입니다. 관리자에게 문의하세요.")
            return

        returned_quantities = {}
        try:
            with open('returns.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    order_id, _, quantity, _, customer_phone = line.strip().split(',')
                    if customer_phone == self.current_user['phone']:
                        returned_quantities[order_id] = returned_quantities.get(order_id, 0) + int(quantity)
        except FileNotFoundError:
            pass  # No previous returns, continue

        eligible_orders = []
        for order in self.orders:
            if order.customer_phone != self.current_user['phone']:
                continue
            try:
                # Parse the order date as a datetime object
                order_date = datetime.strptime(order.order_date, "%Y-%m-%d")
                # Check if the order date is within the last 7 days
                if (return_date - order_date).days < 7:
                    returned_quantity = returned_quantities.get(order.order_id, 0)
                    adjusted_quantity = order.quantity - returned_quantity  # Deduct returned quantity
                    if adjusted_quantity >= 1:
                      eligible_orders.append((order, returned_quantity, adjusted_quantity))
            except (TypeError, ValueError):
                print(f"유효하지 않은 주문 날짜: {order.order_date}")
                continue

        # Check if there are any orders
        if not eligible_orders:
            print("반품 가능한 주문 내역이 없습니다.")
            return

        # Display the orders in a table format
        print(f"{'번호':<5} {'주문번호':<15} {'주문상품명':<15} {'상품번호':<15} {'가격(원)':<10} {'수량':<8} {'주문일':<15} {'반품 회수':<10}")
        for idx, (order, returned_quantity, adjusted_quantity) in enumerate(eligible_orders, 1):
            print(f"{idx:<5} {order.order_id:<15} {order.product_name:<15} {order.product_id:<15} "
                  f"{order.product_price:<10} {adjusted_quantity:<8} {order.order_date:<15} {returned_quantity:<10}")

        # Let the user select an order to return
        input_order_number = input("\n반품할 주문번호를 선택하세요 (0을 입력하면 취소): ").strip()
        if input_order_number == 0:
            print("반품이 취소되었습니다.")
            return
        # Locate the selected order by numeric portion of the order_id
        selected_order_tuple = next(
            ((order, returned_quantity, adjusted_quantity) for order, returned_quantity, adjusted_quantity in eligible_orders if order.order_id[3:] == input_order_number),
            None
        )
        if not selected_order_tuple:
            print("유효하지 않은 주문번호입니다. 다시 시도해주세요.")
            return

        selected_order, returned_quantity, adjusted_quantity = selected_order_tuple

        try:
            # Ask the user how many units they want to return
            quantity_to_return = int(input(f"\n'{selected_order.product_name}'의 반품 수량을 입력하세요: "))
            if quantity_to_return <= 0 or quantity_to_return > adjusted_quantity:
                print("잘못된 수량입니다. 다시 시도해주세요.")
                return
        except ValueError:
            print("유효한 숫자를 입력하세요.")
            return

        # Confirm the return with the user
        confirm = input(f"\n'{selected_order.product_name}' {quantity_to_return}개를 반품 처리하시겠습니까? (예/아니오): ").strip().lower()
        if confirm not in ['예', 'y', 'yes']:
            print("반품이 취소되었습니다.")
            return

        # Update return record in returns.txt
        try:
            with open('returns.txt', 'a', encoding='utf-8') as f:
                f.write(f"{selected_order.order_id},{selected_order.product_name},{quantity_to_return},{return_date.strftime('%Y-%m-%d')},{self.current_user['phone']}\n")
        except IOError:
            print("반품 기록을 저장하는 동안 오류가 발생했습니다.")
            return

        # Update the inventory for the returned product
        product_id = selected_order.product_id
        if product_id in self.products:
            product_name, product_price, product_quantity = self.products[product_id]
            self.products[product_id] = (product_name, product_price, product_quantity + quantity_to_return)
            print(f"'{selected_order.product_name}'의 {quantity_to_return}개가 반품 처리되었습니다.")
        else:
            print(f"상품 번호 '{product_id}'가 존재하지 않습니다. 반품 처리가 완료되지 않았습니다.")
            return

        # Save the updated inventory
        self.save_items()

    # 관리자 메뉴
    def admin_menu(self):
        while True:
            print("\n[ 관 리 자 ]")
            print("\n(1) 상품 목록 조회\n(2) 주문 조회\n(3) 매출 조회\n(0) 이전 화면으로 돌아가기")
            choice = input("\n메뉴 번호 입력 (0~3): ")
            if choice == '1':
                self.manage_products()  # 상품 목록 및 관리
            elif choice == '2':
                self.view_orders()  # 주문 조회
            elif choice == '3':
                self.view_sales()  # 매출 조회
            elif choice == '0':
                print("이전 화면으로 돌아갑니다.")
                break
            else:
                print("오류 : 잘못된 입력입니다 .")

    # 사용자 역할 선택
    def role_selection(self):
        while True:
            print("\n[ 쇼 핑 몰 ]")
            print("\n(1) 관리자 페이지\n(2) 고객 페이지\n(0) 종료")
            role = input("이용하실 서비스를 선택해주세요 (0~2): ")
            if role == '2':
                self.customer_menu()  # 고객 메뉴로 이동
            elif role == '1':
                while True:
                    admin_code = input("관리자 코드 : ")
                    if admin_code == '0':
                        print("첫 화면으로 돌아갑니다.")
                        break  # 관리자 코드 입력을 종료하고 상위 메뉴로 돌아감
                    elif admin_code == "1234":  # 관리자 코드 수정
                        self.admin_menu()  # 관리자 메뉴로 이동
                        break
                    else:
                        print("잘못된 코드입니다.")
            elif role == '0':
                print("프로그램이 종료 됩니다.") # 프로그램 종료
                sys.exit()
            else:
                print("잘못된 입력입니다.")

# 프로그램 실행
if __name__ == "__main__":
    shopping_mall = ShoppingMall()
    shopping_mall.role_selection()  # 역할 선택