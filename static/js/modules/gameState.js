// Game state management
export const gameState = {
    round: 1,
    budget: 60000,
    actions: 4,
    timeLeft: 300,
    activityLog: [],
    company: null // 'A' or 'D'
};

export function updateGameState(updates) {
    Object.assign(gameState, updates);
    updateUI();
}

function updateUI() {
    document.getElementById('current-round').textContent = gameState.round;
    document.getElementById('current-budget').textContent = gameState.budget;
    document.getElementById('remaining-actions').textContent = gameState.actions;
}