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



$(document).ready(function() {
    // Function to update the cart count
    function updateCartCount() {
        // Perform an AJAX request to fetch the current cart count from the server
        fetch('/get-cart-count')
            .then(response => response.json())
            .then(data => {
                // Update the cart count in the header
                $('#cart-count').text(data.cart_count);
            })
            .catch(error => {
                console.error('Error fetching cart count:', error);
            });
    }

    // Add event listener to the "Add to Cart" buttons
    $('.add-to-cart-btn').click(function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get the product ID from the data attribute of the button
        var productId = $(this).data('product-id');

        // Make an AJAX request to add the item to the cart
        fetch('/add-to-cart/' + productId, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    // If the item was successfully added to the cart, update the cart count
                    updateCartCount();
                } else {
                    console.error('Failed to add item to cart:', response.statusText);
                    // Optionally, display an error message
                    alert('An error occurred while adding the item to the cart.');
                }
            })
            .catch(error => {
                console.error('Error adding item to cart:', error);
                // Optionally, display an error message
                alert('An error occurred while adding the item to the cart.');
            });
    });

    // Update the cart count when the page loads
    updateCartCount();
});








