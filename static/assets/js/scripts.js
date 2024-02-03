/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project


document.addEventListener('DOMContentLoaded', function () {
    var onSaleCheckbox = document.getElementById('on_sale');
    var salePriceLabel = document.querySelector('label[for="sale_price"]');
    var salePriceField = document.getElementById('sale_price');

    // Hide sale_price label and field initially
    salePriceLabel.style.display = onSaleCheckbox.checked ? 'block' : 'none';
    salePriceField.style.display = onSaleCheckbox.checked ? 'block' : 'none';

    // Add change event listener to on_sale checkbox
    onSaleCheckbox.addEventListener('change', function () {
        // Show or hide sale_price label and field based on checkbox state
        salePriceLabel.style.display = this.checked ? 'block' : 'none';
        salePriceField.style.display = this.checked ? 'block' : 'none';
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var starsRange = document.getElementById('stars');
    var starsLabel = document.querySelector('label[for="stars"]');

    // Initialize stars display
    starsLabel.innerHTML = generateStars(starsRange.value);

    // Add input event listener to stars range slider
    starsRange.addEventListener('input', function () {
        // Update stars display based on the range slider value
        starsLabel.innerHTML = generateStars(this.value);
    });

    // Function to generate HTML for stars based on the selected value
    function generateStars(value) {
        var starsHTML = '';
        for (var i = 0; i < value; i++) {
            starsHTML += '⭐';
        }
        return starsHTML;
    }
});



