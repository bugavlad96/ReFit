const Cards = (() => {
  window.addEventListener('DOMContentLoaded', () => {
    setTimeout(init, 1);
  }, true);

  function init(e) {
    if (document.querySelector(".cards")) {
      let cards = document.querySelectorAll(".cards .card");
      cards.forEach((card, index) => {
        card.addEventListener('click', clicked, false);
        card.setAttribute("data-card", index);
      });
      document.querySelector(".cards .card[data-card='0']").click();
    }
  }

  function clicked(e) {
    let card = e.target;
    if (card.getAttribute("data-card")) {
      rearrange(card.getAttribute("data-card"));
    }
  }

  function rearrange(card) {
    let cards = document.querySelectorAll(".cards .card");
    cards.forEach((card) => {
      card.classList.remove("card--left");
      card.classList.remove("card--center");
      card.classList.remove("card--right");
      card.classList.remove("card--leftmost");
      card.classList.remove("card--rightmost");
    });
    cards[card].classList.add("card--center");

    const leftIndex = (parseInt(card) - 1 + cards.length) % cards.length;
    const rightIndex = (parseInt(card) + 1) % cards.length;
    const leftmostIndex = (parseInt(card) - 2 + cards.length) % cards.length;
    const rightmostIndex = (parseInt(card) + 2) % cards.length;

    cards[leftIndex].classList.add("card--left");
    cards[rightIndex].classList.add("card--right");
    cards[leftmostIndex].classList.add("card--leftmost");
    cards[rightmostIndex].classList.add("card--rightmost");
  }

  return {
    init
  };
})();
