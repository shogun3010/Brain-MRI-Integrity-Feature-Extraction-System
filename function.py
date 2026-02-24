import cv2
import numpy as np
import pywt
import SimpleITK as sitk
import matplotlib.pyplot as plt

# 1. DATA LOADING & INITIALIZATION
def load_and_preprocess(path):
    
    img_bgr = cv2.imread(path)
    
    if img_bgr is None:
        
        raise ValueError("ไม่พบไฟล์ภาพ กรุณาตรวจสอบชื่อไฟล์")
    
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    return img_bgr, img_gray

# 2. INTEGRITY CHECK (PyWavelets) + HISTOGRAM ANALYSIS
def verify_integrity_with_stats(image):
    
    # ทำ DWT
    coeffs2 = pywt.dwt2(image, 'haar')
    LL, (LH, HL, HH) = coeffs2
    
    # คำนวณ Energy
    energy_hh = np.sum(np.square(HH))
    energy_ll = np.sum(np.square(LL))
    
    # คำนวณ Energy Ratio (เป็น % เพื่อให้เข้าใจง่าย)
    # ถ้าค่านี้สูง แสดงว่ามี Noise แทรกซ้อนในพิกเซลเยอะ
    energy_ratio = (energy_hh / energy_ll) * 100
    
    return LL, HH, energy_hh, energy_ratio

# 3. MEDICAL NORMALIZATION (SimpleITK)
def medical_refinement(image_np):
    
    sitk_img = sitk.GetImageFromArray(image_np.astype(np.float32))
    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    output_sitk = corrector.Execute(sitk_img)
    refined_img = sitk.GetArrayFromImage(output_sitk)
    
    return refined_img

# 4. SEGMENTATION (OpenCV)
def analyze_tumor(original_bgr, refined_gray):
    
    _, thresh = cv2.threshold(refined_gray.astype(np.uint8), 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result_img = original_bgr.copy()
    total_area = 0
    
    for cnt in contours:
        
        area = cv2.contourArea(cnt)
        
        if area > 50:
            
            total_area += area
            cv2.drawContours(result_img, [cnt], -1, (0, 255, 0), 2)
            
    return result_img, mask, total_area