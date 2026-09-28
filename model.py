import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

def get_class(model_path, labels_path, image_path):
    # Desactiva la notación científica para mayor claridad
    np.set_printoptions(suppress=True)

    # Carga el modelo entrenado
    model = tf.keras.models.load_model(model_path, compile=False)

    # Carga las etiquetas (labels)
    with open(labels_path, "r", encoding="utf-8") as f:
        class_names = f.readlines()

    # Crea el array de la forma correcta para alimentar al modelo keras
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Abre la imagen enviada
    image = Image.open(image_path).convert("RGB")

    # Redimensiona la imagen a 224x224 (tamaño estándar para estos modelos)
    # y usa un recorte inteligente para que no se deforme
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # Convierte la imagen en un array de numpy
    image_array = np.asarray(image)

    # Normaliza la imagen (escala los valores de los píxeles)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Carga la imagen normalizada en la matriz principal
    data[0] = normalized_image_array

    # Realiza la predicción con el modelo
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # Devuelve el nombre de la clase y la confianza de la predicción
    return class_name, confidence_score