// 游戏状态
let gameState = {
    round: 1,
    budget: 60000,
    actions: 4,
    timeLeft: 300, // 5分钟 = 300秒
    activityLog: []
};

// 计时器
let timer;

// 初始化游戏
function initGame() {
    updateGameStatus();
    startTimer();
}

// 更新游戏状态显示
function updateGameStatus() {
    document.getElementById('current-round').textContent = gameState.round;
    document.getElementById('current-budget').textContent = gameState.budget;
    document.getElementById('remaining-actions').textContent = gameState.actions;
}

// 开始计时器
function startTimer() {
    timer = setInterval(() => {
        gameState.timeLeft--;
        updateTimer();
        if (gameState.timeLeft <= 0) {
            endRound();
        }
    }, 1000);
}

// 更新计时器显示
function updateTimer() {
    const minutes = Math.floor(gameState.timeLeft / 60);
    const seconds = gameState.timeLeft % 60;
    document.getElementById('countdown').textContent = 
        `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

// 显示操作界面
function showAction(actionType) {
    const actionArea = document.getElementById('action-area');
    actionArea.innerHTML = '';

    switch(actionType) {
        case 'visit':
            showVisitInterface();
            break;
        case 'city-meeting':
            showCityMeetingInterface();
            break;
        case 'conference':
            showConferenceInterface();
            break;
        case 'research':
            showResearchInterface();
            break;
    }
}

// 显示专业学术拜访界面
function showVisitInterface() {
    fetch('/api/hospitals')
        .then(response => response.json())
        .then(hospitals => {
            const actionArea = document.getElementById('action-area');
            actionArea.innerHTML = `
                <h3>选择医院</h3>
                <div class="hospital-list">
                    ${hospitals.map(hospital => `
                        <div class="hospital-card" onclick="selectHospital(${hospital.id})">
                            <h4>${hospital.name}</h4>
                            <p>患者数: ${hospital.patient_count}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        });
}

// 显示市场调研界面
function showResearchInterface() {
    const actionArea = document.getElementById('action-area');
    actionArea.innerHTML = `
        <h3>市场调研</h3>
        <p>是否进行市场调研（¥1000/次）？</p>
        <button onclick="conductResearch()">确认</button>
    `;
}

// 进行市场调研
function conductResearch() {
    if (gameState.budget < 1000 || gameState.actions < 1) {
        alert('预算或操作次数不足');
        return;
    }

    fetch('/api/research', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        gameState.budget -= 1000;
        gameState.actions -= 1;
        updateGameStatus();
        displayResearchResults(data);
    });
}

// 添加活动日志
function addActivityLog(activity) {
    gameState.activityLog.push(activity);
    const logContent = document.getElementById('log-content');
    logContent.innerHTML += `<div>${activity}</div>`;
    logContent.scrollTop = logContent.scrollHeight;
}

// 结束回合
function endRound() {
    clearInterval(timer);
    fetch('/api/end-round', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            activityLog: gameState.activityLog
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.gameOver) {
            showGameResults(data);
        } else {
            startNewRound(data);
        }
    });
}

// 初始化游戏
document.addEventListener('DOMContentLoaded', initGame);