document.addEventListener("DOMContentLoaded", function () {
    const photoInput = document.querySelector("#id_photo");
    if (!photoInput) {
        return;
    }
    const video = document.querySelector("#camera-stream");
    const canvas = document.querySelector("#snapshot");

    const captureButton = document.querySelector("#capture-btn");
    const photoTakeContainer = document.querySelector("#photo-take");
    const photoContainer = document.querySelector("#photo-container");
    const capturedPhoto = document.querySelector("#captured-photo");
    const retakeButton = document.querySelector("#retake-btn");
    const mainCameraContainer = document.querySelector("#main-camera-container");


    mainCameraContainer.style.display = "block";


    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
                video.play();
            })
            .catch(function (error) {
                console.error("Camera access denied: ", error);
            });
    }

    captureButton.addEventListener("click", function () {
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(function (blob) {
            const file = new File([blob], "photo.jpg", { type: "image/jpeg" });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            photoInput.files = dataTransfer.files;

            // Display the captured image
            const imgUrl = URL.createObjectURL(blob);
            capturedPhoto.src = imgUrl;
            photoContainer.style.display = "block"; // Show the result section
            photoTakeContainer.style.display = "none";
        });
    });

    retakeButton.addEventListener("click", function () {
        // Hide the result and show the video stream again
        photoContainer.style.display = "none";
        photoTakeContainer.style.display = "block";
    });
});