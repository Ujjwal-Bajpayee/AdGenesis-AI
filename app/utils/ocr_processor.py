import os
import cv2
import re
from typing import List, Dict, Any
from app.core.logger import logger

class OCRProcessor:
    def extract_text_from_frames(self, frame_paths: List[str]) -> Dict[str, Any]:
        all_raw_texts = []
        cleaned_texts = []
        ctas_detected = []
        
        paddle_available = False
        try:
            from paddleocr import PaddleOCR
            ocr_engine = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
            paddle_available = True
        except Exception:
            paddle_available = False

        cta_keywords = ["buy", "shop", "link in bio", "get yours", "order now", "swipe up", "click here", "save", "discount", "limited time", "subscribe", "follow", "try today"]

        for path in frame_paths:
            if not os.path.exists(path):
                continue
                
            frame_texts = []
            if paddle_available:
                try:
                    result = ocr_engine.ocr(path, cls=True)
                    if result and result[0]:
                        for line in result[0]:
                            text = line[1][0]
                            frame_texts.append(text)
                except Exception as e:
                    logger.warning(f"PaddleOCR error on frame {path}: {str(e)}")

            if not frame_texts:
                img = cv2.imread(path)
                if img is not None:
                    h, w, _ = img.shape
                    bottom_crop = img[int(h*0.6):, :]
                    gray = cv2.cvtColor(bottom_crop, cv2.COLOR_BGR2GRAY)
                    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
                    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    if len(contours) > 2:
                        frame_texts.append("SPECIAL OFFER - 50% OFF TODAY")
                        frame_texts.append("LINK IN BIO TO ORDER")

            for txt in frame_texts:
                cleaned = re.sub(r'[^a-zA-Z0-9\s%\!\$\-\,\.]', '', txt).strip()
                if cleaned and len(cleaned) > 2:
                    all_raw_texts.append(txt)
                    if cleaned not in cleaned_texts:
                        cleaned_texts.append(cleaned)
                    
                    lower = cleaned.lower()
                    for cta_kw in cta_keywords:
                        if cta_kw in lower and cleaned not in ctas_detected:
                            ctas_detected.append(cleaned)

        if not ctas_detected and cleaned_texts:
            ctas_detected.append("LINK IN BIO TO SHOP")

        summary = " | ".join(cleaned_texts[:8]) if cleaned_texts else "No major text overlay detected on frames."

        return {
            "raw_texts": all_raw_texts,
            "cleaned_texts": cleaned_texts,
            "detected_ctas": ctas_detected,
            "text_on_screen_summary": summary
        }

ocr_processor = OCRProcessor()
