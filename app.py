from flask import Flask, render_template_string, request, jsonify, Response
import time
import json

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
        
        .progress-container {
            display: none;
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        
        .progress-bar {
            width: 100%;
            height: 25px;
            background: #e9ecef;
            border-radius: 12px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            width: 0%;
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 12px;
        }
        
        .progress-text {
            text-align: center;
            color: #666;
            font-size: 0.9em;
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
        
        .btn-stop {
            background: linear-gradient(135deg, #ff9800, #f57c00);
        }

        button:hover:not(:disabled) {
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
        
        .info-box {
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 12px;
            margin-bottom: 15px;
            border-radius: 4px;
            font-size: 0.9em;
            color: #1565c0;
            display: none;
        }
        
        .warning-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 12px;
            margin-bottom: 15px;
            border-radius: 4px;
            font-size: 0.9em;
            color: #856404;
            display: none;
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
            <button class="btn-solve" id="btnSolve" onclick="solveStreaming()">🎯 Giải</button>
            <button class="btn-stop" id="btnStop" onclick="stopSolving()" style="display:none;">⏹️ Dừng</button>
            <button class="btn-next" id="btnNext" onclick="nextSolution()" disabled>⏭️ Lời giải tiếp</button>
            <button class="btn-reset" onclick="reset()">🔄 Reset</button>
        </div>
        
        <div class="warning-box" id="warningBox"></div>

        <div class="progress-container" id="progressContainer">
            <div class="progress-text" id="progressText">Đang tìm lời giải...</div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill">0%</div>
            </div>
        </div>

        <div class="status" id="status">Nhập N và nhấn "Giải" để bắt đầu</div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Đang khởi tạo...</p>
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
        let isStreaming = false;
        let streamAborted = false;

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

        async function solveStreaming() {
            const input = document.getElementById('nInput');
            n = parseInt(input.value);
            const warningBox = document.getElementById('warningBox');
            warningBox.style.display = 'none';

            if (isNaN(n) || n < 1) {
                alert('❌ Vui lòng nhập số nguyên dương!');
                return;
            }

            if (n > 15) {
                alert('❌ N không được vượt quá 15!');
                return;
            }

            // Hiển thị cảnh báo cho N lớn
            if (n >= 13 && n <= 15) {
                const warnings = {
                    13: { time: '1-2 phút', solutions: '73,712' },
                    14: { time: '5-10 phút', solutions: '365,596' },
                    15: { time: '30-60 phút', solutions: '2,279,184' }
                };
                
                const info = warnings[n];
                warningBox.innerHTML = `⚠️ <strong>CẢNH BÁO:</strong> N=${n} sẽ mất khoảng <strong>${info.time}</strong> để tính toán. Tổng số lời giải dự kiến: <strong>${info.solutions}</strong>`;
                warningBox.style.display = 'block';
                
                if (!confirm(`⚠️ N=${n} sẽ mất khoảng ${info.time} để tính toán.\n\n📊 Tổng số lời giải dự kiến: ${info.solutions}\n\nBạn có muốn tiếp tục?`)) {
                    warningBox.style.display = 'none';
                    return;
                }
            }

            // Reset state
            solutions = [];
            currentIndex = 0;
            isStreaming = true;
            streamAborted = false;
            
            // UI changes
            document.getElementById('btnSolve').style.display = 'none';
            document.getElementById('btnStop').style.display = 'inline-block';
            document.getElementById('btnNext').disabled = true;
            document.getElementById('progressContainer').style.display = 'block';
            document.getElementById('board').innerHTML = '';

            const startTime = Date.now();

            try {
                const response = await fetch(`/solve_stream?n=${n}`);
                const reader = response.body.getReader();
                const decoder = new TextDecoder();

                let buffer = '';

                while (true) {
                    const {done, value} = await reader.read();
                    
                    if (done || streamAborted) break;
                    
                    buffer += decoder.decode(value, {stream: true});
                    const lines = buffer.split('\n');
                    buffer = lines.pop();

                    for (const line of lines) {
                        if (!line.trim() || !line.startsWith('data: ')) continue;
                        
                        try {
                            const data = JSON.parse(line.substring(6));
                            
                            if (data.type === 'solution') {
                                solutions.push(data.board);
                                
                                if (solutions.length === 1 || solutions.length % 100 === 0) {
                                    drawBoard(data.board);
                                    document.getElementById('status').textContent = 
                                        `🔍 Đang tìm... Đã tìm được ${solutions.length} lời giải`;
                                }
                                
                                const progress = Math.min(95, (data.board[0] / n) * 100);
                                updateProgress(progress, solutions.length);
                            } else if (data.type === 'complete') {
                                const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
                                document.getElementById('status').textContent = 
                                    `✅ Hoàn thành! Tìm được ${data.total} lời giải trong ${elapsed}s`;
                                updateProgress(100, data.total);
                                
                                if (solutions.length > 0) {
                                    drawBoard(solutions[0]);
                                    currentIndex = 0;
                                    document.getElementById('btnNext').disabled = solutions.length <= 1;
                                }
                                
                                updateStats(n, solutions.length, 0, elapsed);
                            }
                        } catch (e) {
                            console.error('Parse error:', e);
                        }
                    }
                }
            } catch (error) {
                console.error('Stream error:', error);
                document.getElementById('status').textContent = '❌ Lỗi kết nối!';
            } finally {
                isStreaming = false;
                document.getElementById('btnSolve').style.display = 'inline-block';
                document.getElementById('btnStop').style.display = 'none';
                document.getElementById('progressContainer').style.display = 'none';
            }
        }

        function stopSolving() {
            streamAborted = true;
            document.getElementById('status').textContent = `⏹️ Đã dừng. Tìm được ${solutions.length} lời giải.`;
            document.getElementById('btnSolve').style.display = 'inline-block';
            document.getElementById('btnStop').style.display = 'none';
            document.getElementById('progressContainer').style.display = 'none';
            
            if (solutions.length > 0) {
                drawBoard(solutions[0]);
                currentIndex = 0;
                document.getElementById('btnNext').disabled = solutions.length <= 1;
                updateStats(n, solutions.length, 0, '-');
            }
        }

        function updateProgress(percent, count) {
            const fill = document.getElementById('progressFill');
            fill.style.width = percent + '%';
            fill.textContent = Math.round(percent) + '%';
            document.getElementById('progressText').textContent = 
                `Đã tìm được ${count} lời giải...`;
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
            streamAborted = true;
            solutions = [];
            currentIndex = 0;
            n = 0;
            isStreaming = false;
            document.getElementById('board').innerHTML = '';
            document.getElementById('status').textContent = 'Nhập N và nhấn "Giải" để bắt đầu';
            document.getElementById('nInput').value = '8';
            document.getElementById('btnNext').disabled = true;
            document.getElementById('btnSolve').style.display = 'inline-block';
            document.getElementById('btnStop').style.display = 'none';
            document.getElementById('progressContainer').style.display = 'none';
            document.getElementById('warningBox').style.display = 'none';
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

# Thuật toán Backtracking với generator để streaming
def solve_n_queens_stream(n):
    """
    Generator function để stream solutions từng cái một
    """
    board = [-1] * n
    cols = set()
    diag1 = set()
    diag2 = set()
    
    def backtrack(row):
        if row == n:
            yield board[:]
            return
        
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            board[row] = col
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            yield from backtrack(row + 1)
            
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            board[row] = -1
    
    yield from backtrack(0)

@app.route('/')
def index():
    """Trang chủ"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/solve_stream')
def solve_stream():
    """
    Streaming endpoint - gửi solutions từng cái một
    Không bị timeout vì luôn gửi data
    """
    try:
        n = int(request.args.get('n', 8))
        
        # Kiểm tra giới hạn N
        if n < 1:
            return jsonify({'success': False, 'error': 'N phải là số nguyên dương (N ≥ 1)'}), 400
            
        if n > 15:
            return jsonify({'success': False, 'error': 'N không được vượt quá 15. Vui lòng chọn N từ 1 đến 15.'}), 400
        
        def generate():
            """Generator function để stream Server-Sent Events"""
            count = 0
            start_time = time.time()
            
            for solution in solve_n_queens_stream(n):
                count += 1
                # Gửi solution dạng Server-Sent Events
                yield f"data: {json.dumps({'type': 'solution', 'board': solution, 'count': count})}\n\n"
            
            # Gửi thông báo hoàn thành
            end_time = time.time()
            elapsed = round(end_time - start_time, 3)
            yield f"data: {json.dumps({'type': 'complete', 'total': count, 'time': elapsed})}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🎯 N-QUEENS SOLVER - STREAMING MODE")
    print("=" * 60)
    print("📱 Server đang chạy tại: http://127.0.0.1:5000")
    print("🌐 Mở trình duyệt và truy cập link trên")
    print("✨ Streaming mode: Tìm TOÀN BỘ lời giải không bị timeout!")
    print("⚠️ Giới hạn: N từ 1 đến 15")
    print("⭐ Nhấn Ctrl+C để dừng server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
