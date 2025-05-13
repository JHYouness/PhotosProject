"use client"

import type React from "react"

import { useState } from "react"
import { Upload, ImageIcon, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import Image from "next/image"

export default function ImageProcessor() {
  const [image, setImage] = useState<string | null>(null)
  const [processedImage, setProcessedImage] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null)
    const file = e.target.files?.[0]
    if (!file) return

    // Check if the file is an image
    if (!file.type.startsWith("image/")) {
      setError("Por favor, sube un archivo de imagen válido.")
      return
    }

    // Create a preview of the uploaded image
    const reader = new FileReader()
    reader.onload = () => {
      setImage(reader.result as string)
      setProcessedImage(null)
    }
    reader.readAsDataURL(file)
  }

  const processImage = async () => {
    if (!image) return

    setIsLoading(true)
    setError(null)

    try {
      // Here you would make an API call to your API Gateway
      // For now, we'll simulate a response after a delay
      await new Promise((resolve) => setTimeout(resolve, 2000))

      // Simulate a processed image (in a real app, this would come from your API)
      setProcessedImage(image)
    } catch (err) {
      setError("Ocurrió un error al procesar la imagen. Por favor, intenta de nuevo.")
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container mx-auto py-10 px-4">
      <h1 className="text-3xl font-bold text-center mb-8">Procesador de Imágenes</h1>
      <p className="text-center text-muted-foreground mb-10">
        Sube una imagen para detectar y pixelar automáticamente los rostros de menores de edad
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
        {/* Upload Card */}
        <Card>
          <CardHeader>
            <CardTitle>Subir Imagen</CardTitle>
            <CardDescription>Selecciona una imagen para procesarla</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col items-center">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 w-full h-64 flex flex-col items-center justify-center mb-4">
              {image ? (
                <div className="relative w-full h-full">
                  <Image src={image || "/placeholder.svg"} alt="Imagen subida" fill className="object-contain" />
                </div>
              ) : (
                <>
                  <Upload className="h-10 w-10 text-gray-400 mb-2" />
                  <p className="text-sm text-gray-500">Arrastra y suelta una imagen o haz clic para seleccionar</p>
                </>
              )}
            </div>
            <div className="flex gap-4">
              <Button variant="outline" onClick={() => document.getElementById("image-upload")?.click()}>
                Seleccionar Imagen
              </Button>
              <input id="image-upload" type="file" accept="image/*" className="hidden" onChange={handleImageUpload} />
              <Button onClick={processImage} disabled={!image || isLoading}>
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Procesando...
                  </>
                ) : (
                  "Procesar Imagen"
                )}
              </Button>
            </div>
            {error && <p className="text-red-500 mt-2">{error}</p>}
          </CardContent>
        </Card>

        {/* Result Card */}
        <Card>
          <CardHeader>
            <CardTitle>Resultado</CardTitle>
            <CardDescription>Imagen con rostros de menores pixelados</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col items-center">
            <div className="border-2 border-gray-300 rounded-lg p-6 w-full h-64 flex flex-col items-center justify-center">
              {processedImage ? (
                <div className="relative w-full h-full">
                  <Image
                    src={processedImage || "/placeholder.svg"}
                    alt="Imagen procesada"
                    fill
                    className="object-contain"
                  />
                </div>
              ) : (
                <div className="flex flex-col items-center text-gray-400">
                  <ImageIcon className="h-10 w-10 mb-2" />
                  <p className="text-sm text-gray-500">La imagen procesada aparecerá aquí</p>
                </div>
              )}
            </div>
          </CardContent>
          <CardFooter className="flex justify-center">
            {processedImage && (
              <Button variant="outline" onClick={() => window.open(processedImage)}>
                Ver Imagen Completa
              </Button>
            )}
          </CardFooter>
        </Card>
      </div>
    </div>
  )
}
