const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("input");
const btnSend = document.getElementById("btn-send");
const btnReset = document.getElementById("btn-reset");

const LABEL_SUMBER = { knowledge_base: "Knowledge Base", llm: "Gemini AI" };

async function ambilJawaban(pertanyaan) {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: pertanyaan }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Server gagal memproses pertanyaan.");
  return data;
}

function tambahPesan(teks, peran, sumber, error = false) {
  const msg = document.createElement("div");
  msg.className = `msg ${peran}` + (error ? " error" : "");
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = teks;
  msg.appendChild(bubble);
  if (sumber) {
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.textContent = "Sumber: " + (LABEL_SUMBER[sumber] || sumber);
    msg.appendChild(meta);
  }
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
  return msg;
}

async function kirim() {
  const teks = input.value.trim();
  if (!teks || btnSend.disabled) return;
  tambahPesan(teks, "user");
  input.value = "";
  btnSend.disabled = true;
  const mengetik = tambahPesan("Sedang mengetik...", "bot");
  try {
    const data = await ambilJawaban(teks);
    mengetik.remove();
    tambahPesan(data.answer, "bot", data.source);
  } catch (err) {
    mengetik.remove();
    const pesan = err instanceof TypeError
      ? "Tidak bisa terhubung ke server. Jalankan python main.py dulu."
      : err.message;
    tambahPesan(pesan, "bot", null, true);
  } finally {
    btnSend.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (e) => { e.preventDefault(); kirim(); });
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); kirim(); }
});
btnReset.addEventListener("click", () => { chat.innerHTML = ""; input.focus(); });