function showFullTags(element) {
    let container = element.closest('td, div');  // Works in both list and detail views
    let preview = container.querySelector('.tag-preview');
    let full = container.querySelector('.tag-full');

    if (preview.style.display === "none") {
        preview.style.display = "inline";
        full.style.display = "none";
        element.textContent = "Show All";
    } else {
        preview.style.display = "none";
        full.style.display = "inline";
        element.textContent = "Show Less";
    }
}
