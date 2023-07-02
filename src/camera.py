import numpy as np
import cv2 as cv
import tensorflow as tf


# def preprocess_image(image):
#     gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#     resized = cv.resize(gray, (28, 28), interpolation=cv.INTER_AREA)
#     normalized = resized / 255.0
#     reshaped = np.reshape(normalized, (-1, 28, 28, 1))
#     return reshaped

def preprocess_image(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # Apply image enhancement techniques (e.g., histogram equalization)
    enhanced = cv.equalizeHist(gray)
    
    # Apply adaptive thresholding to convert to binary image
    _, thresholded = cv.threshold(enhanced, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    
    # Resize the image to the desired dimensions
    resized = cv.resize(thresholded, (28, 28), interpolation=cv.INTER_AREA)
    
    # Normalize the image
    normalized = resized / 255.0
    
    # Reshape the image
    reshaped = np.reshape(normalized, (-1, 28, 28, 1))
    
    return reshaped



def classify_digit(image):
    preprocessed = preprocess_image(image)
    prediction = model.predict(preprocessed)
    print(prediction)
    label = np.argmax(prediction)
    confidence = prediction[0][label]
    return label, confidence


if __name__ == "__main__":
    model = tf.keras.models.load_model('model/digit_classifier_model.h5')
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        if cv.waitKey(1) == ord('q'):
            break

        label, confidence = classify_digit(frame)
        cv.putText(frame, f'Prediction: {label}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv.putText(frame, f'Confidence: {confidence}', (10, 70), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv.imshow('Camera', frame)
    cap.release()
    cv.destroyAllWindows()
