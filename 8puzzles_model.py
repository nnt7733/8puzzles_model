import random

# Trạng thái đích mà chúng ta cần đạt tới
GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Định nghĩa các hướng di chuyển và hành động ngược lại hoàn toàn bằng tiếng Việt
MOVES = {"LEN": (-1, 0), "XUONG": (1, 0), "TRAI": (0, -1), "PHAI": (0, 1)}
REVERSE_MOVE = {"LEN": "XUONG", "XUONG": "LEN", "TRAI": "PHAI", "PHAI": "TRAI"}

# Các hành động hợp lệ dựa trên vị trí của ô trống (0) trên bàn cờ 3x3
VALID_ACTIONS = {
    (0, 0): ["XUONG", "PHAI"], (0, 2): ["XUONG", "TRAI"],
    (2, 0): ["LEN", "PHAI"], (2, 2): ["LEN", "TRAI"],
    (0, 1): ["XUONG", "TRAI", "PHAI"], (1, 0): ["LEN", "XUONG", "PHAI"],
    (1, 2): ["LEN", "XUONG", "TRAI"], (2, 1): ["LEN", "TRAI", "PHAI"],
    (1, 1): ["LEN", "XUONG", "TRAI", "PHAI"]
}

# Đếm số lượng nghịch thế (số lớn đứng trước số nhỏ) để kiểm tra tính giải được
def count_inversions(board):
    flat_list = [num for row in board for num in row if num != 0]
    inv_count = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inv_count += 1
    return inv_count

# Bài toán 8-puzzle giải được khi và chỉ khi tổng số nghịch thế là số chẵn
def is_solvable(board):
    return count_inversions(board) % 2 == 0

# Chuyển bảng thành tuple để làm key lưu vào tập hợp đã đi qua (visited)
def get_state_key(board):
    return tuple(item for row in board for item in row)

# Thực hiện di chuyển ô trống và trả về bảng mới cùng vị trí mới của ô trống
def apply_move(board, action, zero_pos):
    zr, zc = zero_pos
    dr, dc = MOVES[action]
    nr, nc = zr + dr, zc + dc
    new_board = [row[:] for row in board]
    new_board[zr][zc], new_board[nr][nc] = new_board[nr][nc], new_board[zr][zc]
    return new_board, (nr, nc)

# Agent dựa trên mô hình: Sử dụng DFS ngẫu nhiên và quay lui
def model_based_agent(internal_state, visited):
    current_board = internal_state['board']
    zero_pos = internal_state['zero_pos']
    
    possible_actions = VALID_ACTIONS[zero_pos]
    safe_actions = []
    
    # Tìm các hướng đi chưa từng được ghé thăm
    for action in possible_actions:
        temp_board, _ = apply_move(current_board, action, zero_pos)
        if get_state_key(temp_board) not in visited:
            safe_actions.append(action)
            
    if safe_actions:
        # Nếu có đường mới, chọn ngẫu nhiên một hướng và đi tiếp
        action = random.choice(safe_actions)
        internal_state['history'].append(action)
        return action, False
    else:
        # Nếu không còn đường mới, thực hiện quay lui (Backtrack)
        if not internal_state['history']: return None, False
        last_move = internal_state['history'].pop()
        return REVERSE_MOVE[last_move], True

# Hàm in bàn cờ ra màn hình
def print_board(board):
    print("-------------")
    for row in board:
        print(" ".join("_" if x == 0 else str(x) for x in row))
    print("-------------")

def run():
    # Khởi tạo bảng ngẫu nhiên nhưng phải đảm bảo giải được
    while True:
        nums = list(range(9))
        random.shuffle(nums)
        real_board = [nums[0:3], nums[3:6], nums[6:9]]
        if is_solvable(real_board):
            break
            
    # Tìm vị trí ô trống ban đầu
    zr, zc = -1, -1
    for r in range(3):
        for c in range(3):
            if real_board[r][c] == 0: zr, zc = r, c
            
    # Trạng thái nội bộ của Agent
    internal_state = {
        'board': [row[:] for row in real_board],
        'zero_pos': (zr, zc),
        'history': []
    }
    
    visited = {get_state_key(real_board)}
    print("Trang thai ban dau")
    print_board(real_board)
    
    step = 0
    while step < 500000:
        step += 1
        action, is_backtracking = model_based_agent(internal_state, visited)
        
        # Nếu không còn đường nào để quay lui về nữa
        if action is None:
            print(f"\nKhong tim thay loi giai sau khi kham pha {len(visited)} trang thai.")
            print(f"Tong so buoc da thuc hien: {step}")
            break
            
        # Cập nhật bảng thực tế và trạng thái của Agent
        real_board, new_zero = apply_move(real_board, action, internal_state['zero_pos'])
        internal_state['board'] = [row[:] for row in real_board]
        internal_state['zero_pos'] = new_zero
        
        if not is_backtracking:
            visited.add(get_state_key(real_board))
            print(f"Buoc {step}: {action}")
        else:
            print(f"Buoc {step}: QUAY LUI ({action})")
            
        print_board(real_board)
        
        # Kiểm tra xem đã đến đích chưa
        if real_board == GOAL:
            print("Da tim thay dich!")
            print(f"So trang thai da kham pha: {len(visited)}")
            print(f"Tong so buoc da thuc hien: {step}")
            break

if __name__ == "__main__":
    run()