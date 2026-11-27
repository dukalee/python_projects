import os
import random

DIGITS = 3                  # 맞혀야 하는 숫자 자릿수
MAX_TRIES = 10              # 이 횟수 안에 못 맞히면 GAME OVER
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
    center("★  숫자 야구  G A M E  ★")
    print()
    print(LINE)
    print()
    center("S : 시작하기      Q : 종료하기")
    print()


# ───────────────────────────── 게임 규칙 ─────────────────────────────

def make_answer():
    # 0~9 중에서 서로 다른 숫자 DIGITS개를 뽑아 글자로 이어 붙인다 (예: "407")
    numbers = list("0123456789")
    random.shuffle(numbers)
    return "".join(numbers[:DIGITS])


def check_guess(guess):
    # 입력이 올바르면 빈 글자(""), 잘못되었으면 이유를 글자로 돌려준다
    if len(guess) != DIGITS or not guess.isdigit():
        return str(DIGITS) + "자리 숫자를 입력해 주세요."
    for c in guess:
        if guess.count(c) > 1:    # 같은 숫자가 두 번 이상 나오면 안 된다
            return "서로 다른 숫자를 입력해 주세요."
    return ""


def judge(answer, guess):
    # 스트라이크: 숫자와 자리가 모두 같음 / 볼: 숫자는 있지만 자리가 다름
    strike = 0
    ball = 0
    for i in range(DIGITS):
        if guess[i] == answer[i]:
            strike = strike + 1
        elif guess[i] in answer:
            ball = ball + 1
    return strike, ball


def result_text(strike, ball):
    if strike == 0 and ball == 0:
        return "OUT"
    return str(strike) + "S " + str(ball) + "B"


def show_status(used):
    # 화면 맨 위에 항상 보이는 기회 표시줄: 남은 기회는 ♥, 쓴 기회는 ♡
    left = MAX_TRIES - used
    print()
    print(LINE)
    center("기회   " + "♥" * left + "♡" * used + "   (" + str(left) + "번 남음)")
    print(LINE)


# ───────────────────────────── 숫자 야구 ─────────────────────────────

def intro():
    # 안내사항을 보여주고 Enter를 기다린다
    print()
    print(LINE)
    center("♣  게 임 안 내  ♣")
    print(LINE)
    print()
    center_block([
        "▶ 컴퓨터가 서로 다른 숫자 " + str(DIGITS) + "개를 정했습니다. 맞혀 보세요!",
        "▶ 숫자 " + str(DIGITS) + "개를 입력하고 Enter를 누르면 힌트가 나옵니다.",
        "▶ 스트라이크(S): 숫자도 맞고 자리도 맞음",
        "▶ 볼(B): 숫자는 있지만 자리가 다름",
        "▶ 아웃(OUT): 하나도 맞지 않음",
        "▶ " + str(MAX_TRIES) + "번 안에 맞히면 승리!",
    ])
    print()
    print(LINE)
    print()
    center("Enter를 누르면 게임을 시작합니다.")
    print()
    ask()


def play():
    answer = make_answer()
    history = []        # 지금까지의 도전 기록: [입력한 숫자, 결과 글자]
    message = ""        # 잘못 입력했을 때 보여줄 안내 글
    solved = False

    while len(history) < MAX_TRIES and not solved:
        clear()
        show_status(len(history))
        print()
        for i in range(len(history)):
            print("  " + pad_left(str(i + 1), 2) + "회   " + history[i][0] + "   →   " + history[i][1])
        if len(history) == 0:
            print("  아직 도전 기록이 없습니다.")
        print()
        if message != "":
            print("  ※ " + message)
            message = ""
        print("  ◇ " + str(DIGITS) + "자리 숫자를 입력하세요.\n")

        guess = ask()
        message = check_guess(guess)
        if message == "":    # 올바른 입력일 때만 한 번 쓴 것으로 센다
            strike, ball = judge(answer, guess)
            history.append([guess, result_text(strike, ball)])
            if strike == DIGITS:
                solved = True

    # 결과 화면
    clear()
    show_status(len(history))
    print()
    for i in range(len(history)):
        print("  " + pad_left(str(i + 1), 2) + "회   " + history[i][0] + "   →   " + history[i][1])
    print()
    if solved:
        center("★ CLEAR! ★")
        center(str(len(history)) + "번 만에 맞혔습니다!")
    else:
        center("GAME OVER")
        center("정답은 " + answer + " 였습니다.")
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
