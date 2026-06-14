import cv2
import numpy as np
import os
import random
import Utils.config as config

def augment_image(image):
    """
    Applies random augmentations to an image to simulate real-world conditions.
    The CNN ALWAYS expects a WHITE arrow on a BLACK background because 
    that is what the OpenCV HSV mask produces.
    """
    h, w = image.shape
    bg_color = 0 # Black background (standard for masks)
    
    # 1. Random Rotation (-15 to 15 degrees)
    angle = random.uniform(-15, 15)
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    image = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=bg_color)
    
    # 2. Random Scaling (0.8 to 1.2)
    scale = random.uniform(0.8, 1.2)
    new_w, new_h = int(w * scale), int(h * scale)
    image = cv2.resize(image, (new_w, new_h))
    
    # Pad or crop to return to 64x64
    if scale > 1.0:
        # Crop
        start_x = (new_w - w) // 2
        start_y = (new_h - h) // 2
        image = image[start_y:start_y+h, start_x:start_x+w]
    else:
        # Pad
        pad_x = (w - new_w) // 2
        pad_y = (h - new_h) // 2
        image = cv2.copyMakeBorder(image, pad_y, h - new_h - pad_y, pad_x, w - new_w - pad_x, 
                                   cv2.BORDER_CONSTANT, value=bg_color)

    # 3. Random Perspective Transform (simulate camera angle)
    pts1 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    offset = 5
    pts2 = np.float32([
        [random.uniform(0, offset), random.uniform(0, offset)],
        [w - random.uniform(0, offset), random.uniform(0, offset)],
        [random.uniform(0, offset), h - random.uniform(0, offset)],
        [w - random.uniform(0, offset), h - random.uniform(0, offset)]
    ])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    image = cv2.warpPerspective(image, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=bg_color)

    # 4. Add Noise (Gaussian)
    noise = np.random.normal(0, 5, image.shape).astype(np.uint8)
    image = cv2.add(image, noise)

    # 5. Random Blur
    if random.random() > 0.5:
        k_size = random.choice([3, 5])
        image = cv2.GaussianBlur(image, (k_size, k_size), 0)

    return image

def generate_none_image(h=64, w=64):
    """Generates a random non-arrow image (noise, blank, or random shape)"""
    bg_color = 0
    image = np.full((h, w), bg_color, dtype=np.uint8)
    
    choice = random.randint(0, 3)
    if choice == 0:
        # Return mostly blank image
        pass
    elif choice == 1:
        # Add random noise
        noise = np.random.normal(0, 50, (h, w)).astype(np.uint8)
        image = cv2.add(image, noise)
    elif choice == 2:
        # Draw a random white line (simulating track lines)
        pt1 = (random.randint(0, w), random.randint(0, h))
        pt2 = (random.randint(0, w), random.randint(0, h))
        thickness = random.randint(2, 10)
        cv2.line(image, pt1, pt2, 255, thickness)
    else:
        # Draw a random white blob/circle (simulating obstacle/noise)
        center = (random.randint(0, w), random.randint(0, h))
        radius = random.randint(5, 20)
        cv2.circle(image, center, radius, 255, -1)
        
    return augment_image(image)

# Generates an augmented dataset from both base images and captured images.
def generate_dataset( 
    samples_per_class=1000
):
    classes = ['Left', 'Right', 'None']
    
    if not os.path.exists(config.TRAINING_DATA_IMAGES_DIR):
        os.makedirs(config.TRAINING_DATA_IMAGES_DIR)

    for cls in classes:
        print(f"Generating data for class: {cls}")
        class_output_dir = os.path.join(config.TRAINING_DATA_IMAGES_DIR, cls)
        
        # this makes the output directory for the class if it doesnt already exist
        if not os.path.exists(class_output_dir):
            os.makedirs(class_output_dir)
            
        # For loading the captured imgaes into
        source_images = []
        
        # Load Captured Images
        captured_images = os.path.join(config.CAPTURED_IMAGES_DIR, cls)
        if os.path.exists(captured_images):
            # gets all the captured images file names
            file_names = [f for f in os.listdir(captured_images) if f.endswith('.png')]
            print(f"  Found {len(file_names)} captured images for {cls}")
            # loads each image into the source image file
            for filename in file_names:
                img_path = os.path.join(captured_images, filename)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    source_images.append(img)

        if not source_images:
            print(f"Warning: No source images found for {cls}. Skipping.")
            continue
            
        # Augment all source images to reach samples_per_class roughly
        num_sources = len(source_images)
        samples_per_source = samples_per_class // num_sources
        
        print(f"  Augmenting {num_sources} source images ({samples_per_source} samples each)...")
        num_sources = 0
        count = 0
        for src_img in source_images:
            src_img = cv2.resize(src_img, (64, 64))
            num_sources += 1
            source_segment = os.path.join(class_output_dir, f"{cls}_{num_sources}")
            # makes the directory for the segment if it doesnt exist
            if not os.path.exists(source_segment):
                os.makedirs(source_segment)
            
            print(f"Generating images for: {source_segment}")
            for _ in range(samples_per_source):
                count += 1
                augmented = augment_image(src_img.copy())
                # this makes it so that all images that are created based on one source are segmented based on that source 
                cv2.imwrite(os.path.join(source_segment, f"{cls}_{count}.png"), augmented)
    
    print(f"Dataset generation complete. Saved to {config.TRAINING_DATA_IMAGES_DIR}")

if __name__ == "__main__":
    generate_dataset(samples_per_class=2000)
