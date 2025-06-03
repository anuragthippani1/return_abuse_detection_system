import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from typing import Tuple, Dict

class VisualInspector:
    def __init__(self):
        # Initialize ORB detector and Brute Force matcher
        self.orb = cv2.ORB_create()
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Weights for similarity scoring
        self.weights = {
            'ssim': 0.4,
            'hist': 0.3,
            'features': 0.3
        }
        self.similarity_threshold = 0.7

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale, resize, and blur."""
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(image, (800, 800))
        blurred = cv2.GaussianBlur(resized, (5, 5), 0)
        return blurred

    def compute_histogram(self, image: np.ndarray) -> np.ndarray:
        """Compute and normalize histogram (grayscale or BGR)."""
        if len(image.shape) == 3:
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                                [0, 256, 0, 256, 0, 256])
        else:
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        return cv2.normalize(hist, hist).flatten()

    def compute_features(self, image: np.ndarray) -> Tuple:
        """Detect keypoints and compute descriptors."""
        return self.orb.detectAndCompute(image, None)

    def compare_images(self, original_img: np.ndarray, returned_img: np.ndarray) -> Dict:
        """Compare two images and return similarity scores."""
        # Preprocess for SSIM and features
        original_pre = self.preprocess_image(original_img)
        returned_pre = self.preprocess_image(returned_img)

        # SSIM
        ssim_score = ssim(original_pre, returned_pre)

        # Histogram similarity
        hist_orig = self.compute_histogram(original_img)
        hist_ret = self.compute_histogram(returned_img)
        hist_score = cv2.compareHist(hist_orig, hist_ret, cv2.HISTCMP_CORREL)

        # Feature matching
        kp1, desc1 = self.compute_features(original_pre)
        kp2, desc2 = self.compute_features(returned_pre)
        if desc1 is not None and desc2 is not None and len(kp1) > 0 and len(kp2) > 0:
            matches = self.matcher.match(desc1, desc2)
            feature_score = len(matches) / max(len(kp1), len(kp2))
        else:
            feature_score = 0.0

        # Weighted overall similarity
        overall_score = (
            ssim_score * self.weights['ssim'] +
            hist_score * self.weights['hist'] +
            feature_score * self.weights['features']
        )

        return {
            'overall_similarity': round(overall_score, 3),
            'ssim_score': round(ssim_score, 3),
            'histogram_similarity': round(hist_score, 3),
            'feature_similarity': round(feature_score, 3),
            'is_suspicious': overall_score < self.similarity_threshold
        }

    def load_image(self, path: str) -> np.ndarray:
        """Load an image from file path."""
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Could not load image from: {path}")
        return image

    def load_image_from_bytes(self, image_bytes: bytes) -> np.ndarray:
        """Decode image from byte data (e.g., from API)."""
        np_data = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Could not decode image bytes")
        return image

# Example Usage
if __name__ == "__main__":
    inspector = VisualInspector()
    # original = inspector.load_image("original.jpg")
    # returned = inspector.load_image("returned.jpg")
    # result = inspector.compare_images(original, returned)
    # print(result)
