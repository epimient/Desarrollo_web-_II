const slides = Array.from(document.querySelectorAll(".slide"));
const slideList = document.querySelector("#slideList");
const currentSlide = document.querySelector("#currentSlide");
const totalSlides = document.querySelector("#totalSlides");
const progressBar = document.querySelector("#progressBar");
const slideTopic = document.querySelector("#slideTopic");
const prevButton = document.querySelector("#prevSlide");
const nextButton = document.querySelector("#nextSlide");
const toggleNavButton = document.querySelector("#toggleNav");
const fullscreenButton = document.querySelector("#fullscreenButton");
const deck = document.querySelector("#deck");

let activeIndex = 0;
let touchStartX = 0;
let touchStartY = 0;

function formatNumber(value) {
  return String(value).padStart(2, "0");
}

function getTitle(slide, index) {
  return slide.dataset.title || `Diapositiva ${index + 1}`;
}

function getInitialIndex() {
  const match = globalThis.location.hash.match(/slide-(\d+)/);
  if (!match) return 0;

  const requested = Number(match[1]) - 1;
  if (Number.isNaN(requested)) return 0;

  return Math.min(Math.max(requested, 0), slides.length - 1);
}

function setHash(index) {
  const nextHash = `#slide-${index + 1}`;
  if (globalThis.location.hash === nextHash) return;
  globalThis.history.replaceState(null, "", nextHash);
}

function setActiveNav(index) {
  const buttons = slideList.querySelectorAll("button");
  buttons.forEach((button, buttonIndex) => {
    button.classList.toggle("is-active", buttonIndex === index);
    button.setAttribute(
      "aria-current",
      buttonIndex === index ? "step" : "false",
    );
  });
}

function showSlide(index, options = {}) {
  const shouldUpdateHash = options.updateHash !== false;
  activeIndex = Math.min(Math.max(index, 0), slides.length - 1);

  slides.forEach((slide, slideIndex) => {
    slide.classList.toggle("is-active", slideIndex === activeIndex);
    slide.setAttribute(
      "aria-hidden",
      slideIndex === activeIndex ? "false" : "true",
    );
    if (slideIndex === activeIndex) {
      slide.scrollTop = 0;
    }
  });

  currentSlide.textContent = formatNumber(activeIndex + 1);
  totalSlides.textContent = formatNumber(slides.length);
  progressBar.style.width = `${((activeIndex + 1) / slides.length) * 100}%`;
  slideTopic.textContent = getTitle(slides[activeIndex], activeIndex);
  prevButton.disabled = activeIndex === 0;
  nextButton.disabled = activeIndex === slides.length - 1;
  setActiveNav(activeIndex);

  if (shouldUpdateHash) {
    setHash(activeIndex);
  }
}

function nextSlide() {
  showSlide(activeIndex + 1);
}

function previousSlide() {
  showSlide(activeIndex - 1);
}

function closeNav() {
  document.body.classList.remove("nav-open");
  toggleNavButton.setAttribute("aria-expanded", "false");
}

function toggleNav() {
  const isOpen = document.body.classList.toggle("nav-open");
  toggleNavButton.setAttribute("aria-expanded", String(isOpen));
}

function buildSlideList() {
  const fragment = document.createDocumentFragment();

  slides.forEach((slide, index) => {
    const item = document.createElement("li");
    const button = document.createElement("button");
    const number = document.createElement("span");
    const title = document.createElement("span");

    number.textContent = formatNumber(index + 1);
    title.textContent = getTitle(slide, index);
    button.type = "button";
    button.append(number, title);
    button.addEventListener("click", () => {
      showSlide(index);
      closeNav();
      deck.focus({ preventScroll: true });
    });

    item.append(button);
    fragment.append(item);
  });

  slideList.append(fragment);
}

function handleKeyboard(event) {
  const key = event.key;
  const tagName = document.activeElement?.tagName;
  const isTyping = tagName === "INPUT" || tagName === "TEXTAREA" ||
    document.activeElement?.isContentEditable;

  if (isTyping) return;

  if (key === "ArrowRight" || key === "PageDown" || key === " ") {
    event.preventDefault();
    nextSlide();
  }

  if (key === "ArrowLeft" || key === "PageUp") {
    event.preventDefault();
    previousSlide();
  }

  if (key === "Home") {
    event.preventDefault();
    showSlide(0);
  }

  if (key === "End") {
    event.preventDefault();
    showSlide(slides.length - 1);
  }

  if (key === "Escape") {
    closeNav();
  }
}

async function toggleFullscreen() {
  if (!document.fullscreenElement) {
    await document.documentElement.requestFullscreen?.();
    return;
  }

  await document.exitFullscreen?.();
}

function handleTouchStart(event) {
  const touch = event.changedTouches[0];
  touchStartX = touch.clientX;
  touchStartY = touch.clientY;
}

function handleTouchEnd(event) {
  const touch = event.changedTouches[0];
  const deltaX = touch.clientX - touchStartX;
  const deltaY = touch.clientY - touchStartY;

  if (Math.abs(deltaY) > Math.abs(deltaX)) return;
  if (Math.abs(deltaX) < 60) return;

  if (deltaX < 0) {
    nextSlide();
  } else {
    previousSlide();
  }
}

buildSlideList();
showSlide(getInitialIndex(), { updateHash: false });
setHash(activeIndex);

prevButton.addEventListener("click", previousSlide);
nextButton.addEventListener("click", nextSlide);
toggleNavButton.addEventListener("click", toggleNav);
fullscreenButton.addEventListener("click", toggleFullscreen);
document.addEventListener("keydown", handleKeyboard);
deck.addEventListener("click", () => {
  if (document.body.classList.contains("nav-open")) {
    closeNav();
  }
});
deck.addEventListener("touchstart", handleTouchStart, { passive: true });
deck.addEventListener("touchend", handleTouchEnd, { passive: true });
globalThis.addEventListener("hashchange", () => {
  showSlide(getInitialIndex(), { updateHash: false });
});
