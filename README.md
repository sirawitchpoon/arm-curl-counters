# AI-powered Arm Curl Counters

ระบบนับการยกน้ำหนักแขนอัจฉริยะด้วย Computer Vision

## รายละเอียดโปรเจค

โปรเจคนี้เป็นแอปพลิเคชันเว็บที่ใช้ Computer Vision เพื่อตรวจจับและนับจำนวนครั้งในการยกน้ำหนักแขน (Arm Curls) แบบอัตโนมัติ โดยใช้กล้องเว็บแคม แอปพลิเคชันนี้สามารถ:

- นับจำนวนครั้งในการยกน้ำหนักแขนทั้งซ้ายและขวา
- คำนวณแคลอรี่ที่เผาผลาญ
- ตั้งเป้าหมายจำนวนครั้งและติดตามความคืบหน้า
- แสดงผลแบบเรียลไทม์ผ่านวิดีโอสตรีม

## โครงสร้าง Directory

```
arm-curl-counters/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    └── images/
        ├── left_cheer.gif
        └── right_cheer.gif
```

## การติดตั้ง

### ขั้นตอนที่ 1: ติดตั้ง Python

1. ไปที่ [Python.org](https://www.python.org/downloads/)
2. ดาวน์โหลดและติดตั้ง Python เวอร์ชันล่าสุด (3.8 หรือใหม่กว่า)
3. ในระหว่างการติดตั้ง ให้เลือก "Add Python to PATH"

### ขั้นตอนที่ 2: โคลนโปรเจค

```
git clone https://github.com/your-username/arm-curl-counters.git
cd arm-curl-counters
```

### สร้าง Virtual Environment (Optional)

```
python -m venv venv
```

เปิดใช้งาน virtual environment:

- บน Windows:
  ```
  venv\Scripts\activate
  ```
- บน macOS และ Linux:
  ```
  source venv/bin/activate
  ```

### ขั้นตอนที่ 3: ติดตั้ง Dependencies

ติดตั้งไลบรารีที่จำเป็นทั้งหมดโดยใช้คำสั่ง:

```
pip install flask opencv-python-headless mediapipe numpy
```

## การใช้งาน

1. รันแอปพลิเคชัน:
   ```
   python app.py
   ```

2. เปิดเว็บเบราว์เซอร์และไปที่ `http://localhost:5000`

3. อนุญาตให้เว็บไซต์เข้าถึงกล้องเว็บแคมของคุณ

4. เริ่มยกน้ำหนักแขน! แอปพลิเคชันจะนับจำนวนครั้งและคำนวณแคลอรี่ที่เผาผลาญโดยอัตโนมัติ

5. ใช้ปุ่ม "Reset" เพื่อเริ่มนับใหม่ และใช้ช่อง "Set target" เพื่อกำหนดเป้าหมายจำนวนครั้ง

## เทคโนโลยีที่ใช้

- Python
- Flask
- OpenCV
- MediaPipe
- HTML/CSS/JavaScript

## Development Log
For a detailed log of the development process and decisions made during this project, please see my [Project Development Log](development_history/development_log.md).

## วิชาที่เรียน

Semester1/2024 Khonkaen University Computer Engineering, Mini Project for Class: EN813709 Augmented Intelligence 

## Demo Presentation

https://youtu.be/uvPypWTl8aI

## ผู้พัฒนา

Sirawitch Butryojantho - Thailand - Khonkaen University 58 - Computer Engineering 31

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
