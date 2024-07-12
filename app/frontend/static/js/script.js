function fetchImages(query) {
    return fetch(`/api/retrieve_by_text?query=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(image_urls => {
            return image_urls.data || [];
        })
        .catch(error => {
            console.error("Error in fetchImages:", error);
            throw error; // Re-throw the error for the caller to handle
        });
}

function displayImages(imageUrls) {
    const gallery = document.getElementById("gallery");
    gallery.innerHTML = "";
    gallery.className = "gallery";

    if (imageUrls.length === 0) {
        gallery.innerHTML =
        '<p class="text-indigo-600 text-center w-full text-lg">No images found.</p>';
        return;
    }

    imageUrls.forEach((imageUrl) => {
        const imgContainer = document.createElement("div");
        imgContainer.className = "gallery-item";

        const imgElement = document.createElement("img");
        imgElement.src = imageUrl;
        imgElement.alt = "Gallery image";
        imgElement.loading = "lazy";

        imgContainer.appendChild(imgElement);
        gallery.appendChild(imgContainer);
    });
}

async function handleSearch(event) {
    event.preventDefault();
    const query = document.getElementById('search-input').value;
    const image_urls = await fetchImages(query);
    displayImages(image_urls);
}

function toggleSearchBar() {
    const searchBar = document.getElementById("search-bar");
    const imageUpload = document.getElementById("image-upload");
    const gallerySection = document.getElementById("gallery-section");

    searchBar.classList.toggle("visible");
    imageUpload.classList.remove("visible");

    if (searchBar.classList.contains("visible")) {
        searchBar.style.display = "block"; // Add this line
        searchBar.classList.add("slide-down");
        gallerySection.classList.add("moved-down");
        setTimeout(() => {
        searchBar.classList.remove("slide-down");
        }, 500);
    } else {
        setTimeout(() => {
        searchBar.style.display = "none"; // Add this line
        }, 500);
        gallerySection.classList.remove("moved-down");
    }
}

function toggleImageUpload() {
    const searchBar = document.getElementById("search-bar");
    const imageUpload = document.getElementById("image-upload");
    const gallerySection = document.getElementById("gallery-section");

    imageUpload.classList.toggle("visible");
    searchBar.classList.remove("visible");

    if (imageUpload.classList.contains("visible")) {
        imageUpload.style.display = "block"; // Add this line
        imageUpload.classList.add("slide-down");
        gallerySection.classList.add("moved-down");
        setTimeout(() => {
        imageUpload.classList.remove("slide-down");
        }, 500);
    } else {
        setTimeout(() => {
        imageUpload.style.display = "none"; // Add this line
        }, 500);
        gallerySection.classList.remove("moved-down");
    }
}

async function handleImageUpload(event) {
    event.preventDefault();
    const formData = new FormData();
    const imageFile = document.getElementById('image-input').files[0];
    formData.append('image', imageFile);

    try {
        const response = await fetch('/api/retrieve_by_image', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        displayImages(result.data || []);
    } catch (error) {
        console.error("Error in handleImageUpload:", error);
        alert("An error occurred while uploading the image. Please try again.");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('image-upload-form').addEventListener('submit', handleImageUpload);
});
