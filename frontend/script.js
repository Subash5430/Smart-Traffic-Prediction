function predict() {
  const resultBox = document.getElementById("result");

  const payload = {
    city: document.getElementById("city").value,
    latitude: Number(document.getElementById("lat").value),
    longitude: Number(document.getElementById("lon").value),
    hour: Number(document.getElementById("hour").value),
    day: Number(document.getElementById("day").value),
    traffic_volume: Number(document.getElementById("traffic").value)
  };

  resultBox.style.display = "block";
  resultBox.innerText = "Analyzing traffic data...";
  resultBox.className = "result";

  fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      if (data.risk_level === "High") {
        resultBox.className = "result high";
        resultBox.innerText =
          `⚠️ HIGH RISK\nProbability: ${data.accident_risk}`;
      } else {
        resultBox.className = "result low";
        resultBox.innerText =
          `✅ LOW RISK\nProbability: ${data.accident_risk}`;
      }
    })
    .catch(() => {
      resultBox.className = "result high";
      resultBox.innerText = "Backend error.";
    });
}
