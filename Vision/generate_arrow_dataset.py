import cv2
import numpy as np
import os
import random

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

def generate_dataset(base_images_dir, output_dir, samples_per_class=1000):
    """
    Generates an augmented dataset from base images.
    Even if the track arrow is black, the OpenCV mask makes it WHITE.
    So we ALWAYS generate white-on-black for the CNN.
    """
    classes = ['Left', 'Right']
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for cls in classes:
        print(f"Generating data for class: {cls}")
        base_path = os.path.join(base_images_dir, f"{cls}.png")
        if not os.path.exists(base_path):
            print(f"Warning: Base image {base_path} not found. Skipping {cls}.")
            continue
            
        base_img = cv2.imread(base_path, cv2.IMREAD_GRAYSCALE)
        
        # AUTO-INVERSION LOGIC:
        # We want White Arrow (255) on Black Background (0).
        # If the image is mostly white (mean > 127), it's a black arrow on white.
        # We invert it so the CNN sees what the HSV filter will produce.
        if np.mean(base_img) > 127:
            print(f"  Notice: Inverting {cls}.png (Black-on-White) to White-on-Black for Mask matching...")
            base_img = cv2.bitwise_not(base_img)
        else:
            print(f"  Notice: {cls}.png is already White-on-Black.")
            
        base_img = cv2.resize(base_img, (64, 64))
        
        class_output_dir = os.path.join(output_dir, cls)
        if not os.path.exists(class_output_dir):
            os.makedirs(class_output_dir)
            
        for i in range(samples_per_class):
            augmented = augment_image(base_img.copy())
            cv2.imwrite(os.path.join(class_output_dir, f"{cls}_{i}.png"), augmented)

    print(f"Dataset generation complete. Saved to {output_dir}")

if __name__ == "__main__":
    generate_dataset("Vision/BaseArrows", "Vision/TrainingData", samples_per_class=500)
