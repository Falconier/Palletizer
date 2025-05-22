document.getElementById('sellerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const seller = {
        seller_name: document.getElementById('seller_name').value,
        seller_website: document.getElementById('seller_website').value
    };
    fetch('/add_seller', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(seller)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.message);
            });
        }
        return response.json();
    })
    .then(data => {
        alert('Seller added successfully!');
        this.reset();
    })
    .catch(error => {
        alert('Error adding seller: ' + error.message);
    });
});