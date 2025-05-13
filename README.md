# PhotosProyect

## Arquitectura provisional
```bash
proyecto_caras/
├── api_gateway/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── engine/
│   ├── appi_organizador.py
│   ├── Dockerfile
│   └── requirements.txt
├── bd/                  # Contenedor del detector de caras
│   ├── detector.py
│   ├── model/           # Aquí va el modelo que te entregarán
│   ├── Dockerfile
│   └── requirements.txt
├── clasit/              # Clasificador de edad
│   ├── clasificador.py
│   ├── model/           # Modelo de clasificación (mayor o menor)
│   ├── Dockerfile
│   └── requirements.txt
├── pixelado/            # Pixelador de rostros menores
│   ├── pixelador.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```
