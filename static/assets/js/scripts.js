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

            // Create a FormData object and append the new quantity value
            var formData = new FormData();
            formData.append('quantity-input', newValue);

            // Fetch the URL for changing item quantity and submit the form data
            fetch('/change-item-quantity/' + quantityInput.dataset.productId, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                // Handle the response as needed
                console.log('Quantity updated successfully');
            })
            .catch(error => {
                // Handle errors
                console.error('An error occurred:', error);
            });
        }
    });
});




document.addEventListener('DOMContentLoaded', function() {
    updateCartCount(); // Update the cart count when the page loads

    // Function to update the cart count
    function updateCartCount() {
        // Perform an AJAX request to fetch the current cart count from the server
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

    // Add event listener to the "Add to Cart" buttons only once
    var addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(function(button) {
        if (!button.dataset.addToCartListener) {
            button.dataset.addToCartListener = true; // Mark button as having event listener
            button.addEventListener('click', function(event) {
                event.preventDefault(); // Prevent the default form submission

                // Get the product ID from the data attribute of the button
                var productId = button.dataset.productId;

                // Make an AJAX request to add the item to the cart
                fetch('/add-to-cart/' + productId, { method: 'POST' })
                    .then(response => {
                        if (response.ok) {
                            // If the item was successfully added to the cart, update the cart count
                            updateCartCount();
                        } else {
                            console.error('Failed to add item to cart:', response.statusText);
                        }
                    })
                    .catch(error => {
                        console.error('Error adding item to cart:', error);
                    });
            });
        }
    });
});


$(document).ready(function() {
    // Add event listener to the "Add to Cart" buttons only once
    $('.add-to-cart-btn').each(function() {
        var $this = $(this);
        if (!$this.data('addToCartListener')) {
            $this.data('addToCartListener', true); // Mark button as having event listener
            $this.click(function(event) {
                event.preventDefault(); // Prevent the default form submission

                // Get the product ID from the data attribute of the button
                var productId = $this.data('product-id');

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
        }
    });
});








