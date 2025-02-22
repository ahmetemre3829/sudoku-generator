#ahmetemre3829
import random
import os
import time
from PIL import ImageFont, ImageDraw, Image
from colorama import Fore

class DLXNode:
    def __init__(self):
        self.L = self
        self.R = self
        self.U = self
        self.D = self
        self.C = None
        self.row_data = None

class ColumnNode(DLXNode):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.size = 0

class DLXSolver:
    def __init__(self, board=None):
        self.num_cols = 324
        self.header = ColumnNode("header")
        self.columns = [ColumnNode(i) for i in range(self.num_cols)]
        
        self.header.R = self.columns[0]
        self.header.L = self.columns[-1]
        for i in range(len(self.columns)):
            self.columns[i].L = self.columns[i - 1]
            self.columns[i].R = self.columns[(i + 1) % len(self.columns)]
            self.columns[i].U = self.columns[i]
            self.columns[i].D = self.columns[i]
        self.header.R.L = self.header
        self.header.L.R = self.header

        self.candidate_nodes = {}
        for i in range(9):
            for j in range(9):
                for num in range(1, 10):
                    if board and board[i][j] != 0 and board[i][j] != num:
                        continue
                    col1 = i * 9 + j
                    col2 = 81 + i * 9 + (num - 1)
                    col3 = 162 + j * 9 + (num - 1)
                    col4 = 243 + (((i // 3) * 3) + (j // 3)) * 9 + (num - 1)
                    cols = [col1, col2, col3, col4]
                    
                    first_node = None
                    prev_node = None
                    for c in cols:
                        col = self.columns[c]
                        node = DLXNode()
                        node.row_data = (i, j, num)
                        node.C = col
                        node.U = col.U
                        node.D = col
                        col.U.D = node
                        col.U = node
                        col.size += 1
                        if first_node is None:
                            first_node = node
                            node.L = node
                            node.R = node
                        else:
                            node.L = prev_node
                            node.R = first_node
                            prev_node.R = node
                            first_node.L = node
                        prev_node = node
                    self.candidate_nodes[(i, j, num)] = first_node

        self.solution = []
        if board:
            for i in range(9):
                for j in range(9):
                    if board[i][j] != 0:
                        candidate = (i, j, board[i][j])
                        node = self.candidate_nodes.get(candidate)
                        if node:
                            self.__select_row(node)

    def __select_row(self, node):
        row_nodes = []
        temp = node
        row_nodes.append(temp)
        temp = temp.R
        while temp != node:
            row_nodes.append(temp)
            temp = temp.R
        for n in row_nodes:
            self.cover(n.C)
        self.solution.append(node)

    def cover(self, col):
        col.R.L = col.L
        col.L.R = col.R
        i = col.D
        while i != col:
            j = i.R
            while j != i:
                j.D.U = j.U
                j.U.D = j.D
                j.C.size -= 1
                j = j.R
            i = i.D

    def uncover(self, col):
        i = col.U
        while i != col:
            j = i.L
            while j != i:
                j.C.size += 1
                j.D.U = j
                j.U.D = j
                j = j.L
            i = i.U
        col.R.L = col
        col.L.R = col

    def search(self, k, solutions, limit):
        if self.header.R == self.header:
            solutions.append(self.solution.copy())
            return
        col = None
        min_size = float('inf')
        j = self.header.R
        while j != self.header:
            if j.size < min_size:
                min_size = j.size
                col = j
            j = j.R
        if col is None or col.size == 0:
            return
        self.cover(col)
        r = col.D
        while r != col:
            self.solution.append(r)
            j = r.R
            while j != r:
                self.cover(j.C)
                j = j.R
            self.search(k + 1, solutions, limit)
            if len(solutions) >= limit:
                return
            self.solution.pop()
            j = r.L
            while j != r:
                self.uncover(j.C)
                j = j.L
            r = r.D
        self.uncover(col)

    def solve(self, limit=2):
        solutions = []
        self.search(0, solutions, limit)
        return solutions

def dlx_solve_sudoku(board):
    solver = DLXSolver(board)
    solutions = solver.solve(limit=2)
    if not solutions:
        return None
    solution_board = [[0] * 9 for _ in range(9)]
    for node in solutions[0]:
        i, j, num = node.row_data
        solution_board[i][j] = num
    return solution_board

def dlx_has_unique_solution(board):
    solver = DLXSolver(board)
    solutions = solver.solve(limit=2)
    return len(solutions) == 1

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

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if any(board[i][col] == num for i in range(9)):
        return False
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def remove_numbers_target_strategic(board, target_empty):
    board_copy = [row[:] for row in board]
    empty_count = count_empty_cells(board_copy)
    
    groups = []
    for i in range(9):
        for j in range(9):
            if (i, j) > (8 - i, 8 - j):
                continue
            if (i, j) == (8 - i, 8 - j):
                groups.append([(i, j)]) 
            else:
                groups.append([(i, j), (8 - i, 8 - j)])
    random.shuffle(groups)
    
    for group in groups:
        if empty_count >= target_empty:
            break
        removed = []
        for (i, j) in group:
            if board_copy[i][j] != 0:
                removed.append((i, j, board_copy[i][j]))
                board_copy[i][j] = 0
                empty_count += 1
        if not dlx_has_unique_solution(board_copy):
            for (i, j, val) in removed:
                board_copy[i][j] = val
                empty_count -= 1
    
    if empty_count < target_empty:
        remaining = [(i, j) for i in range(9) for j in range(9) if board_copy[i][j] != 0]
        random.shuffle(remaining)
        for (i, j) in remaining:
            if empty_count >= target_empty:
                break
            temp = board_copy[i][j]
            board_copy[i][j] = 0
            empty_count += 1
            if not dlx_has_unique_solution(board_copy):
                board_copy[i][j] = temp
                empty_count -= 1
    return board_copy

def count_empty_cells(board):
    return sum(1 for i in range(9) for j in range(9) if board[i][j] == 0)

def generate_minimal_sudoku(target_empty=64):
    global attempt
    attempt = 0
    while True:
        attempt += 1
        full = generate_full_sudoku()
        puzzle = remove_numbers_target_strategic(full, target_empty)
        empty_count = count_empty_cells(puzzle)
        print(Fore.YELLOW + f"Deneme {attempt}: {empty_count} boş hücre bulundu.", end='\r')
        if empty_count == target_empty:
            return puzzle, full

# ---------------------------------------------------------------------
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
                bbox = draw.textbbox((0, 0), text, font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text((j * cell_size + (cell_size - w) // 2, i * cell_size + (cell_size - h) // 2),
                          text, fill="black", font=font)
    
    img.save(os.path.join(folder, filename), dpi=(300, 300))

# ---------------------------------------------------------------------
def main():
    print(Fore.GREEN + "Sudoku oluşturma aracına hoş geldiniz! " + Fore.CYAN + "#ahmetemre3829")
    while True:
        try:
            num_sudokus = int(input(Fore.MAGENTA + "Kaç tane sudoku oluşturmak istersiniz: " + Fore.WHITE))
            while True:
                target_empty = int(input(Fore.MAGENTA + "Zorluk seviyesi (17-64 arası): " + Fore.WHITE))
                if 17 <= target_empty <= 64:
                    break
                print(Fore.RED + "Hata: " + Fore.WHITE + "Zorluk 17 ile 64 arasında olmalıdır!")
            
            sudokular_folder = "Sudoku"
            sudoku_cozumleri_folder = "Sudoku"
            
            if not os.path.exists(sudokular_folder):
                os.makedirs(sudokular_folder)

            for i in range(num_sudokus):
                puzzle, full = generate_minimal_sudoku(target_empty)
                save_sudoku_image(puzzle, sudokular_folder, f"sudoku_{i+1}.jpg")
                solved = dlx_solve_sudoku(full)
                save_sudoku_image(solved, sudoku_cozumleri_folder, f"cozum_{i+1}.jpg")
                print(Fore.CYAN + f"Sudoku " + Fore.GREEN + f"{i+1}" + 
                      Fore.CYAN +" oluşturuldu. Deneme: " + Fore.GREEN + f"{attempt}                                                              ")
            print(Fore.GREEN + "\nBütün sudokular oluşturuldu.")
            time.sleep(3)
            print("\n")
        except ValueError:
            print(Fore.RED + "Hata: " + Fore.WHITE + "Geçersiz değer girdiniz!")
        except Exception as e:
            print(Fore.RED + "Hata: " + Fore.WHITE + str(e))

if __name__ == "__main__":
    main()
