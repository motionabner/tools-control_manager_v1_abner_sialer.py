# 🛠️ CONTROL MANAGER V1 - ABNER SIALER

A lightweight custom control creation tool for Autodesk Maya, designed to streamline the rigging process by automating the generation of clean, animator-friendly controllers.

---

## ✨ Features

- 💡 **Custom control shapes**: circle, square, arrow, cross, star
- 🎯 **World-space alignment** to any selected joint or object
- 🎨 **Color selector by name** (no more color indexes)
- 🧱 **Auto hierarchy**: control → OFFSET → GRP
- 🧩 **Multi-control creation**: one controller per selected object
- 📋 **Add custom attributes** directly to each controller
- ✅ Clean transforms, ready for constraints or animation

---

## 📷 UI Preview

<img src="https://your-screenshot-link.com" alt="UI Screenshot" width="500" />

---

## 🚀 Installation

1. Download the script file:
   [`control_manager_v1_abner_sialer.py`](./control_manager_v1_abner_sialer.py)

2. Place it in your Maya scripts folder or custom tools directory.

3. In Maya's Script Editor (Python tab):

```python
import control_manager_v1_abner_sialer as cm
cm.show_control_manager_ui()
