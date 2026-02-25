# Brain-MRI-Integrity-Feature-Extraction-System
ระบบวิเคราะห์และตรวจสอบความสมบูรณ์ของภาพถ่าย MRI สมอง (Brain MRI Integrity &amp; Feature Extraction System)

Image from Kaggle: URL 'https://www.kaggle.com/code/mahmoudlimam/brain-mri-segmentation'

ระบบวิเคราะห์และตรวจสอบความสมบูรณ์ของภาพถ่าย MRI สมอง (Brain MRI Integrity \& Feature Extraction System)



1\. การตรวจสอบและกรองสัญญาณด้วยความถี่ (Frequency Analysis)



* Library: PyWavelets (ใช้ฟังก์ชัน pywt.dwt2)
* Method: Discrete Wavelet Transform (DWT) โดยใช้ Wavelet ชนิด 'Haar' หรือ 'Biorthogonal'
* รายละเอียดทางเทคนิค: คำสั่ง dwt2 จะแยกภาพออกเป็น 4 ส่วน: LL (Approximation), LH (Horizontal), HL (Vertical), และ HH (Diagonal)
* ทำเพื่ออะไร: เราใช้ส่วน HH เพื่อวิเคราะห์ Noise พลังงานสูง หากมีการตัดต่อภาพ รอยต่อของพิกเซลที่ถูกฝังเข้าไปใหม่จะสร้างค่าสัมประสิทธิ์ในย่าน HH ให้สูงกว่าปกติอย่างมีนัยสำคัญ



2\. การปรับแก้ความไม่สม่ำเสมอของความเข้มแสง (Intensity Correction)



* Library: SimpleITK (ใช้คลาส sitk.N4BiasFieldCorrectionImageFilter)
* Method: N4 Bias Field Correction
* รายละเอียดทางเทคนิค: เครื่อง MRI มักมีปัญหา "Bias Field" หรือความสว่างที่ไม่เท่ากันทั่วทั้งภาพ (สว่างกลาง มืดขอบ) คำสั่งนี้จะทำการประมาณค่าความผิดเพี้ยนของแสงและลบออก (Correct) จากภาพเดิม
* ทำเพื่ออะไร: เพื่อให้พิกเซลของเนื้อสมองชนิดเดียวกันมีค่าความสว่าง (Intensity) เท่ากันทั้งภาพ ช่วยให้การกำหนดค่า Threshold ในขั้นตอนถัดไปแม่นยำ ไม่เกิดการ "หลุด" หรือ "เกิน" ของพื้นที่เนื้องอก



3\. การจำแนกส่วนภาพเชิงสถิติ (Image Segmentation)



* Library: OpenCV (ใช้ฟังก์ชัน cv2.threshold คู่กับ cv2.THRESH\_OTSU)
* Method: Otsu’s Global Thresholding
* รายละเอียดทางเทคนิค: อัลกอริทึมของ Otsu จะคำนวณหาค่า Threshold ที่เหมาะสมที่สุดโดยอัตโนมัติจากการวิเคราะห์ Histogram ของภาพ เพื่อแยก Foreground (เนื้องอก) ออกจาก Background (เนื้อเยื่อปกติ)
* ทำเพื่ออะไร: เพื่อสร้าง Binary Mask (ภาพขาว-ดำ) ที่ระบุตำแหน่งของเซลล์ที่มีความหนาแน่นผิดปกติได้อย่างรวดเร็ว



4\. การจัดการรูปร่างและการวัดผล (Morphology \& Measurement)



* Library: OpenCV (ใช้ฟังก์ชัน cv2.morphologyEx และ cv2.findContours)
* Method: Morphological Opening \& Contour Analysis
* รายละเอียดทางเทคนิค: ใช้ Opening (Erosion ตามด้วย Dilation) เพื่อกำจัดจุดขาวเล็กๆ (Salt noise) ที่หลุดออกมา และใช้ findContours เพื่อคำนวณหาพื้นที่พิกเซล (Area)
* ทำเพื่ออะไร: เพื่อให้ได้ขอบเขตเนื้องอกที่ "สะอาด" และสามารถระบุขนาดพื้นที่ (Quantitative Data) เพื่อใช้เปรียบเทียบในเชิงวิจัยได้



#### การตีความผลลัพธ์จากสี (Color Interpretation)



ในหน้าต่าง Final Result เราใช้เทคนิค Alpha Blending และ Overlay เพื่อช่วยในการวินิจฉัย:



* เส้นขอบสีเขียว (Green) : พื้นที่ตรวจพบ (Detected Zone): คือขอบเขตที่อัลกอริทึมยืนยันว่าเป็นพยาธิสภาพที่ต้องติดตาม
* สีแดง (Red Overlay) :  จุดวิกฤต (Critical Spots): แสดงบริเวณที่มีความหนาแน่นของเนื้องอกสูงสุด (Hotspot)
* สีน้ำเงิน/ม่วง (Blue/Purple) : โครงสร้างสมอง (Brain Structure): ช่วยให้แพทย์มองเห็นขอบเขตของเนื้อสมองปกติเพื่อเปรียบเทียบตำแหน่งกับเนื้องอก
* พื้นที่สีดำ (Black) : พื้นที่ว่าง (Empty Space): ส่วนที่ระบบกรองออกเพื่อให้แพทย์โฟกัสเฉพาะจุดที่สำคัญ



#### บทสรุปผลลัพธ์เชิงตัวเลข (Metric Results)



* Energy Ratio: บ่งบอกว่า "ภาพนี้สะอาดแค่ไหน" (ถ้า < 0.01% ถือว่ายอดเยี่ยม)
* HH Histogram: กราฟที่แคบและแหลมบ่งบอกว่า "ภาพนี้ไม่ได้ถูกดัดแปลง" (Integrity Verified)
* Tumor Area: บอกขนาดพื้นที่รอยโรคเป็นจำนวนพิกเซล เพื่อใช้ประเมินว่าการรักษาก่อนหน้าได้ผลหรือไม่ (เนื้องอกยุบหรือโตขึ้น)
