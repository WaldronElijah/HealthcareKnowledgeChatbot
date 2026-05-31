const form = document.querySelector("#question-form");
const input = document.querySelector("#question-input");
const submitButton = document.querySelector("#submit-button");
const resetButton = document.querySelector("#reset-button");
const statusBox = document.querySelector("#status");
const answerCard = document.querySelector("#answer-card");
const answerText = document.querySelector("#answer-text");
const sourcesList = document.querySelector("#sources-list");

function setStatus(message, isError = false) {
  statusBox.textContent = message;
  statusBox.classList.toggle("error", isError);
}

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  input.disabled = isLoading;
  submitButton.textContent = isLoading ? "Asking..." : "Ask question";
}

function renderSources(sources) {
  sourcesList.innerHTML = "";

  if (!sources || sources.length === 0) {
    const item = document.createElement("li");
    item.textContent = "No sources returned.";
    sourcesList.appendChild(item);
    return;
  }

  const seen = new Set();
  sources.forEach((source) => {
    const url = source.source;
    if (!url || seen.has(url)) {
      return;
    }
    seen.add(url);

    const item = document.createElement("li");
    const link = document.createElement("a");
    link.href = url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = source.title || source.source_owner || url;

    item.appendChild(link);
    sourcesList.appendChild(item);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = input.value.trim();
  if (!question) {
    input.focus();
    return;
  }

  answerCard.hidden = true;
  answerText.textContent = "";
  sourcesList.innerHTML = "";
  setStatus("Searching the diabetes knowledge base...");
  setLoading(true);

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    answerText.textContent = data.answer || "No answer returned.";
    renderSources(data.sources);
    answerCard.hidden = false;
    setStatus("");
  } catch (error) {
    setStatus(
      "Something went wrong while asking the backend. Make sure FastAPI is running and your model settings are valid.",
      true,
    );
  } finally {
    setLoading(false);
  }
});

resetButton.addEventListener("click", () => {
  input.value = "";
  answerCard.hidden = true;
  answerText.textContent = "";
  sourcesList.innerHTML = "";
  setStatus("");
  input.disabled = false;
  input.focus();
});
