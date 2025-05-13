I'll create a frontend for your image processing application that allows users to upload images and view the pixelated results.

```typescriptreact project="image-processor"
...
```

Este frontend permite a los usuarios:

1. Subir imágenes a través de un selector de archivos o arrastrar y soltar
2. Ver una vista previa de la imagen subida
3. Procesar la imagen (que enviará la imagen a tu API Gateway)
4. Ver el resultado procesado con los rostros de menores pixelados


Para integrar completamente esta interfaz con tu arquitectura de contenedores, necesitarás:

1. Modificar la función `processImage` en `page.tsx` para enviar la imagen a tu API Gateway
2. Actualizar la ruta API en `app/api/process-image/route.ts` para comunicarse con tu Engine API


Esta es una estructura básica que puedes expandir según tus necesidades específicas. La interfaz es responsive y ofrece una experiencia de usuario intuitiva.
