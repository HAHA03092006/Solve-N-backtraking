from flask import Flask, render_template_string, request, jsonify
import time

app = Flask(__name__)

# HTML Template với CSS và JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>N-Queens Solver - Backtracking</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 30px;
            max-width: 700px;
            width: 100%;
        }

        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2em;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
        }

        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
        }

        .input-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        label {
            font-weight: 600;
            color: #333;
        }

        input[type="number"] {
            width: 80px;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }

        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }

        button {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            color: white;
        }

        .btn-solve {
            background: linear-gradient(135deg, #4CAF50, #45a049);
        }

        .btn-reset {
            background: linear-gradient(135deg, #f44336, #da190b);
        }

        .btn-next {
            background: linear-gradient(135deg, #2196F3, #0b7dda);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .status {
            text-align: center;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: 500;
            color: #333;
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .board-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }

        .board {
            display: inline-grid;
            gap: 2px;
            background: #333;
            padding: 2px;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }

        .cell {
            width: 50px;
            height: 50px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 30px;
            transition: all 0.3s;
            position: relative;
        }

        .cell.light {
            background: #f0d9b5;
        }

        .cell.dark {
            background: #b58863;
        }

        .cell.queen {
            animation: placeQueen 0.5s ease-out;
        }

        @keyframes placeQueen {
            0% {
                transform: scale(0) rotate(180deg);
                opacity: 0;
            }
            50% {
                transform: scale(1.2) rotate(-10deg);
            }
            100% {
                transform: scale(1) rotate(0deg);
                opacity: 1;
            }
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 5px;
        }

        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
        }

        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>♛ N-Queens Solver ♛</h1>
        <p class="subtitle">Giải bài toán N hậu bằng thuật toán Backtracking</p>

        <div class="controls">
            <div class="input-group">
                <label for="nInput">Nhập N:</label>
                <input type="number" id="nInput" min="1" max="15" value="8">
            </div>
            <button class="btn-solve" onclick="solve()">🎯 Giải</button>
            <button class="btn-next" id="btnNext" onclick="nextSolution()" disabled>⏭️ Lời giải tiếp</button>
            <button class="btn-reset" onclick="reset()">🔄 Reset</button>
        </div>

        <div class="status" id="status">Nhập N và nhấn "Giải" để bắt đầu</div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Đang tính toán trên server...</p>
        </div>

        <div class="board-container">
            <div class="board" id="board"></div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Kích thước bàn cờ</div>
                <div class="stat-value" id="statN">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Tổng số lời giải</div>
                <div class="stat-value" id="statTotal">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Đang xem</div>
                <div class="stat-value" id="statCurrent">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Thời gian</div>
                <div class="stat-value" id="statTime">-</div>
            </div>
        </div>
    </div>

    <script>
        let solutions = [];
        let currentIndex = 0;
        let n = 0;

        function drawBoard(board) {
            const boardElement = document.getElementById('board');
            boardElement.innerHTML = '';
            const n = board.length;
            
            const cellSize = Math.min(50, Math.floor(500 / n));
            boardElement.style.gridTemplateColumns = `repeat(${n}, ${cellSize}px)`;

            for (let i = 0; i < n; i++) {
                for (let j = 0; j < n; j++) {
                    const cell = document.createElement('div');
                    cell.className = 'cell ' + ((i + j) % 2 === 0 ? 'light' : 'dark');
                    cell.style.width = cellSize + 'px';
                    cell.style.height = cellSize + 'px';
                    cell.style.fontSize = (cellSize * 0.6) + 'px';
                    
                    if (board[i] === j) {
                        cell.textContent = '♛';
                        cell.classList.add('queen');
                    }
                    
                    boardElement.appendChild(cell);
                }
            }
        }

        async function solve() {
            const input = document.getElementById('nInput');
            n = parseInt(input.value);

            if (n < 1 || n > 15) {
                alert('N phải từ 1 đến 15!');
                return;
            }

            if (n > 12) {
                if (!confirm(`N=${n} có thể mất nhiều thời gian. Bạn có muốn tiếp tục?`)) {
                    return;
                }
            }

            document.getElementById('loading').style.display = 'block';
            document.getElementById('status').textContent = `Đang giải N=${n} trên server...`;
            document.getElementById('btnNext').disabled = true;

            try {
                const response = await fetch('/solve', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ n: n })
                });

                const data = await response.json();
                document.getElementById('loading').style.display = 'none';

                if (data.success) {
                    solutions = data.solutions;
                    currentIndex = 0;

                    if (solutions.length > 0) {
                        drawBoard(solutions[0]);
                        document.getElementById('status').textContent = 
                            `✅ Tìm thấy ${solutions.length} lời giải trong ${data.time}s`;
                        document.getElementById('btnNext').disabled = solutions.length <= 1;
                    } else {
                        document.getElementById('board').innerHTML = '';
                        document.getElementById('status').textContent = '❌ Không có lời giải!';
                    }

                    updateStats(n, solutions.length, currentIndex, data.time);
                } else {
                    document.getElementById('status').textContent = '❌ Lỗi: ' + data.error;
                }
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('status').textContent = '❌ Lỗi kết nối server!';
                console.error(error);
            }
        }

        function nextSolution() {
            if (solutions.length === 0) return;
            
            currentIndex = (currentIndex + 1) % solutions.length;
            drawBoard(solutions[currentIndex]);
            document.getElementById('status').textContent = 
                `Đang xem lời giải ${currentIndex + 1}/${solutions.length}`;
            updateStats(n, solutions.length, currentIndex, '-');
        }

        function reset() {
            solutions = [];
            currentIndex = 0;
            n = 0;
            document.getElementById('board').innerHTML = '';
            document.getElementById('status').textContent = 'Nhập N và nhấn "Giải" để bắt đầu';
            document.getElementById('nInput').value = '8';
            document.getElementById('btnNext').disabled = true;
            updateStats('-', '-', '-', '-');
        }

        function updateStats(n, total, current, time) {
            document.getElementById('statN').textContent = n;
            document.getElementById('statTotal').textContent = total;
            document.getElementById('statCurrent').textContent = 
                total > 0 ? `${current + 1}/${total}` : '-';
            document.getElementById('statTime').textContent = 
                time === '-' ? '-' : time + 's';
        }

        // Initialize
        reset();
    </script>
</body>
</html>
'''

# Thuật toán Backtracking giải N-Queens
def solve_n_queens(n):
    """
    Giải bài toán N-Queens bằng thuật toán Backtracking
    """
    solutions = []
    board = [-1] * n
    cols = set()
    diag1 = set()
    diag2 = set()
    
    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return
        
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            # Đặt hậu
            board[row] = col
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            # Đệ quy
            backtrack(row + 1)
            
            # Backtrack - gỡ hậu
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            board[row] = -1
    
    backtrack(0)
    return solutions

@app.route('/')
def index():
    """Trang chủ"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/solve', methods=['POST'])
def solve():
    """API endpoint để giải bài toán N-Queens"""
    try:
        data = request.get_json()
        n = int(data.get('n', 8))
        
        if n < 1 or n > 15:
            return jsonify({
                'success': False,
                'error': 'N phải từ 1 đến 15'
            })
        
        # Tính thời gian
        start_time = time.time()
        solutions = solve_n_queens(n)
        end_time = time.time()
        
        time_taken = round(end_time - start_time, 3)
        
        return jsonify({
            'success': True,
            'solutions': solutions,
            'count': len(solutions),
            'time': time_taken
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("=" * 60)
    print("🎯 N-QUEENS SOLVER - WEB APPLICATION")
    print("=" * 60)
    print("📱 Server đang chạy tại: http://127.0.0.1:5000")
    print("🌐 Mở trình duyệt và truy cập link trên")
    print("⭐ Nhấn Ctrl+C để dừng server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)