document.addEventListener('DOMContentLoaded', function() {
    const imageGrid = document.getElementById('imageGrid');
    const dropBox = document.getElementById('dropBox');
    const results = document.getElementById('results');

    // Load initial CIFAR images (stored locally)
    const imageUrls = [
        'images/frog.png', 'images/deer.png', 'images/plane.png', 'images/horse.png'
    ];
    imageUrls.forEach(url => {
        const img = document.createElement('img');
        img.src = url;
        img.draggable = true;
        img.addEventListener('dragstart', handleDragStart);
        imageGrid.appendChild(img);
    });

    dropBox.addEventListener('dragover', function(event) {
        event.preventDefault();
    });

    dropBox.addEventListener('drop', function(event) {
        event.preventDefault();
        const imageUrl = event.dataTransfer.getData('text');
        retrieveSimilarImages(imageUrl);
    });

    function handleDragStart(event) {
        event.dataTransfer.setData('text', event.target.src);
    }

    function retrieveSimilarImages(imageUrl) {
        fetch(imageUrl) // Fetch the image from the local server
        .then(response => response.blob()) // Convert the image to a blob
        .then(blob => {
            var formData = new FormData();
            formData.append('file', blob, imageUrl.split('/').pop()); // Append the blob to the FormData, naming the file as its original name

            // AJAX call to Flask backend
            fetch(`${config.apiUrl}/infer`, {
                method: 'POST',
                body: formData, // Send the form data
                // Note: Do not set 'Content-Type' header when sending FormData
            })
            .then(response => response.json())
            .then(data => {
                results.innerHTML = ''; // Clear previous results
                data.images.forEach(imgData => {
                    const img = document.createElement('img');
                    img.src = imgData;
                    results.appendChild(img);
                });
            })
            .catch(error => console.error('Error:', error));
        })
        .catch(error => console.error('Error fetching the image:', error));
    }
});
