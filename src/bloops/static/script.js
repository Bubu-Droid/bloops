const root = document.documentElement;

// theme toggle
const toggle = document.createElement("button");
toggle.className = "theme-toggle";
toggle.ariaLabel = "Toggle theme";
toggle.innerHTML =
  '<svg class="icon-moon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>' +
  '<svg class="icon-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>';
toggle.onclick = () => {
  root.dataset.theme = root.dataset.theme === "night" ? "day" : "night";
  try {
    localStorage.setItem("theme", root.dataset.theme);
  } catch {}
};
document.body.prepend(toggle);

// wide screens: put each sidenote beside its sidemark, below the previous note
// (ignored on narrow screens, where sidenotes are not absolutely positioned)
const marks = document.querySelectorAll(".sidemark");
const notes = document.querySelectorAll(".sidenote");
new ResizeObserver(() => {
  let floor = 0;
  notes.forEach((note, i) => {
    if (!marks[i] || !note.offsetParent) return; // e.g. inside a closed <details>
    const top = Math.max(
      marks[i].getBoundingClientRect().top -
        document.body.getBoundingClientRect().top,
      floor,
    );
    note.style.top = `${top}px`;
    floor = top + note.offsetHeight + 12;
  });
}).observe(document.body);
