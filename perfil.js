const fileInput = document.getElementById("file-input");
const preview = document.getElementById("preview");

fileInput.addEventListener("change", function() {
    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();

    reader.onload = function(e) {
        preview.src = e.target.result;
    };

    reader.readAsDataURL(file);
});
