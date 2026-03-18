# BRNA Galactic Command Portal

**ศูนย์ควบคุม Command Center สำหรับสถาปัตยกรรมเครือข่าย BRNA (Web Portal UI)**

โปรเจกต์นี้เป็นหน้าเว็บแอปพลิเคชัน (Dashboard) ที่ออกแบบมาด้วยสไตล์ Premium Glassmorphism เพื่อทำหน้าที่เป็น **ศูนย์สั่งการ (Command Center)** สำหรับพล็อตกราฟิก ติดตามสถานะ (Telemetry) และสั่งรันระบบจำลอง BRNA Core ผ่านหน้าเว็บแบบ Real-time

---

## 🌟 ฟีเจอร์หลัก (Key Features)

- **Interactive Topology Canvas**: แผนที่เครือข่าย BRNA แบบ Live 2D Canvas แสดงเส้นทางการเชื่อมต่อ คลื่นควอนตัม และโซนการทำงาน (Core, Bio, HITL, Entangle) อย่างชัดเจน
- **Live Data Flow Animation**: มองเห็นการเคลื่อนที่ของข้อมูล (Packet) และการทำ Entanglement Swapping ได้ทันทีที่สั่งรัน Test Case
- **Validation Subroutines (Test Runner)**: ผนวกการทดสอบทั้ง 10 รูปแบบจาก `mock_up.py` ให้สั่งงานง่ายๆ ด้วยปุ่มเดียว และมี Log แสดงผลแบบ Step-by-step
- **Sub-Quantum Telemetry Log**: ติดตาม Log ทั้งหมดจากเซิร์ฟเวอร์ เช่น เหตุกาณ์พายุ Decoherence หรือมนุษย์เข้าแทรกแซง
- **Architecture Wiki (`/architecture`)**: หน้าความรู้แบบครบวงจรอธิบายแนวคิด 5-Layer Stack, IP Plan และหลักการทำงานของเครือข่ายชีวภาพควอนตัม

---

## ⚙️ โครงสร้างเทคโนโลยี (Tech Stack)

*   **Frontend**: Next.js (App Router), React, TailwindCSS, Framer Motion, HTML5 Canvas, Lucide Icons
*   **Backend (API)**: FastAPI, Python `asyncio` สำหรับการจัดการ subprocess
*   **Integration**: รันคำสั่งเชื่อมต่อไปยัง BRNA Core Engine ในโฟลเดอร์ `/Github_artifact/pro10-brna-v2` แบบเบื้องหลัง

---

## 🚀 การติดตั้งและเปิดรันระบบ (How to run)

เนื่องจากระบบนี้ประกอบด้วย 2 ฝั่ง (Frontend และ Backend) จะต้องรันทั้งคู่ขนานกัน:

### 1. เปิด BRNA Backend API (FastAPI)
ตัว Backend ทำหน้าที่เชื่อมต่อกับ Python Core Engine และอ่านผลลัพธ์มาส่งให้เว็บ:
```bash
# เปิด Terminal ช่องแรก
cd /home/shachi/repos/network_project/brna-portal

# รันเซิร์ฟเวอร์ FastAPI บนเครื่อง
python main.py
```
*(Backend จะรันอยู่ที่พอร์ต `http://localhost:8000`)*

### 2. เปิด BRNA Frontend Portal (Next.js)
```bash
# เปิด Terminal ช่องที่สอง
cd /home/shachi/repos/network_project/brna-portal

# ติดตั้ง Dependencies ถ้ายังไม่ได้ทำ
npm install

# รันหน้าเว็บ
npm run dev
```
*(Frontend จะรันอยู่ที่พอร์ต `http://localhost:3000`)*

---

## 📂 ลำดับความสำคัญของไฟล์ (File Structure)

*   **`src/app/page.tsx`**: หน้า Command Dashboard หลัก (มีการดึงข้อมูลจาก FastAPI และการสลับหน้าต่าง Test Runner)
*   **`src/app/architecture/page.tsx`**: หน้า Document รวบรวมข้อมูลเชิงลึกของ BRNA 
*   **`src/components/TopologyCanvas.tsx`**: ไฟล์จัดการวาดกราฟิกแผนที่ 2D บน Canvas และควบคุม Animation ของเครือข่าย
*   **`src/components/Navbar.tsx`**: ส่วนของ Navigation นำทางด้านบน
*   **`main.py`**: API Backend (FastAPI) ที่รับ Request เพื่อสั่งให้ Environment Python ใน Core Engine ตื่นขึ้นมาทำงาน
