import math
import random

import tensorflow as tf
from keras import layers, models
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import cv2
import Utils.config as config
import os

EPOCHS = 5

class ArrowCNN:
    def __init__(self):
        # this is the name of the classes the NN predicts
        self.class_names = ['Left', 'Right', 'None']
        # number of outputs the NN can predict 
        self.num_classes = len(self.class_names)
        # saves a model with randomised weights
        self.model = self._build_model()

    def _build_model(self):
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
        # Using the model directly is faster than model.predict for single images
        predictions = self.model(processed, training=False).numpy()
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

def load_images_from_folders(folder_paths, label):
    """
    Helper function to read all .png images from a list of folders
    and attach their class label.
    """
    images_and_labels = []
    
    for folder_path in folder_paths:
        # checks if the folder is a directory 
        if not os.path.isdir(folder_path):
            continue
            
        # Look at every file inside subfolders like 'Left_1'
        for filename in os.listdir(folder_path):
            if filename.endswith('.png'):
                img_path = os.path.join(folder_path, filename)
                # read the image as grayscale (as the CNN will be analysing a masked frame taht is gray scale)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                
                if img is not None:
                    # Append a tuple containing the image array and its label
                    images_and_labels.append((img, label))
                    
    return images_and_labels

def create_dataset_with_images():
    # Master arrays to hold the (image, label) tuples
    train = []
    val = []
    test = []
    
    if not os.path.exists(config.TRAINING_DATA_IMAGES_DIR):
        print(f"Error: Base directory '{config.TRAINING_DATA_IMAGES_DIR}' not found.")
        return train, val, test
        
    classes = ['Left', 'Right', 'None']
    
    for cls in classes:
        class_dir = os.path.join(config.TRAINING_DATA_IMAGES_DIR, cls)
        
        subfolders = [f for f in os.listdir(class_dir) if os.path.isdir(os.path.join(class_dir, f))]
        random.shuffle(subfolders)
        
        total_folders = len(subfolders)
        if total_folders == 0:
            print(f"Warning: No subfolders found in {class_dir}")
            continue
            
        # Calculate indices for the 80/10/10 split
        train_end = math.floor(0.8 * total_folders)
        val_end = math.floor(0.9 * total_folders)
        
        # Construct full folder paths for the splits
        cls_train_folders = [os.path.join(class_dir, f) for f in subfolders[:train_end]]
        cls_val_folders = [os.path.join(class_dir, f) for f in subfolders[train_end:val_end]]
        cls_test_folders = [os.path.join(class_dir, f) for f in subfolders[val_end:]]
        
        print(f"Loading '{cls}' -> Train: {len(cls_train_folders)} folders, Val: {len(cls_val_folders)} folders, Test: {len(cls_test_folders)} folders")

        # Load the actual images from those split folders into the master arrays
        train.extend(load_images_from_folders(cls_train_folders, cls))
        val.extend(load_images_from_folders(cls_val_folders, cls))
        test.extend(load_images_from_folders(cls_test_folders, cls))
        
        # debugging prints
        print(f"\n--- {cls} Image Loading Summary ---")
        print(f"Total Train Images Loaded: {len(train)}")
        print(f"Total Val Images Loaded: {len(val)}")
        print(f"Total Test Images Loaded: {len(test)}")
    return train, val, test

def prep_data(data):
    # randomly shuffling the data
    data_to_prep = data
    random.shuffle(data_to_prep)
    
    classes_as_strings = [item[1] for item in data_to_prep]
    # a dictionary that acts as our translation guide
    class_map = {
        'Left': 0, 
        'Right': 1, 
        'None': 2
    }
    # translate every string into an integer
    integer_labels = [class_map[label] for label in classes_as_strings]
    # Convert the integer list into a numpy array for tensorflow
    cls = np.array(integer_labels)
    
    images = [item[0] for item in data_to_prep]
    # converts the integers used to represent pixel values to floating point numbers so that tensor flow can process it 
    images = np.array(images).astype('float32')
    # normalising the pixel values form 0-255 to 0-1.0
    images = images / 255.0
    # as the initial images for the arrow is grayscale png it does not contain a dimention for colour channels 
    images = np.expand_dims(images, axis=-1) # This adds the channel dimension
    # randomly shuffles the array
    
    return images, cls

def train_model(data_dir):
    # this is the classes of the output layer
    class_names = ['Left', 'Right', 'None']
    # loading the training data
    train, val, test = create_dataset_with_images()
    
    # preparing the training data
    training_images, training_classes = prep_data(train)
    val_images, val_classes = prep_data(val)
    test_images, test_classes = prep_data(test)
    
    # initialising a new model to train
    cnn = ArrowCNN()
    
    # early stopping stopping condition to stop over training 
    es = EarlyStopping(monitor="val_loss", mode="min", patience=10, restore_best_weights=True)
    
    print(f"Starting training for {EPOCHS} epochs...")
    # Further split X_train into training and validation during fit (20% of training data for validation)
    # this also trains the program
    history = cnn.model.fit(training_images,
                training_classes,
                epochs=EPOCHS,
                validation_data=(val_images, val_classes), # this is the validation data for the model
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
    results = cnn.model.evaluate(test_images, test_classes, verbose=1)
    
    # Keras returns [loss, accuracy, error_rate] based on compilation
    test_loss, test_acc = results
    print("=" * 30)
    print(f"Test Accuracy:   {test_acc*100:.2f}%")
    
    # Save the trained model
    cnn.save()
    print(f"Training complete. Model saved to {config.ARROW_CNN_PATH}")

if __name__ == "__main__":
    # If TrainingData exists, run training. Otherwise, just print summary.
    data_path = config.TRAINING_DATA_IMAGES_DIR
    if os.path.exists(data_path) and any(os.scandir(data_path)):
        train_model(data_path)
        print("Completed initial training of ArrowCNN")
    else:
        cnn = ArrowCNN()
        print("CNN Model Summary:")
        cnn.model.summary()
        print(f"\nTraining data not found at {data_path}. Please run generate_arrow_dataset.py first.")