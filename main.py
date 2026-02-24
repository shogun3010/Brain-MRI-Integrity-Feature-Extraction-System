from function import *
import matplotlib.pyplot as plt


path = 'Image/kaggle_3m/TCGA_CS_4941_19960909/TCGA_CS_4941_19960909_3.tif' 
    
try:
    
    bgr, gray = load_and_preprocess(path)

    # วิเคราะห์ Wavelet และค่าทางสถิติ
    ll_comp, hh_comp, hh_energy, ratio = verify_integrity_with_stats(gray)
        
    # ปรับปรุงคุณภาพภาพทางการแพทย์
    refined = medical_refinement(gray)
        
    # วิเคราะห์พื้นที่เนื้องอก
    final_view, final_mask, area_sum = analyze_tumor(bgr, refined)

    # --- ส่วนการแสดงผล (Visual Report) ---
    plt.figure(figsize=(16, 9))

    # 1. ภาพต้นฉบับ
    plt.subplot(2, 3, 1)
    plt.imshow(gray, cmap='gray')
    plt.title(f"Original MRI\nEnergy Ratio: {ratio:.4f}%")
    plt.axis('off')

    # 2. Histogram ของ Wavelet Coefficients (HH)
    # ใช้ดูว่า Noise บานออกแค่ไหน
    plt.subplot(2, 3, 2)
    plt.hist(hh_comp.flatten(), bins=100, color='crimson', range=(-5, 5))
    plt.title("Wavelet HH Histogram\n(Sharpness = Low Noise)")
    plt.xlabel("Coeff Value")

    # 3. SimpleITK Refined (แก้แสง)
    plt.subplot(2, 3, 3)
    plt.imshow(refined, cmap='gray')
    plt.title("SimpleITK Refined\n(Bias Field Corrected)")
    plt.axis('off')

    # 4. Wavelet LL Component (ภาพโครงสร้างหลัก)
    plt.subplot(2, 3, 4)
    plt.imshow(ll_comp, cmap='gray')
    plt.title("DWT LL Component\n(Low-pass Filtering)")
    plt.axis('off')

    # 5. Final Result
    plt.subplot(2, 3, 5)
    plt.imshow(cv2.cvtColor(final_view, cv2.COLOR_BGR2RGB))
    plt.title(f"Final Detection\nTumor Area: {area_sum} px")
    plt.axis('off')

    plt.tight_layout()
    print(f"Energy Ratio (HH/LL): {ratio:.6f}%")
    print(f"Tumor Area: {area_sum} pixels")
    plt.show()

except Exception as e:
    
    print(f"เกิดข้อผิดพลาด: {e}")