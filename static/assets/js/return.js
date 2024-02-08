initialize();

async function initialize() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const sessionId = urlParams.get('session_id');
  const response = await fetch(`/session-status?session_id=${sessionId}`);
  const session = await response.json();

  if (session.status == 'open') {
    window.replace('http://localhost:4242/checkout.html')
  } else if (session.status == 'complete') {
    document.getElementById('success').classList.remove('hidden');
    document.getElementById('customer-email').textContent = session.customer_email
    document.getElementById('customer-name').textContent = session.customer_name

    // Make an AJAX request to the empty-cart route
    $.ajax({
        type: 'POST',
        url: '/empty-cart',
        success: function(response) {
            // Handle the success response here, if needed
            console.log('Cart emptied successfully');
        },
        error: function(xhr, status, error) {
            // Handle any errors that occur during the AJAX request
            console.error(error);
            alert('An error occurred while emptying the cart.');
        }
  }
}