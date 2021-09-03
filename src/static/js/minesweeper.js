function UIUpdate() {
  const tileInnerHtml = {
    f: '<span class="material-icons material-icons-outlined">flag</span>',
    xf: '<span class="material-icons material-icons-outlined">flag</span>\
    <span class="material-icons material-icons-outlined" style="position:absolute; color:red;">close</span>',
  };

  function updateBoard(board) {
    const canvas = document.getElementById('minesweeper');

    board.forEach((singleTile, idx) => {
      const cell = canvas.querySelector(`.cell[data-cell='${idx}']`);
      cell.dataset.type = singleTile;
      cell.classList.remove('open');
      cell.classList.remove('violated');

      if (singleTile.length !== 1) {
        cell.innerHTML = tileInnerHtml[singleTile];
      } else {
        if (singleTile === ' ') {
          cell.innerText = ' ';
        } else if (singleTile === '@') {
          cell.classList.add('open');
          cell.classList.add('violated');
          cell.innerText = ' ';
        } else if (singleTile >= 'A' && singleTile <= 'H') {
          cell.classList.add('open');
          cell.classList.add('violated');
          cell.innerText = String.fromCharCode(singleTile.charCodeAt(0) - 16);
        } else if (singleTile === '0') {
          cell.classList.add('open');
          cell.innerText = ' ';
        } else if (/^\d+$/.test(singleTile)) {
          cell.classList.add('open');
          cell.innerText = singleTile;
        } else if (singleTile === 'c') {
          cell.innerHTML = '<span class="material-icons material-icons-outlined">flag</span>';
        } else if (singleTile === 'p') {
          cell.innerHTML = '<span class="material-icons material-icons-outlined">help_outline</span>';
        } else if (singleTile === 'm') {
          cell.innerHTML = '<span class="material-icons material-icons-outlined">close</span>';
        } else if (singleTile === 's') {
          cell.innerHTML = '<span class="material-icons material-icons-outlined">done</span>';
        } else if (singleTile === '*') {
          cell.innerHTML = '<span class="material-icons material-icons-outlined">coronavirus</span>';
        } else {
          cell.innerHTML = tileInnerHtml[singleTile];
          cell.classList.remove('open');
        }
      }
    }
    );
  }

  function updateNoOfFlag(flag) {
    const flagButton = document.getElementById('flag-count');
    flagButton.innerText = flag;
  }

  function updateGameStatus(gameStatus) {
    const { has_won, has_lost } = gameStatus;
    if (!has_won && !has_lost) return;

    clearInterval(timeOutFn);
    if (has_lost) {
      const cells = document.querySelectorAll('.cell');
      cells.forEach((cell) => {
        cell.removeEventListener('click', minesweeper.leftClick);
        cell.removeEventListener('contextmenu', minesweeper.rightClick);
      });
    }

    const iconContainer = document.querySelector('.game-button span');
    const text = gameStatus.has_won
      ? 'emoji_emotions'
      : 'sentiment_very_dissatisfied';
    iconContainer.innerText = text;
  }

  return { updateBoard, updateNoOfFlag, updateGameStatus };
}

let isFirstClick = true;
let timeOutFn;

const minesweeper = (function () {
  function createEventHandler() {
    const cells = document.querySelectorAll('.cell');

    if (!cells) return;
    cells.forEach((cell) => {
      cell.addEventListener('click', leftClick);
      cell.addEventListener('contextmenu', rightClick);
    });

    const gameButton = document.querySelector('.game-button span');

    if (gameButton) {
      gameButton.addEventListener('click', loadNewGame);
    }
  }

  function resetTimerVars() {
    isFirstClick = true;
    const timer = document.getElementById('timer');

    if (timer) {
      timer.innerText = 0;
    }
  }

  function createNewGame({ target }) {
    resetTimerVars();
    createEventHandler();
    const name = target.name;
    const clss = target.classList;
    gameAssist = 0;
    if (clss.contains('al1' )) {gameAssist = 1;}
    if (clss.contains('al2' )) {gameAssist = 2;}
    fetch('/api/game', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ level: name,
                             assist: gameAssist }),
    })
      .then(() => window.location.replace('/minesweeper'))
      .catch((err) => console.error(err));
  }

  function loadNewGame() {
    resetTimerVars();
    createEventHandler();
    const iconContainer = document.querySelector('.game-button span');
    iconContainer.innerText = 'sentiment_satisfied_alt';
    fetch('/api/reload_game_type')
      .then((res) => res.json())
      .then(handleJSONResponse)
      .catch((err) => console.error(err));
  }

  function handleJSONResponse(json) {
    const { has_lost, has_won, no_of_flags, player_board } = json;
    const { updateBoard, updateNoOfFlag, updateGameStatus } = UIUpdate();
    updateBoard(player_board);
    updateNoOfFlag(no_of_flags);
    updateGameStatus({ has_won, has_lost });
  }

  function leftClick({ currentTarget }) {
    if (isFirstClick) {
      startTimer();
      isFirstClick = false;
    }

    const { cell } = currentTarget.dataset;
    update({ cell, type: 'open' });
  }

  function rightClick(e) {
    e.preventDefault();

    if (isFirstClick) {
      startTimer();
      isFirstClick = false;
    }

    const { cell } = e.currentTarget.dataset;
    update({ cell, type: 'flag' });
  }

  function startTimer() {
    const timer = document.getElementById('timer');
    timeOutFn = setInterval(() => {
      const timerText = Number(timer.innerText);
      if (timerText === 998) {
        clearInterval(timeOutFn);
      }
      timer.innerText = timerText + 1;
    }, 1000);
  }

  function update(data) {
    fetch('/api/update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then(handleJSONResponse)
      .catch((err) => console.error(err));
  }

  return {
    createNewGame,
    leftClick,
    rightClick,
    loadNewGame,
    createEventHandler,
  };
})();
