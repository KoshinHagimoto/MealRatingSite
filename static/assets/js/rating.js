'use strict'

const rating = document.querySelectorAll('#id_rating').item(0);
// console.log(rating.value);

rating.addEventListener('change', () => {
    let ratingDisplay = document.querySelectorAll('#rating-display').item(0);
    ratingDisplay.innerHTML = rating.value
    console.log(ratingDisplay.value);
})