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

document.addEventListener('DOMContentLoaded', function() {
    var quantityInput = document.getElementById('quantity-input');
    quantityInput.addEventListener('input', function(event) {
        var newValue = parseInt(quantityInput.value);
        if (!isNaN(newValue)) {
            var min = parseInt(quantityInput.min);
            var max = parseInt(quantityInput.max);
            if (newValue < min) {
                newValue = min;
            } else if (newValue > max) {
                newValue = max;
            }
            quantityInput.value = newValue;
            // Submit the form after updating the input field
            document.getElementById('quantity-form').submit();
        }
    });
});



document.addEventListener('DOMContentLoaded', function() {
    updateCartCount(); // Update the cart count when the page loads

    // Function to update the cart count
    function updateCartCount() {
        // Perform an AJAX request to fetch the current cart count from the server
        // You need to implement this AJAX request endpoint in your Flask application
        fetch('/get-cart-count')
            .then(response => response.json())
            .then(data => {
                // Update the cart count in the header
                document.getElementById('cart-count').textContent = data.cart_count;
            })
            .catch(error => {
                console.error('Error fetching cart count:', error);
            });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var quantityInputs = document.querySelectorAll('.quantity-input');
    console.log('Found quantity inputs:', quantityInputs);
    quantityInputs.forEach(function(quantityInput) {
        quantityInput.addEventListener('input', function(event) {
            console.log('Input field value:', quantityInput.value);
            // Add other debug logs as needed
            // Your existing code follows...
        });
    });
});

// script.js

$(document).ready(function() {
    $('.add-to-cart-btn').click(function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get the product ID from the data attribute of the button
        var productId = $(this).data('product-id');

        // Make an AJAX request to your Flask route
        $.ajax({
            type: 'POST',
            url: '/add-to-cart/' + productId,
            success: function(response) {
                // Handle the success response here, for example, you could display a success message
                alert('Item added to cart successfully!');
            },
            error: function(xhr, status, error) {
                // Handle any errors that occur during the AJAX request
                console.error(error);
                alert('An error occurred while adding the item to the cart.');
            }
        });
    });
});







