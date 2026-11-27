import os
import random

SYMBOLS = "♠♥♦♣★●▲♪"        # 카드에 그려진 문양 (각각 2장씩 만든다 -> 총 16장)
COLS = 4                    # 한 줄에 놓는 카드 수 (4 x 4 판)
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
    center("★  카드 뒤집기  G A M E  ★")
    print()
    print(LINE)
    print()
    center("S : 시작하기      Q : 종료하기")
    print()


# ───────────────────────────── 카드 판 ─────────────────────────────

def make_cards():
    # 문양마다 2장씩 넣고 섞는다 (예: ["♣", "♠", "♪", ...])
    cards = []
    for s in SYMBOLS:
        cards.append(s)
        cards.append(s)
    random.shuffle(cards)
    return cards


def card_text(i, cards, matched, flipped, reveal):
    # 카드 한 장을 5칸짜리 글자로 만든다 (가운데에 번호 또는 문양이 온다)
    #   [ 3 ] 뒤집혀 있는 카드(번호만 보임)   [ ♠ ] 열려 있는 카드(문양이 보임)
    if matched[i] or i in flipped or reveal:
        return "[ " + cards[i] + " ]"
    return "[" + str(i + 1).center(3) + "]"    # center(3): 3칸 가운데에 번호를 놓는다


def show_board(cards, matched, flipped, reveal):
    # 카드를 COLS장씩 한 줄로 묶어 보여 준다 (줄 사이는 한 줄 띄움)
    lines = []
    for start in range(0, len(cards), COLS):
        row = ""
        for i in range(start, start + COLS):
            row = row + card_text(i, cards, matched, flipped, reveal) + "   "
        lines.append(row.rstrip())
        lines.append("")
    del lines[-1]    # 맨 아래의 빈 줄은 필요 없다
    center_block(lines)


def show_status(turns, pairs):
    # 화면 맨 위에 항상 보이는 표시줄: 카드를 뒤집어 본 횟수(적을수록 좋다)와 맞춘 짝의 수
    print()
    print(LINE)
    center("시도 횟수  " + str(turns) + "번")
    print()
    center("맞춘 짝  " + str(pairs) + " / " + str(len(SYMBOLS)))
    print(LINE)


def check_pick(text, cards, matched, flipped):
    # 입력이 올바르면 빈 글자(""), 잘못되었으면 이유를 글자로 돌려준다
    if not text.isdigit() or int(text) < 1 or int(text) > len(cards):
        return "1부터 " + str(len(cards)) + " 사이의 카드 번호를 입력해 주세요."
    i = int(text) - 1
    if matched[i]:
        return "이미 짝을 맞춘 카드입니다."
    if i in flipped:
        return "방금 뒤집은 카드입니다. 다른 카드를 골라 주세요."
    return ""


def pick_card(cards, matched, flipped, turns, pairs, question):
    # 카드 한 장을 골라 번호(0부터 시작하는 위치)를 돌려준다. 잘못 입력하면 다시 묻는다
    message = ""
    while True:
        clear()
        show_status(turns, pairs)
        print()
        show_board(cards, matched, flipped, False)
        print()
        if message != "":
            print("  ※ " + message)
        print("  ◇ " + question + "\n")
        text = ask()
        message = check_pick(text, cards, matched, flipped)
        if message == "":
            return int(text) - 1


# ───────────────────────────── 카드 뒤집기 ─────────────────────────────

def intro():
    # 안내사항을 보여주고 Enter를 기다린다
    print()
    print(LINE)
    center("♣  게 임 안 내  ♣")
    print(LINE)
    print()
    center_block([
        "▶ 뒤집혀 있는 카드 " + str(len(SYMBOLS) * 2) + "장 중에서 같은 문양 두 장을 찾는 게임입니다.",
        "▶ 카드 번호를 입력하면 그 카드가 뒤집힙니다. 두 장을 차례로 고르세요.",
        "▶ 문양이 같으면 짝 성공! 그 카드는 계속 열려 있습니다.",
        "▶ 문양이 다르면 카드가 다시 뒤집힙니다.",
        "▶ 목표: 가능한 적은 시도로 모든 짝을 맞히세요!",
    ])
    print()
    print(LINE)
    print()
    center("Enter를 누르면 게임을 시작합니다.")
    print()
    ask()


def play():
    cards = make_cards()
    matched = [False] * len(cards)    # 카드마다 짝을 맞췄는지 (처음엔 모두 False)
    pairs = 0           # 맞춘 짝의 수
    turns = 0           # 카드를 두 장 뒤집은 횟수 (적을수록 좋다)

    while pairs < len(SYMBOLS):
        first = pick_card(cards, matched, [], turns, pairs, "첫 번째 카드 번호를 입력하세요.")
        second = pick_card(cards, matched, [first], turns, pairs, "두 번째 카드 번호를 입력하세요.")
        turns = turns + 1

        # 두 장을 모두 뒤집어 보여 주고 결과를 알려 준다
        clear()
        show_status(turns, pairs)
        print()
        show_board(cards, matched, [first, second], False)
        print()
        if cards[first] == cards[second]:
            matched[first] = True
            matched[second] = True
            pairs = pairs + 1
            center("짝이 맞았습니다!  (" + cards[first] + ")")
        print()
        center("Enter를 누르면 계속합니다.")
        print()
        ask()

    # 결과 화면
    clear()
    show_status(turns, pairs)
    print()
    show_board(cards, matched, [], False)
    print()
    center("★ CLEAR! ★")
    center(str(turns) + "번 만에 모든 짝을 맞혔습니다!")
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
