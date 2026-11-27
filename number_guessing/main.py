import os
import random

MIN_NUM = 1                 # 맞혀야 하는 숫자의 범위 (MIN_NUM ~ MAX_NUM)
MAX_NUM = 100
MAX_TRIES = 7               # 이 횟수 안에 못 맞히면 GAME OVER
PROMPT = "  > "             # 사용자 입력 칸 표시 (모든 화면에서 동일)

WIDTH = 62                  # 화면 가운데 정렬의 기준이 되는 폭
LINE = "  " + "═" * WIDTH   # 화면을 나누는 가로줄


# ───────────────────────────── 화면 출력 ─────────────────────────────

def clear():
    os.system("cls")


def ask():
    # 모든 입력 칸은 같은 모양(PROMPT)으로 보이게 한다. 앞뒤 공백은 지운다.
    return input(PROMPT).strip()


def width(text):
    # 화면에서 차지하는 칸 수: 한글은 2칸, 그 밖의 글자(영어, 숫자, ═ ★ 같은 기호)는 1칸
    total = 0
    for c in text:
        if "가" <= c <= "힣":    # 한글 글자는 '가'부터 '힣'까지 순서대로 들어 있다
            total = total + 2
        else:
            total = total + 1
    return total


def pad_left(text, size):
    # 글자 앞에 공백을 붙여 size칸으로 맞춤 (오른쪽 정렬)
    return " " * (size - width(text)) + text


def margin(size):
    # size칸짜리 글자를 가로줄(LINE)의 가운데에 놓으려면 앞에 몇 칸을 띄울까?
    # 가로줄 앞의 공백 2칸 + 남는 칸의 절반
    return " " * (2 + (WIDTH - size) // 2)


def center(text):
    # 한 줄을 가운데 정렬해서 출력
    print(margin(width(text)) + text)


def center_block(lines):
    # 여러 줄을 '가장 긴 줄' 기준으로 한꺼번에 가운데 정렬 (줄 맞춤이 유지됨)
    longest = 0
    for line in lines:
        if width(line) > longest:
            longest = width(line)
    for line in lines:
        print(margin(longest) + line)


def show_title():
    # 게임 타이틀 화면 (r"..." 은 \ 를 글자 그대로 쓰게 해 주는 문자열)
    print()
    print(LINE)
    print()
    center_block([
        r"     _    ___ ____  _   _ ___ _____ _____ ",
        r"    / \  |_ _/ ___|| | | |_ _|  ___|_   _|",
        r"   / _ \  | |\___ \| |_| || || |_    | |  ",
        r"  / ___ \ | | ___) |  _  || ||  _|   | |  ",
        r" /_/   \_\___|____/|_| |_|___|_|     |_|  ",
    ])
    print()
    center("★  숫자 맞추기  G A M E  ★")
    print()
    print(LINE)
    print()
    center("S : 시작하기      Q : 종료하기")
    print()


# ───────────────────────────── 게임 규칙 ─────────────────────────────

def check_guess(text):
    # 입력이 올바르면 빈 글자(""), 잘못되었으면 이유를 글자로 돌려준다
    if not text.isdigit():
        return "숫자만 입력해 주세요."
    number = int(text)
    if number < MIN_NUM or number > MAX_NUM:
        return str(MIN_NUM) + "부터 " + str(MAX_NUM) + " 사이의 숫자를 입력해 주세요."
    return ""


def hint(guess, answer):
    # 입력한 숫자가 정답보다 작으면 UP(더 큰 수를 불러라), 크면 DOWN
    if guess < answer:
        return "UP   ▲  (더 큰 수)"
    if guess > answer:
        return "DOWN ▼  (더 작은 수)"
    return "정답!"


def show_status(used, low, high):
    # 화면 맨 위에 항상 보이는 표시줄: 남은 기회는 ♥, 쓴 기회는 ♡, 그리고 정답이 있을 수 있는 범위
    left = MAX_TRIES - used
    print()
    print(LINE)
    center("기회   " + "♥" * left + "♡" * used + "   (" + str(left) + "번 남음)")
    print()
    center("정답은  " + str(low) + " ~ " + str(high) + "  사이")
    print(LINE)


def show_history(history):
    for i in range(len(history)):
        print("  " + pad_left(str(i + 1), 2) + "회   " + pad_left(str(history[i][0]), 3) + "   →   " + history[i][1])


# ───────────────────────────── 숫자 맞추기 ─────────────────────────────

def intro():
    # 안내사항을 보여주고 Enter를 기다린다
    print()
    print(LINE)
    center("♣  게 임 안 내  ♣")
    print(LINE)
    print()
    center_block([
        "▶ 컴퓨터가 " + str(MIN_NUM) + "부터 " + str(MAX_NUM) + " 사이의 숫자 하나를 정했습니다.",
        "▶ 숫자를 입력하고 Enter를 누르면 힌트가 나옵니다.",
        "▶ UP ▲ : 정답이 입력한 숫자보다 큽니다.",
        "▶ DOWN ▼ : 정답이 입력한 숫자보다 작습니다.",
        "▶ " + str(MAX_TRIES) + "번 안에 맞히면 승리!",
    ])
    print()
    print(LINE)
    print()
    center("Enter를 누르면 게임을 시작합니다.")
    print()
    ask()


def play():
    answer = random.randint(MIN_NUM, MAX_NUM)    # MIN_NUM 이상 MAX_NUM 이하의 정수 하나
    history = []        # 지금까지의 도전 기록: [입력한 숫자, 힌트 글자]
    low = MIN_NUM       # 정답이 있을 수 있는 가장 작은 수
    high = MAX_NUM      # 정답이 있을 수 있는 가장 큰 수
    message = ""        # 잘못 입력했을 때 보여줄 안내 글
    solved = False

    while len(history) < MAX_TRIES and not solved:
        clear()
        show_status(len(history), low, high)
        print()
        show_history(history)
        if len(history) == 0:
            print("  아직 도전 기록이 없습니다.")
        print()
        if message != "":
            print("  ※ " + message)
            message = ""
        print("  ◇ " + str(MIN_NUM) + "~" + str(MAX_NUM) + " 사이의 숫자를 입력하세요.\n")

        text = ask()
        message = check_guess(text)
        if message == "":    # 올바른 입력일 때만 한 번 쓴 것으로 센다
            guess = int(text)
            history.append([guess, hint(guess, answer)])
            if guess == answer:
                solved = True
            elif guess < answer and guess + 1 > low:
                low = guess + 1      # 정답은 guess보다 크다
            elif guess > answer and guess - 1 < high:
                high = guess - 1     # 정답은 guess보다 작다

    # 결과 화면
    clear()
    show_status(len(history), low, high)
    print()
    show_history(history)
    print()
    if solved:
        center("★ CLEAR! ★")
        center(str(len(history)) + "번 만에 맞혔습니다!")
    else:
        center("GAME OVER")
        center("정답은 " + str(answer) + " 였습니다.")
    print()
    center("Enter를 누르면 메인 화면으로 돌아갑니다.")
    print()
    ask()


# ───────────────────────────── 메인 ─────────────────────────────

while True:
    clear()
    show_title()
    choice = ask().lower()    # lower(): 대문자도 소문자로 바꿔서 비교
    clear()
    if choice == "s":
        intro()
        play()
    elif choice == "q":
        break    # 반복문을 빠져나가 프로그램 종료
