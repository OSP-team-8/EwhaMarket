// list.js와 같은 스토리지 키 사용
const STORAGE_KEY = "likes";

function loadLikes() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
  catch { return {}; }
}
function saveLikes(map) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(map));
}
function applyLike(btn, liked) {
  if (!btn) return;
  btn.textContent = liked ? "♥" : "♡";
  btn.dataset.liked = String(liked);
}

document.addEventListener("DOMContentLoaded", () => {
  const map = loadLikes();
  const heartBtn = document.querySelector(".heart");
  if (!heartBtn) return;

  const pid = heartBtn.dataset.pid;
  applyLike(heartBtn, !!map[pid]);

  heartBtn.addEventListener("click", () => {
    const next = heartBtn.dataset.liked !== "true";
    map[pid] = next;
    applyLike(heartBtn, next);
    saveLikes(map);
  });
});
