def print_gugudan():
    print("=================== 구구단 (2단 ~ 9단) ===================")
    # 2단부터 5단까지 가로로 출력
    for row in range(1, 10):
        line1 = []
        for dan in range(2, 6):
            line1.append(f"{dan} x {row} = {dan * row:2d}")
        print("   |   ".join(line1))
    
    print("-" * 58)
    
    # 6단부터 9단까지 가로로 출력
    for row in range(1, 10):
        line2 = []
        for dan in range(6, 10):
            line2.append(f"{dan} x {row} = {dan * row:2d}")
        print("   |   ".join(line2))
    print("==========================================================")

if __name__ == "__main__":
    print_gugudan()
