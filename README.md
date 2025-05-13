# PhotosProyect

## Arquitectura provisional
```bash
proyecto_caras/
├── web/                      # Página web que usa el usuario
│   ├── index.html
│   ├── style.css
│   ├── script.js            # JS separado opcionalmente
│   ├── Dockerfile           # Servidor web (por ejemplo, nginx o Flask)
│   └── uploads/             # Carpeta temporal de imágenes
│
├── api_web/                 # Flask que recibe la imagen y la manda al engine
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── engine/                  # Organiza el flujo entre los modelos
│   ├── appi_organizador.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── bd/                      # Detección de caras
│   ├── detector.py
│   ├── model/               # Modelo preentrenado
│   ├── Dockerfile
│   └── requirements.txt
│
├── clasit/                  # Clasificador de edad
│   ├── clasificador.py
│   ├── model/
│   ├── Dockerfile
│   └── requirements.txt
│
├── pixelado/                # Pixelador de rostros
│   ├── pixelador.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md

```
