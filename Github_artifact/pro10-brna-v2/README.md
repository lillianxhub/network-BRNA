# BRNA Core Engine (pro10-brna-v2)

**ระบบจำลองการทำงานหลักของ Bio-Resonance Network Architecture (Core Simulator)**

โฟลเดอร์นี้บรรจุตรรกะการทำงานทั้งหมดที่เกี่ยวข้องกับการจำลอง (Simulation) สถาปัตยกรรมเครือข่ายชีวภาพควอนตัม (Bio-Quantum Stack) เขียนด้วย **Python** ระบบนี้จะถูกเรียกใช้งานโดย BRNA Portal เพื่อประมวลผลเครือข่ายและจำลอง Test Cases ต่างๆ

---

## 🧩 โครงสร้าง 5-Layer Bio-Quantum Stack

ระบบ Engine ถูกแบ่งย่อยออกเป็นโมดูลตาม Layer ทั้ง 5 ชั้น ดังนี้:

- **L5: Galactic Application** (`dashboard.py` / `mock_up.py`) - ควบคุมแอปพลิเคชันและการสุ่มตัวอย่างข้อมูล
- **L4: Quantum-Digital Bridge** (`hitl_gateway.py` / `spin_bridge.py`) - แปลงสถานะควอนตัมสปินให้เป็นข้อมูล Digital และการตรวจสอบโดยมนุษย์ (HITL - Human in the Loop)
- **L3: Interstellar Routing** (`routing.py`) - คำนวณเส้นทางข้ามมิติด้วย Resonance Cost ผ่านโปรโตคอล BRR
- **L2: Mycelial Mesh** (`mycelial_mesh.py`) - สร้างการเชื่อมต่อระดับ Data Link ด้วยราเส้นใย (BLAP Protocol) ที่จำลองการซ่อมแซมเครือข่ายอัตโนมัติ
- **L1: Bio-Physical** (`microtubule.py`) - จำลองท่อเส้นใยระดับเซลล์ การทำงานของ Orch OR และระบบความร้อน (Metabolic Cooling)

---

## 🔬 Test Scenarios (10 Validation Subroutines)

ภายในไฟล์ `mock_up.py` บรรจุ **Test Case 10 สถานการณ์** เพื่อใช้ทดสอบความสามารถของเครือข่าย BRNA ได้แก่:

1. **Orch OR Coherence Test**: ทดสอบการรักษาความเสถียรควอนตัมใน Neural Repeater
2. **DNA Store Recovery**: ทดสอบบันทึก/กู้คืนข้อมูลชีวภาพเทียบกับการเกิด Error
3. **Entanglement Swapping**: ทดสอบการทำ Entanglement ระหว่างโหนดที่ไม่ได้ต่อกันโดยตรง
4. **HITL Override**: ทดสอบให้มนุษย์เข้ามาแทรกแซงแพ็กเก็ตที่มีความเสี่ยงเชิงจริยธรรม
5. **Mycelial Self-Healing**: ทดสอบลิงก์ขาดและให้ราเส้นใยงอกหาเส้นทางใหม่ (Rerouting) ภายใน <50ms
6. **QSP Handshake Test**: ทดสอบการจับมือกันด้วยการซิงค์คลื่น (Phase Sync)
7. **Paradox Prevention (PPP)**: ทดสอบกรองแพ็กเก็ตที่ขัดแย้งกับหลักความเป็นเหตุเป็นผล (Causality) ของกาลเวลา
8. **Metabolic Cooling Mode**: ทดสอบการรักษาความเย็นของระบบชีวภาพไม่ให้ Coherence ตก
9. **Galactic Routing (Zero-Latency)**: จำลองการวิ่งของพัลส์ข้อมูลไปดาว Proxima Centauri โดยเทเลพอร์ตเชิงควอนตัม
10. **Resonance Cost Routing**: ทดสอบอัลกอริทึม Modified Dijkstra ผ่าน C_R metric

---

## 🛠️ วิธีการติดตั้งและการใช้งาน (Setup & Run)

**สิ่งที่ต้องมี (Prerequisites):**

- Python 3.10+
- `pip install -r requirements.txt` (รวม NetworkX และ ไลบรารีประมวลผลอื่นๆ)

**การรัน Test Cases ทั่วไป:**
หากต้องการรันการจำลองสถานการณ์ทั้งหมดผ่าน Terminal ธรรมดา (Interactive TUI):

```bash
# รันไฟล์ mock up menu
python mock_up.py
```

_(กรณีที่นำไปผูกกับ Web Portal, ไฟล์นี้และ `run_simulation.py` จะถูก Trigger ผ่าน API บน `main.py` อัตโนมัติ)_

**การรัน Unit Tests:**

```bash
# ตรวจสอบความถูกต้องของโมดูลทั้งหมด
python -m pytest tests/
```
