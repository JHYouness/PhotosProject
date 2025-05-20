const input = document.getElementById('imageInput');
const previewImage = document.getElementById('previewImage');
const resultImage = document.getElementById('resultImage');
const processBtn = document.getElementById('processBtn');
const viewBtn = document.getElementById('viewBtn');

input.addEventListener('change', () => {
  const file = input.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

processBtn.addEventListener('click', async () => {
  const file = input.files[0];
  if (!file) {
    alert('Selecciona una imagen.');
    return;
  }

  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error('Error al procesar');

    const data = await response.json();
    const resultUrl = `http://localhost:5000/uploads/processed/${data.filename}`;
    resultImage.src = resultUrl;
    viewBtn.href = resultUrl;
    viewBtn.style.display = 'inline-block';
  } catch (error) {
    alert('Hubo un error al procesar la imagen.');
    console.error(error);
  }
});
