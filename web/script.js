document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const uploadArea = document.getElementById("upload-area")
  const uploadIcon = document.getElementById("upload-icon")
  const previewImage = document.getElementById("preview-image")
  const selectButton = document.getElementById("select-button")
  const imageUpload = document.getElementById("image-upload")
  const processButton = document.getElementById("process-button")
  const errorMessage = document.getElementById("error-message")
  const resultPlaceholder = document.getElementById("result-placeholder")
  const resultImage = document.getElementById("result-image")
  const viewButton = document.getElementById("view-button")
  const loadingOverlay = document.getElementById("loading-overlay")

  // Variables to store image data
  let uploadedImage = null

  // Event Listeners
  uploadArea.addEventListener("click", () => {
    imageUpload.click()
  })

  uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault()
    uploadArea.classList.add("drag-over")
  })

  uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("drag-over")
  })

  uploadArea.addEventListener("drop", (e) => {
    e.preventDefault()
    uploadArea.classList.remove("drag-over")

    if (e.dataTransfer.files.length) {
      handleFileSelect(e.dataTransfer.files[0])
    }
  })

  selectButton.addEventListener("click", () => {
    imageUpload.click()
  })

  imageUpload.addEventListener("change", function () {
    if (this.files.length) {
      handleFileSelect(this.files[0])
    }
  })

  processButton.addEventListener("click", processImage)

  viewButton.addEventListener("click", () => {
    if (resultImage.src) {
      window.open(resultImage.src)
    }
  })

  // Functions
  function handleFileSelect(file) {
    // Reset error message
    errorMessage.classList.add("hidden")
    errorMessage.textContent = ""

    // Check if file is an image
    if (!file.type.startsWith("image/")) {
      showError("Por favor, sube un archivo de imagen válido.")
      return
    }

    // Create a preview of the uploaded image
    const reader = new FileReader()
    reader.onload = (e) => {
      uploadedImage = e.target.result
      previewImage.src = uploadedImage
      previewImage.classList.remove("hidden")
      uploadIcon.classList.add("hidden")
      processButton.disabled = false

      // Reset result area
      resultImage.classList.add("hidden")
      resultPlaceholder.classList.remove("hidden")
      viewButton.classList.add("hidden")
    }
    reader.readAsDataURL(file)
  }

  function processImage() {
    if (!uploadedImage) return

    // Show loading overlay
    loadingOverlay.classList.remove("hidden")

    // Simulate processing delay
    setTimeout(() => {
      // Hide loading overlay
      loadingOverlay.classList.add("hidden")

      // Display processed image (in this demo, we just use the same image)
      resultImage.src = uploadedImage
      resultImage.classList.remove("hidden")
      resultPlaceholder.classList.add("hidden")
      viewButton.classList.remove("hidden")
    }, 2000)
  }

  function showError(message) {
    errorMessage.textContent = message
    errorMessage.classList.remove("hidden")
  }
})
