#ahmetemre3829 tarafından yazılmıştır
import random
import os
import time
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from colorama import Fore

def is_valid(board, row, col, num):
    if num in board[row] or num in [board[i][col] for i in range(9)]:
        return False
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def generate_full_sudoku():
    board = [[0] * 9 for _ in range(9)]
    def fill_board():
        empty = find_empty(board)
        if not empty:
            return True
        row, col = empty
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if is_valid(board, row, col, num):
                board[row][col] = num
                if fill_board():
                    return True
                board[row][col] = 0
        return False
    fill_board()
    return board

def remove_numbers(board, target_empty):
    while True:
        board_copy = [row[:] for row in board]
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        count = 0
        for row, col in cells:
            temp = board_copy[row][col]
            board_copy[row][col] = 0
            temp_board = [r[:] for r in board_copy]
            if not has_unique_solution(temp_board):
                board_copy[row][col] = temp
            else:
                count += 1
                if count >= target_empty:
                    return board_copy
        board = generate_full_sudoku()

def has_unique_solution(board):
    solutions = []
    def solve_and_count():
        if len(solutions) > 1:
            return
        empty = find_empty(board)
        if not empty:
            solutions.append([row[:] for row in board])
            return
        row, col = empty
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row][col] = num
                solve_and_count()
                board[row][col] = 0
    solve_and_count()
    return len(solutions) == 1

def save_sudoku_image(board, folder, filename="sudoku.jpg"):
    cell_size = 180
    img_size = 9 * cell_size
    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", size=70)
    except IOError:
        font = ImageFont.load_default()
    
    for i in range(10):
        line_width = 10 if i % 3 == 0 else 5
        draw.line([(i * cell_size, 0), (i * cell_size, img_size)], fill="black", width=line_width)
        draw.line([(0, i * cell_size), (img_size, i * cell_size)], fill="black", width=line_width)

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                text = str(board[i][j])
                w, h = draw.textbbox((0, 0), text, font=font)[2:]
                draw.text((j * cell_size + (cell_size - w) // 2, i * cell_size + (cell_size - h) // 2), text, fill="black", font=font)
    
    img.save(os.path.join(folder, filename), dpi=(300, 300))

def main():
    print(Fore.GREEN + "Sudoku oluşturma aracına hoş geldiniz! "+ Fore.CYAN + "#ahmetemre3829")
    while True:
        try:
            num_sudokus = int(input(Fore.MAGENTA + "Kaç tane sudoku oluşturmak istersiniz: " + Fore.WHITE))
            while True:
                empty_cells = int(input(Fore.MAGENTA + "Zorluk seviyesi (17-57 arası): " + Fore.WHITE))
                if 17 <= empty_cells <= 57:
                    break
                print(Fore.RED + "Hata:" + Fore.WHITE + "Zorluk 17 ile 57 arasında olmalıdır!")
            
            sudokular_folder = "Sudokular"
            sudoku_cozumleri_folder = "Sudoku Çözümleri"
            
            if not os.path.exists(sudokular_folder):
                os.makedirs(sudokular_folder)
            if not os.path.exists(sudoku_cozumleri_folder):
                os.makedirs(sudoku_cozumleri_folder)

            for i in range(num_sudokus):
                print(Fore.YELLOW + "Sudokular üretiliyor " + Fore.WHITE +f"({i+1}/{num_sudokus})", end='\r')
                full_sudoku = generate_full_sudoku()
                sudoku_puzzle = remove_numbers(full_sudoku, empty_cells)
                save_sudoku_image(sudoku_puzzle, sudokular_folder, f"sudoku_{i+1}.jpg")
                solve_sudoku(full_sudoku)
                save_sudoku_image(full_sudoku, sudoku_cozumleri_folder, f"çözum_{i+1}.jpg")
            print(Fore.GREEN + "Sudokular oluşturuldu.                       ")
            time.sleep(3),
            print("\n")
        except ValueError:
            print(Fore.RED + "Hata: " + Fore.WHITE + "Geçersiz değer girdiniz!")
        except Exception as e:
            print(Fore.RED + "Hata: ",Fore.WHITE + e)
    
if __name__ == "__main__":
    main()
