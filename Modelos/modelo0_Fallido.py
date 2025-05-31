# 6. Modelo CNN
input_shape = (224, 224, 3)
batch_size = 32
epochs = 20

def crear_modelo_cnn(input_shape):
    model = models.Sequential()

    # Bloque 1
    model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    # Bloque 2
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    # Bloque 3
    model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    # Bloque 4 (opcional)
    model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.25))

    # Clasificación
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1, activation='sigmoid'))  # salida binaria

    return model

model = crear_modelo_cnn(input_shape)

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy', tf.keras.metrics.AUC(name="AUC"),
                       tf.keras.metrics.Precision(name="precision"),
                       tf.keras.metrics.Recall(name="recall")])

model.summary()

# 7. Generadores de datos
train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True,
                                   rotation_range=10, brightness_range=(0.9, 1.1))
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    str(base_output_path / "train"),
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='binary',
    shuffle=True
)

val_generator = val_datagen.flow_from_directory(
    str(base_output_path / "validation"),
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='binary',
    shuffle=True
)

# 8. Entrenar

checkpoint = ModelCheckpoint(
    filepath='mejor_modelo.keras',
    monitor='val_precision',
    mode='max',
    save_best_only=True,
    verbose=1
)

early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

history = model.fit(train_generator,
                    validation_data=val_generator,
                    epochs=epochs,
                    callbacks=[checkpoint, early_stop])


"""
Mejor resultado:
val_AUC: 0.9817 - val_accuracy: 0.9133 - val_loss: 0.1863 - val_precision: 0.9733 - val_recall: 0.8478
"""
