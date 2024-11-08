import datetime
import random
import re
import sys

# 주문 클래스
class Order:
    def __init__(self, order_id, product_id, product_name, product_price, quantity, customer_name, customer_address, order_date):
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.order_date = order_date

    def __str__(self):
        return (f"주문번호: {self.order_id}, 상품번호: {self.product_id}, 상품명: {self.product_name}, 가격: {self.product_price}원, "
                f"수량: {self.quantity}, 고객명: {self.customer_name}, 주소: {self.customer_address}, "
                f"주문일: {self.order_date}")

    def to_file_string(self):
        return (f"{self.order_id},{self.product_id},{self.product_name},{self.product_price},{self.quantity},"
                f"{self.customer_name},{self.customer_address},{self.order_date}\n")

    @staticmethod
    def from_file_string(order_str):
        order_data = order_str.strip().split(',')
        return Order(order_data[0], order_data[1], order_data[2], int(order_data[3]), int(order_data[4]), 
                     order_data[5], order_data[6], order_data[7])  # Add order_date as well

# 쇼핑몰 클래스
class ShoppingMall:
    def __init__(self):
        self.orders = []  # 주문 목록
        self.products = {}  # 상품 목록 (상품명: (가격, 수량))
        self.load_items()
        self.load_orders()

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
        elif product_name.isdigit():
            print("\n오류: 잘못된 입력입니다.")
            return False
        return True
    
    def update_product_by_name(self, product_name):
        # Find products matching the given name
        matching_products = {
            product_id: (name, price, quantity)
            for product_id, (name, price, quantity) in self.products.items()
            if product_name.lower() in name.lower()
        }

        # Check if there are matching products
        if not matching_products:
            print("해당 이름의 상품이 없습니다. 다시 확인해 주세요.")
            return

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

        while True:
            # Display options for the user to choose what to update
            print("\n수정할 사항")
            print("\n(1) 상품명")
            print("(2) 가격")
            print("(3) 수량")
            print("(0) 뒤로 가기")
            choice = input("\n메뉴 번호 입력 (0~3): ")

            if choice == '1':
                # Update name
                print("현재 상품명:", matching_products[product_id][0])
                new_name = input("수정할 상품의 이름을 입력하세요: ")
                if new_name:
                    if not self.is_valid_product_name(new_name):
                        continue  # Invalid name, loop back to the options
                    product_name = new_name
                    self.products[product_id] = (product_name, price, quantity)
                    self.save_items()
                    print("수정이 완료되었습니다.")

            elif choice == '2':
                print("현재 가격:", matching_products[product_id][1])
                # Update price with non-negative check
                try:
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
                print("현재 수량:", matching_products[product_id][2])
                # Update quantity with non-negative check
                try:
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
        return re.sub(r'[^a-zA-Z0-9]', '', query)
    
    # Modified search_products function
    def search_products(self, query):
        # Remove spaces from the search query
        query = self.remove_space(query)
        
        # 검색어가 비어 있으면 빈 딕셔너리 반환
        if not query:
            print("\n검색어가 비어 있습니다. 다시 입력하세요.")
            return {}
        
        # 제품을 검색하여 결과를 딕셔너리로 반환
        results = {
            product_id: (name, price, quantity)
            for product_id, (name, price, quantity) in self.products.items()
            if self.remove_space(name.lower()).find(query.lower()) != -1
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
        product_id = input("\n주문할 상품을 선택해 주세요: ")

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
                    quantity = int(input("\n주문할 수량 (0을 입력하면 종료): "))
                    if quantity == 0:
                        print("\n주문을 종료합니다.")
                        return  # 주문 종료
                    if quantity > product_quantity:
                        print("\n주문이 불가능합니다. 수량이 다시 입력해 주세요.")
                        continue  # 수량이 적절하지 않으면 다시 입력받도록 함
                    break
                except ValueError:
                    print("\n수량은 정수로 입력해주세요.")
            
            print(f"주문가능 합니다. 고객 정보 입력 화면으로 넘어갑니다.")   
            print("\n[ 고객 정보 ]") 

            while True:
                #번호 입력 불가, 다시 입력하도록 함
                customer_name = input("고객명: ")
                if not re.match(r'^[a-zA-Z가-힣\s]+$', customer_name):
                    print("오류: 잘못된 입력입니다.")
                    continue
        
                customer_address = input("주소: ")
                if not re.match(r'^[a-zA-Z0-9가-힣\s\-]+$', customer_address):
                    print("오류: 잘못된 입력입니다.")
                    continue

                self.last_order_date = Order.from_file_string(self.orders[-1].to_file_string()).order_date if self.orders else None
                if self.last_order_date is None:
                    # 첫 주문일 경우, 아무 날짜나 입력받도록 허용
                    while True:
                        order_date = input("주문일 (YYYY-MM-DD): ")
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", order_date):
                            self.last_order_date = order_date
                            break
                        else:
                            print("오류: 날짜는 'YYYY-MM-DD' 형식이어야 합니다. 다시 입력하세요.")
                else:
                    # 마지막 주문일이 있을 경우, 그 날짜 이후로만 입력받도록 함, orders.txt 파일에 저장된 마지막 주문일을 읽어옴
                    while True:
                        order_date = input("주문일 (" + str(self.last_order_date) + "~): ")
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", order_date):
                            # 입력된 주문일이 마지막 주문일 이전이면 오류 처리
                            if order_date < self.last_order_date:
                                print("오류: 주문일은 마지막 주문일 이후여야 합니다.")
                            else:
                                # 유효한 날짜 입력되었으면 last_order_date 갱신
                                self.last_order_date = order_date
                                break
                        else:
                            print("오류: 날짜는 'YYYY-MM-DD' 형식이어야 합니다. 다시 입력하세요.")

                print(f"\n입력이 완료되었습니다.")

                #주문 확인
                print("\n주문 상품:" + product_name)
                print("주문 수량:" + str(quantity))
                print("고객명:" + customer_name)
                print("주소:" + customer_address)
                print("주문일:" + str(order_date))
                print("\n주문 정보가 일치합니까?")
                print("\n(1) YES\n(2) NO")
                while True:
                    choice = input("\n선택: ")
                    if choice == '1':
                        
                        order_id = f"ORD{random.randint(1000, 9999)}"  # 고유 주문 ID 생성
                        # 주문 번호 중복 검사
                        if not self.check_id(order_id):
                        # 주문 번호가 중복되면 주문을 종료하거나 다시 입력받도록 처리
                            print("주문 번호가 중복되었습니다")
                            return

                        order = Order(order_id, product_id, product_name, product_price, quantity, customer_name, customer_address, order_date)
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
                        print(f"\n고객명: {customer_name}")
                        print(f"주소: {customer_address}")
                        print(f"주문일: {order_date}")
                        print("\n이용해주셔서 감사합니다.")
                        choice = input("처음으로 돌아가려면 아무 키나 눌러주세요: ")
                        if choice:
                            self.customer_menu()
                        break
                    elif choice == '2':
                        print("주문을 취소되었습니다. 상품 목록 페이지로 넘어갑니다.")
                        self.view_products()
                        self.add_order()
                    else:
                        print("\n오류: 잘못된 입력입니다.")
                        # 주문 추가 실패 후 다시 choice 입력받도록 함
                        continue

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
        if not self.orders:
            print("등록된 주문이 없습니다.")
        else:
            # 헤더 출력
            print(f"{'주문번호':<15} {'고객명':<15} {'주소':<30} {'주문상품명':<15} {'상품번호':<15} {'가격(원)':<15} {'수량':<10} {'주문일':<15}")
            
            for order in self.orders:
                print(f"{order.order_id:<15} {order.customer_name:<15} {order.customer_address:<30} {order.product_name:<15} {order.product_id:<15} {order.product_price:<15} {order.quantity:<10} {order.order_date:<15}")

        # 뒤로 가기 아무나 키나 누르면 이전 화면으로 돌아감
        input_key = input("\n뒤로가기 (아무 키나 입력하세요): ")
        if input_key:
            print("\n이전 화면으로 돌아갑니다.")
            self.admin_menu()


    # 매출 조회
    def view_sales(self):
        total_sales = 0
        print("\n[ 매출 조회 ]")
        print(f"{'상품번호':<15} {'상품명':<15} {'판매량(개)':<15} {'매출(원)':<10}")
        for order in self.orders:
            total_price = order.product_price * order.quantity
            print(f"{order.product_id:<15} {order.product_name:<15} {order.quantity:<15} {total_price:<10}원")
            total_sales += total_price
        print(f"\n총매출(원): {total_sales}")

        input_key = input("\n뒤로가기 (아무 키나 입력하세요): ")
        if input_key:
            print("\n이전 화면으로 돌아갑니다.")
            self.admin_menu()

    # 파일로부터 상품 읽어오기
    def load_items(self):
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
        print(f"\n*((**(: 환영합니다  :) **))*")
        
        # Step 1: Ask if the customer wants to view products
        print("상품 목록을 조회하시겠습니까? \n\n(1) YES \n(2) NO: ")
        
        view_choice = input("\n선택: ")
        if view_choice == '1':
            self.view_products()  # Show products if they choose "YES"
        elif view_choice == '2':
            print("이전 화면으로 돌아갑니다.")
            # return to the role selection menu
            self.role_selection()
        else:
            print("오류 잘못된 입력입니다.")  # Prompt again for valid input

        # Step 2: Only view_choice 1 will proceed to the next step
        if view_choice == '1':
            while True:
                print("\n(1) 상품 검색\n(2) 상품 선택\n(0) 종료")
                choice = input("선택: ")

                if choice == '1':
                    while True:
                        print("상품 검색 화면으로 넘어갑니다.")
                        print("\n[상품 검색]")

                        search_query = input("\n검색어를 입력하세요: ")

                        # Check for empty query
                        if not search_query:
                            print("\n검색어가 비어 있습니다. 다시 입력하세요.")
                            print("\n(1) 다시 검색하기 \n(0) 검색 종료")
                            search_choice = input("선택: ")
                            if search_choice == '1':
                                continue  # Restart search input
                            elif search_choice == '0':
                                self.view_products()
                                break  # Go back to main menu
                            else:
                                print("잘못된 입력입니다. 다시 선택하세요.")
                                continue

                        # Perform search
                        search_results = self.search_products(search_query)
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
                            print("\n(1) 다시 검색하기 \n(0) 검색 종료")
                            search_choice = input("선택: ")
                            if search_choice == '1':
                                continue  # Restart search input
                            elif search_choice == '0':
                                self.view_products()
                                break  # Go back to main menu
                            else:
                                print("잘못된 입력입니다. 다시 선택하세요.")
                    

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


    # 관리자 메뉴
    def admin_menu(self):
        while True:
            print("\n[ 관 리 자 ]")
            print("\n(1) 상품 목록 조회\n(2) 주문 조회\n(3) 매출 조회\n(0) 종료")
            choice = input("\n메뉴 번호 입력 (0~3): ")
            if choice == '1':
                self.manage_products()  # 상품 목록 및 관리
            elif choice == '2':
                self.view_orders()  # 주문 조회
            elif choice == '3':
                self.view_sales()  # 매출 조회
            elif choice == '0':
                print("프로그램이 종료합니다 .")
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
                print("프로그램이 종료 됩니다 .") # 프로그램 종료 
                sys.exit()

            else:
                print("잘못된 입력입니다.")

# 프로그램 실행
if __name__ == "__main__":  
    shopping_mall = ShoppingMall()
    shopping_mall.role_selection()  # 역할 선택
