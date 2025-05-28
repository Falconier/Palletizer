document.addEventListener('DOMContentLoaded', () => {
    loadSellers();
});

document.getElementById('in_boxes').addEventListener('change', function() {
    const itemsPerBoxContainer = document.getElementById('items_per_box_container');
    itemsPerBoxContainer.classList.toggle('hidden', !this.checked);
    if (this.checked) {
        document.getElementById('items_per_box').required = true;
    } else {
        document.getElementById('items_per_box').required = false;
    }
});

document.getElementById('itemForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const item = {
        item_upc: document.getElementById('item_upc').value,
        item_mn: document.getElementById('item_model_number').value,
        item_pn: document.getElementById('item_part_number').value,
        item_name: document.getElementById('item_name').value,
        item_desc: document.getElementById('item_description').value,
        item_price: document.getElementById('item_price').value,
        items_per_pallet: document.getElementById('items_per_pallet').value,
        in_box: document.getElementById('in_boxes').checked,
        items_per_box: document.getElementById('items_per_box_container').value,
        seller_id: document.getElementById('seller_id').value,
        seller_sku: document.getElementById('seller_sku').value
    };
    fetch('/add_inventory', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(item)
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
        alert('Item added successfully!');
        this.reset();
        document.getElementById('items_per_box_container').classList.add('hidden');
        document.getElementById('items_per_box').required = false;
        document.getElementById('in_boxes').checked = false;
    })
    .catch(error => {
        alert('Error adding item: ' + error.message);
    });
});

function loadSellers() {
    fetch('/sellers')
        .then(response => response.json())
        .then(sellers => {
            const sellerSelect = document.getElementById('seller_id');
            sellerSelect.innerHTML = '';
            sellers.forEach(seller => {
                const option = document.createElement('option');
                option.value = seller.seller_id;
                option.textContent = seller.seller_name;
                sellerSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading sellers:', error));
}