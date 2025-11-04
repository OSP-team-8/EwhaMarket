// 모바일에서 햄버거 버튼으로 메뉴 열고닫기
document.addEventListener('DOMContentLoaded', () => {
  const menu = document.querySelector('.navbar__menu');
  const toggle = document.querySelector('.navbar__toogleBtn');

  // 아이콘이 폰트어썸 없이도 보이도록 기본 문자 제공
  if (toggle && toggle.innerHTML.trim() === '') {
    toggle.textContent = '☰';
  }

  toggle?.addEventListener('click', (e) => {
    e.preventDefault();
    menu?.classList.toggle('active');
  });

  // 메뉴 클릭 시 닫기 (모바일 UX)
  menu?.addEventListener('click', (e) => {
    if (e.target.tagName === 'A') menu.classList.remove('active');
  });
});