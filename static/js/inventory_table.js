document.addEventListener('DOMContentLoaded', () => {
    loadInventory();
});

function loadInventory() {
    fetch('/inventory')
        .then(response => response.json())
        .then(items => {
            const tbody = document.querySelector('#itemTable tbody');
            tbody.innerHTML = '';
            items.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="libre-barcode-128-text-regular">${item.item_upc}</td>
                    <td>${item.item_model_number}</td>
                    <td>${item.item_part_number}</td>
                    <td>${item.item_name}</td>
                    <td>${item.item_description}</td>
                    <td>${item.item_price}</td>
                    <td>${item.items_per_pallet}</td>
                    <td>${item.in_box}</td>
                    <td>${item.items_per_box}</td>
                    <td><button class="btn btn-info btn-sm" onclick="Details(${item.item_id})">View Details</button></td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error loading inventory:', error));
}