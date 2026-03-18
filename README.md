# โครงการ BRNA (Bio-Resonance Network Architecture)

**Advanced Bio-Quantum Network Engineering & Living Infrastructure**

ยินดีต้อนรับสู่ Repository หลักของโครงการ **BRNA** ซึ่งเป็นโครงการวิจัยและพัฒนาสถาปัตยกรรมเครือข่ายแห่งอนาคต ที่เปลี่ยนผ่านจากระบบเครือข่ายที่ใช้ซิลิคอนและการส่งข้อมูลแบบดั้งเดิม (Classical Networking) ไปสู่ **เครือข่ายชีวภาพควอนตัม (Bio-Quantum Systems)** ที่ทำงานบนรากฐานของเซลล์สิ่งมีชีวิตและกลศาสตร์ควอนตัม เพื่อการส่งข้อมูลแบบ Zero-latency และการเก็บข้อมูลระดับ DNA ที่ยั่งยืน

---

## 📂 โครงสร้างของโปรเจกต์ (Repository Structure)

โปรเจกต์นี้ถูกแบ่งออกเป็น 2 ส่วนหลัก เพื่อแยกการจำลองผลตรรกะระดับลึก (Core Engine) และระบบจัดการภาพรวม (Command Portal) ออกจากกัน:

1. **[BRNA Core Engine (`/Github_artifact/pro10-brna-v2`)](./Github_artifact/pro10-brna-v2/README.md)**
   - ระบบ Core Simulator พัฒนาด้วย **Python**
   - จำลองการทำงานของ Neural Router, Mycelial Mesh, DNA Storage และ QSP Protocol
   - รวม Test Cases ทั้ง 10 รูปแบบ สำหรับการประเมินการออกแบบสถาปัตยกรรม

2. **[BRNA Galactic Command Portal (`/brna-portal`)](./brna-portal/README.md)**
   - หน้าเว็บบอร์ด (Dashboard) ถ่ายทอดสดสถานะเครือข่าย พัฒนาด้วย **Next.js** และ **FastAPI**
   - มี Topology Canvas สำหรับแสดงผลโหนดต่างๆ แบบ Real-time
   - มี "Test Runner" สั่งรันการทดสอบและดูการไหลของข้อมูล (Data Flow) ลงบนหน้าแผนที่เครือข่าย

---

## 🎯 องค์ประกอบหลัก (Core Themes)

*   🧠 **Neural Processing**: การใช้ท่อ Microtubule ในเซลล์เป็น "เร้าเตอร์มีชีวิต" (Living Routers) เคลื่อนย้ายข้อมูลด้วยหลักการ Orchestrated Objective Reduction (Orch OR)
*   🌱 **Biological Topology**: การกระจายเครือข่ายด้วยราเส้นใย (Mycelial Mesh) ที่สามารถซ่อมแซมตัวเองได้ (Self-healing) โอบล้อมระดับภูมิศาสตร์
*   🌌 **Quantum Synchronization**: โปรโตคอล QSP เชื่อมต่อเครือข่ายระหว่างดวงดาวผ่าน Entanglement Swapping หลุดพ้นจากข้อจำกัดด้านระยะทางและเวลา
*   🧬 **Massive Persistence**: การเปลี่ยนข้อมูลเป็นรหัสพันธุกรรม (DNA) เพื่อเก็บรักษาข้อมูลให้คงอยู่ได้เป็นพันๆ ปี

---

## 🚀 การเริ่มต้นใช้งาน (Quick Start)

เพื่อให้ระบบทำงานได้สมบูรณ์ กรุณาเปิดระบบทั้ง 2 ส่วนควบคู่กัน:

1. **รัน BRNA Portal Backend (FastAPI)**
   ```bash
   cd brna-portal
   # รัน Virtual Environment (ถ้ามี)
   python main.py
   ```
   *เซิร์ฟเวอร์จะรันที่ `http://localhost:8000`*

2. **รัน BRNA Portal Frontend (Next.js)**
   ```bash
   cd brna-portal
   npm install
   npm run dev
   ```
   *เปิดเบราว์เซอร์ดูผลลัพธ์ที่ `http://localhost:3000`*

ดูรายละเอียดวิธีการรันและการตั้งค่าเพิ่มเติมได้ใน README ของแต่ละส่วนประกอบ