const canvas = document.getElementById("drawing-board");
const context = canvas.getContext("2d");
const predictButton = document.getElementById("predict-button");
const clearButton = document.getElementById("clear-button");
const topLabel = document.getElementById("top-label");
const topConfidence = document.getElementById("top-confidence");
const messageBox = document.getElementById("message-box");

const probabilityCards = Array.from(
  document.querySelectorAll(".probability-card")
).map((card) => ({
  key: card.dataset.key,
  labelNode: card.querySelector(".probability-label"),
  scoreNode: card.querySelector(".probability-score"),
  fillNode: card.querySelector(".probability-fill"),
}));

const classLabelMap = new Map(
  (window.APP_CONFIG.classes || []).map((item) => [item.key, item.label])
);

const state = {
  drawing: false,
  hasStroke: false,
  lastPoint: null,
  predictTimer: null,
};

function syncVisibleLabels() {
  probabilityCards.forEach((item) => {
    const label = classLabelMap.get(item.key);
    if (label) {
      item.labelNode.textContent = label;
    }
  });
}

function setupCanvas() {
  context.fillStyle = "#ffffff";
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.lineCap = "round";
  context.lineJoin = "round";
  context.strokeStyle = "#b94672";
  context.lineWidth = 18;
}

function getCanvasPoint(event) {
  const rect = canvas.getBoundingClientRect();
  const source = event.touches ? event.touches[0] : event;
  return {
    x: ((source.clientX - rect.left) / rect.width) * canvas.width,
    y: ((source.clientY - rect.top) / rect.height) * canvas.height,
  };
}

function beginDrawing(event) {
  event.preventDefault();
  state.drawing = true;
  state.hasStroke = true;
  state.lastPoint = getCanvasPoint(event);
}

function draw(event) {
  if (!state.drawing) {
    return;
  }

  event.preventDefault();
  const point = getCanvasPoint(event);
  context.beginPath();
  context.moveTo(state.lastPoint.x, state.lastPoint.y);
  context.lineTo(point.x, point.y);
  context.stroke();
  state.lastPoint = point;
  queuePrediction();
}

function endDrawing() {
  state.drawing = false;
  state.lastPoint = null;
}

function queuePrediction() {
  if (!window.APP_CONFIG.modelReady) {
    return;
  }

  window.clearTimeout(state.predictTimer);
  state.predictTimer = window.setTimeout(() => {
    if (state.hasStroke) {
      predictDrawing();
    }
  }, 500);
}

function resetProbabilities() {
  probabilityCards.forEach((item) => {
    item.scoreNode.textContent = "0%";
    item.fillNode.style.width = "0%";
  });
}

function updateResult(result) {
  topLabel.textContent = result.label;
  topConfidence.textContent = `Độ tin cậy ${result.confidence.toFixed(2)}%`;
  messageBox.textContent = "Mô hình đang ưu tiên nhãn có hình dáng gần nhất với nét vẽ của bạn.";

  result.probabilities.forEach((entry) => {
    const card = probabilityCards.find((item) => item.key === entry.key);
    if (!card) {
      return;
    }
    card.scoreNode.textContent = `${entry.score.toFixed(2)}%`;
    card.fillNode.style.width = `${entry.score}%`;
  });
}

async function predictDrawing() {
  if (!state.hasStroke) {
    messageBox.textContent = "Bạn hãy vẽ một món đồ trước khi nhận dạng.";
    return;
  }

  messageBox.textContent = "Đang phân tích nét vẽ...";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        image: canvas.toDataURL("image/png"),
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Không thể dự đoán lúc này.");
    }

    updateResult(data);
  } catch (error) {
    messageBox.textContent = error.message;
  }
}

function clearCanvas() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  setupCanvas();
  state.hasStroke = false;
  topLabel.textContent = "Chưa có kết quả";
  topConfidence.textContent = "Hãy vẽ để bắt đầu nhận dạng";
  messageBox.textContent = window.APP_CONFIG.modelReady
    ? "Ứng dụng đã sẵn sàng nhận dạng từ nét vẽ của bạn."
    : "Mô hình chưa được huấn luyện. Hãy chạy script train trước khi nhận dạng.";
  resetProbabilities();
}

canvas.addEventListener("mousedown", beginDrawing);
canvas.addEventListener("mousemove", draw);
window.addEventListener("mouseup", endDrawing);
canvas.addEventListener("mouseleave", endDrawing);
canvas.addEventListener("touchstart", beginDrawing, { passive: false });
canvas.addEventListener("touchmove", draw, { passive: false });
canvas.addEventListener("touchend", endDrawing);

predictButton.addEventListener("click", predictDrawing);
clearButton.addEventListener("click", clearCanvas);

setupCanvas();
syncVisibleLabels();
resetProbabilities();
