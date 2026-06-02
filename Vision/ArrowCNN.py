import tensorflow as tf
from keras import layers, models
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import cv2
import config
import os

EPOCHS = 30

class ArrowCNN:
    def __init__(self):
        # this is the name of the classes the NN predicts
        self.class_names = ['Left', 'Right']
        # number of outputs the NN can predict 
        self.num_classes = len(self.class_names)
        # saves a model with randomised weights
        self.model = self._build_model()

    def _build_model(self):
        """Defines the CNN architecture with accuracy and error rate metrics."""
        # this is the structure of the NN recomended by Gemini 
        model = models.Sequential([
            layers.Input(shape=config.INPUT_SHAPE),
            layers.Conv2D(32, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # this compiles the NN with random weights
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def preprocess_image(self, mask):
        """
        Preprocesses an OpenCV mask (binary image) for the CNN.
        :param mask: Binary image from HSV filtering.
        :return: Normalized and reshaped image.
        """
        # Resize to model input shape
        resized = cv2.resize(mask, (config.INPUT_SHAPE[1], config.INPUT_SHAPE[0]))
        
        # Normalize pixel values (0-255 -> 0-1.0)
        normalized = resized.astype('float32') / 255.0
        
        # Add channel and batch dimensions
        reshaped = np.expand_dims(normalized, axis=(0, -1))
        return reshaped

    def predict(self, mask):
        """
        Predicts the direction from a mask.
        :param mask: Binary image from HSV filtering.
        :return: String (Direction Name), confidence score.
        """
        processed = self.preprocess_image(mask)
        predictions = self.model.predict(processed, verbose=0)
        class_idx = np.argmax(predictions[0])
        confidence = predictions[0][class_idx]
        
        return self.class_names[class_idx], confidence

    def save(self):
        """
        Saves the model weights and architecture to a .keras file.
        """
        self.model.save(config.ARROW_CNN_PATH)

    def load(self):
        """
        Loads the model weights and architecture from a .keras file.
        """
        self.model = tf.keras.models.load_model(config.ARROW_CNN_PATH)

def train_model(data_dir):
    # this is the classes of the output layer
    class_names = ['Left', 'Right']
    images = []
    indexes = []

    # this loads the data for testing
    print(f"Loading training data from {data_dir}...")
    for index, name in enumerate(class_names):
        folder = os.path.join(data_dir, name)

        # this checks if the training data folder exists
        if not os.path.exists(folder):
            print(f"Warning: Folder {folder} not found. Skipping.")
            continue
        
        # loads the data for training
        for filename in os.listdir(folder):
            # processing the individual image into a cv2 format
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            # checks that the image is indeed an image
            if img is not None:
                # Resize to match CNN input
                img = cv2.resize(img, (config.INPUT_SHAPE[1], config.INPUT_SHAPE[0]))
                images.append(img)
                indexes.append(index)

    # checks how many images were loaded
    if not images:
        print("Error: No images found for training.")
        return
    else:
        print(f"The number of images loaded for training is: {len(images)}")

    # converts the integers used to represent pixel values to floating point numbers so that tensor flow can process it 
    images = np.array(images).astype('float32')
    # normalising the pixel values form 0-255 to 0-1.0
    images = images / 255.0
    # as the initial images for the arrow is grayscale png it does not contain a dimention for colour channels 
    images = np.expand_dims(images, axis=-1) # This adds the channel dimension
    indexes = np.array(indexes)

    # split into train and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(images, indexes, test_size=0.2, random_state=42)

    # initialising a new model to train
    cnn = ArrowCNN()
    
    # early stopping stopping condition to stop over training 
    es = EarlyStopping(monitor="val_loss", mode="min", patience=10, restore_best_weights=True)
    
    print(f"Starting training for {EPOCHS} epochs...")
    # Further split X_train into training and validation during fit (20% of training data for validation)
    # this also trains the program
    history = cnn.model.fit(X_train,
                y_train,
                epochs=EPOCHS,
                validation_split=0.2,
                batch_size=32, # number of samples processed before the weights are updated
                callbacks=[es], # setting early stopping conditions
                verbose=1 # shows a progress bar.
                )

    # determine the number of epochs actually run (in case early stopping kicked in)
    n_plot = min(EPOCHS, len(history.history["loss"]))
    x = np.arange(1, n_plot + 1)

    # plotting
    plt.figure()
    plt.plot(x, history.history["loss"], label="Training Loss", color="blue")
    plt.plot(x, history.history["val_loss"], label="Validation Loss", color="purple")

    # plot labels
    plt.xlabel("Training Epoch")
    plt.ylabel("MSE Loss")
    plt.title("ArrowCNN losses")

    # layout and legend
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=False)
    plt.grid()  # Adds a grid to the plot
    plt.tight_layout()
    plt.show()
    
    # evaluate on the unseen test set
    print("\nEvaluating on Test Set (Unseen Data)...")
    results = cnn.model.evaluate(X_test, y_test, verbose=1)
    
    # Keras returns [loss, accuracy, error_rate] based on compilation
    test_loss, test_acc = results
    print("=" * 30)
    print(f"Test Accuracy:   {test_acc*100:.2f}%")
    
    # Save the trained model
    cnn.save()
    print(f"Training complete. Model saved to {config.ARROW_CNN_PATH}")

if __name__ == "__main__":
    # If TrainingData exists, run training. Otherwise, just print summary.
    data_path = "Vision/TrainingData"
    if os.path.exists(data_path) and any(os.scandir(data_path)):
        train_model(data_path)
        print("Completed initial training of ArrowCNN")
    else:
        cnn = ArrowCNN()
        print("CNN Model Summary:")
        cnn.model.summary()
        print(f"\nTraining data not found at {data_path}. Please run generate_arrow_dataset.py first.")