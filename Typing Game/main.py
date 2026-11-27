import os
import random
import time

TEXT_FILE = "text.txt"      # 연습용 문장 목록 (한 줄에 한 문장)
RANK_FILE = "ranking.txt"   # 랭킹 기록 (한 줄에 이름,정확도,평균WPM,최고WPM)
COUNT = 10                  # 한 번에 테스트할 문장 수
MIN_ACCURACY = 95           # 이 정확도 미만이면 랭킹에 기록하지 않음
PROMPT = "  > "             # 사용자 입력 칸 표시 (모든 화면에서 동일)
TOP = 5                     # 랭킹에 보여줄 인원 수

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


def pad_right(text, size):
    # 글자 뒤에 공백을 붙여 size칸으로 맞춤 (왼쪽 정렬)
    return text + " " * (size - width(text))


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
    center("★  영문 타자연습  G A M E  ★")
    print()
    print(LINE)
    print()
    center("S : 시작하기      R : 랭킹 보기      Q : 종료하기")
    print()


# ───────────────────────────── 기록 계산 ─────────────────────────────

def average(numbers):
    if len(numbers) == 0:
        return 0.0
    return sum(numbers) / len(numbers)


def accuracy(correct, chars):
    # 정확도(%) = 맞게 친 글자 수 / 전체 글자 수 * 100
    if chars == 0:
        return 100.0
    return correct / chars * 100


def show_status(name, wpms, correct, chars, done, total):
    # 화면 맨 위에 항상 보이는 현재 기록 표시줄 (게임의 점수판)
    last = 0.0
    best = 0.0
    if len(wpms) > 0:
        last = wpms[-1]    # 리스트의 맨 마지막 값
        best = max(wpms)

    bar = "■" * done + "□" * (total - done)    # 진행 막대: 끝낸 칸(■) / 남은 칸(□)
    print()
    print(LINE)
    center(name + "   진행 [" + bar + "] " + str(done) + "/" + str(total))
    print()
    center("현재 " + str(round(last, 1)) + " WPM    최고 " + str(round(best, 1)) + " WPM    평균 " + str(round(average(wpms), 1)) + " WPM")
    center("정확도 " + str(round(accuracy(correct, chars), 1)) + "%")
    print(LINE)


# ───────────────────────────── 랭킹 ─────────────────────────────

def load_records():
    # ranking.txt를 읽어서 [이름, 정확도, 평균, 최고] 목록으로 만든다
    records = []
    if not os.path.exists(RANK_FILE):
        return records

    file = open(RANK_FILE, "r", encoding="utf-8")
    for line in file:
        parts = line.strip().split(",")    # "a,b,c,d" -> ["a", "b", "c", "d"]
        if len(parts) == 4:
            records.append([parts[0], float(parts[1]), float(parts[2]), float(parts[3])])
    file.close()
    return records


def save_record(name, acc, avg, best):
    # 파일 맨 뒤에 한 줄을 덧붙인다 ("a"는 append 모드)
    file = open(RANK_FILE, "a", encoding="utf-8")
    file.write(name.replace(",", " ") + "," + str(round(acc, 2)) + "," + str(round(avg, 2)) + "," + str(round(best, 2)) + "\n")
    file.close()


def is_higher(a, b):
    # a가 b보다 순위가 높으면 True: 정확도 -> 평균 WPM -> 최고 WPM 순으로 비교
    if a[1] != b[1]:
        return a[1] > b[1]
    if a[2] != b[2]:
        return a[2] > b[2]
    return a[3] > b[3]


def show_ranking():
    records = load_records()

    # 버블 정렬: 이웃한 두 기록을 비교해서 순위가 낮은 쪽이 뒤로 가도록 바꾼다
    for i in range(len(records)):
        for j in range(len(records) - 1 - i):
            if is_higher(records[j + 1], records[j]):
                temp = records[j]
                records[j] = records[j + 1]
                records[j + 1] = temp

    print()
    print(LINE)
    center("★  명 예 의 전 당  (TOP " + str(TOP) + ")  ★")
    print(LINE)
    print()

    # 표의 모든 줄을 모아서 한꺼번에 가운데 정렬한다
    table = [
        pad_right("순위", 6) + pad_right("이름", 14) + pad_left("정확도", 9) + pad_left("평균 WPM", 12) + pad_left("최고 WPM", 12),
        "─" * 53,
    ]
    for i in range(min(TOP, len(records))):
        r = records[i]
        rank = "  " + str(i + 1)
        if i == 0:
            rank = "★ 1"    # 1등에게만 별 표시
        table.append(pad_right(rank, 6) + pad_right(r[0], 14) + pad_left(str(round(r[1], 1)) + "%", 9)
                     + pad_left(str(round(r[2], 1)), 12) + pad_left(str(round(r[3], 1)), 12))
    center_block(table)

    if len(records) == 0:
        print()
        center("아직 기록이 없습니다. 첫 번째 도전자가 되어 보세요!")
    print()
    print(LINE)
    print()
    center("Enter를 누르면 메인 화면으로 돌아갑니다.")
    print()
    ask()


# ───────────────────────────── 타자 테스트 ─────────────────────────────

def intro():
    # 안내사항을 보여주고 이름을 입력받는다 (빈 이름은 다시 입력)
    print()
    print(LINE)
    center("♣  게 임 안 내  ♣")
    print(LINE)
    print()
    center_block([
        "▶ 화면에 나오는 문장 " + str(COUNT) + "개를 차례대로 똑같이 입력하세요.",
        "▶ 문장을 입력하고 Enter를 누르면 다음 문장으로 넘어갑니다.",
        "▶ 속도(WPM)는 문장이 나온 순간부터 Enter를 누를 때까지 잽니다.",
        "▶ 정확도는 전체 글자 중 오타 없이 입력한 비율입니다.",
        "▶ 정확도 " + str(MIN_ACCURACY) + "% 이상이면 랭킹에 기록됩니다.",
    ])
    print()
    print(LINE)
    name = ""
    while name == "":
        print()
        center("이름을 입력해 주세요.")
        print()
        name = ask()
    return name


def typing_test(name):
    # 1) 문장 파일을 읽고 섞어서 COUNT개를 고른다
    file = open(TEXT_FILE, "r", encoding="utf-8")
    texts = []
    for line in file:
        if line.strip() != "":
            texts.append(line.strip())
    file.close()

    random.shuffle(texts)
    sentences = texts[:COUNT]    # 앞에서부터 COUNT개
    total = len(sentences)

    # 2) 문장을 하나씩 보여주고 입력받는다
    wpms = []       # 문장마다의 타수(WPM) 기록
    correct = 0     # 맞게 친 글자 수
    chars = 0       # 전체 글자 수
    for i in range(total):
        target = sentences[i]
        clear()
        show_status(name, wpms, correct, chars, i, total)
        # 문장은 길이가 제각각이라 입력 칸(PROMPT)과 같은 왼쪽 줄에 맞춘다
        print("\n  ◆ 문장 " + str(i + 1))
        print("  " + target)
        print("\n  ◇ User\n")

        start = time.time()                  # 시작 시간
        typed = input(PROMPT)
        seconds = time.time() - start        # 걸린 시간(초)
        if seconds < 0.001:
            seconds = 0.001                  # 0으로 나누는 것을 방지

        # 타수(WPM) = (글자 수 / 5) / 걸린 시간(분)  -> 5글자를 1단어로 계산
        wpms.append(len(typed) / 5 / (seconds / 60))

        # 같은 위치의 글자가 같으면 맞게 친 것. 모자라거나 넘치는 글자는 오타
        for k in range(min(len(target), len(typed))):
            if target[k] == typed[k]:
                correct = correct + 1
        chars = chars + len(target)

    # 3) 결과 화면: 정확도가 기준 이상일 때만 랭킹에 기록
    clear()
    show_status(name, wpms, correct, chars, total, total)
    print()
    if accuracy(correct, chars) >= MIN_ACCURACY:
        save_record(name, accuracy(correct, chars), average(wpms), max(wpms))
        center("★ CLEAR! ★")
        center(name + "님, 랭킹에 기록되었습니다!")
    else:
        center("GAME OVER")
        center("정확도 " + str(MIN_ACCURACY) + "% 미만이라 기록되지 않았습니다.")
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
        typing_test(intro())
    elif choice == "r":
        show_ranking()
    elif choice == "q":
        break    # 반복문을 빠져나가 프로그램 종료
