# Vision-Impaired Shopping Assistant 🛒👁️

> An affordable, open-source assistive technology device that empowers vision-impaired individuals to shop independently with confidence.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red.svg)
![Status](https://img.shields.io/badge/status-Prototype-orange.svg)

## 📋 Overview

The Vision-Impaired Shopping Assistant is a Raspberry Pi-based assistive device designed to help vision-impaired individuals navigate grocery shopping independently. Created as part of my senior year Engineering Design and Development (PLTW) course, this project addresses a critical accessibility gap in retail environments.

**Project Constraints:**

-   **Budget:** $75 total
-   **Timeline:** One academic year
-   **Goal:** Create a working prototype that demonstrates real-world viability

## 🎯 Problem Statement

Vision-impaired individuals face significant challenges when shopping independently:

-   **Product Identification:** Difficulty distinguishing between similar products
-   **Label Reading:** Unable to read nutritional information, prices, or expiration dates
-   **Allergen Detection:** Critical safety concerns with identifying allergen information
-   **Shopping Confidence:** Many avoid independent shopping due to these barriers

## ✨ Features

### Core Functionality

#### 🔍 **Real-Time OCR Text Detection**

-   Continuous text recognition from product labels using Tesseract OCR
-   Confidence-based filtering to reduce false positives
-   Automatic text-to-speech announcement of detected text
-   Optimized image preprocessing for improved accuracy

#### 📊 **Barcode Scanning System**

-   Hardware barcode scanner integration for instant product identification
-   Database lookup for product information including:
    -   Product name and brand
    -   Allergen information
    -   Custom product notes
-   Audio feedback for both known and unknown products

#### 🔊 **Intelligent Text-to-Speech**

-   Configurable speech rate (100-500 WPM)
-   Non-blocking audio synthesis to maintain system responsiveness
-   Customizable announcement templates
-   Smart text change detection to prevent repetitive announcements

#### 🌐 **Web-Based Configuration Interface**

-   Responsive web UI built with Svelte and TypeScript
-   Real-time configuration updates without system restart
-   Barcode database management (add, view, delete entries)
-   Network-agnostic design (works on localhost, LAN, or hotspot)

### Technical Features

#### 🎛️ **Configurable Image Processing**

-   Adjustable thresholding for different lighting conditions
-   Real-time grayscale conversion and normalization
-   Debug mode with visual pipeline inspection

#### 🗄️ **Robust Database System**

-   SQLite database for offline operation
-   SQLAlchemy ORM for maintainable code
-   Comprehensive error handling and data validation

#### 🔧 **Developer-Friendly Architecture**

-   Modular design with clear separation of concerns
-   Comprehensive documentation and type hints
-   RESTful API for external integrations
-   Thread-safe operations for concurrent processing

## 🚀 Getting Started

### Prerequisites

-   Raspberry Pi 4B or newer
-   USB Camera or Raspberry Pi Camera Module
-   USB Barcode Scanner (HID-compliant)
-   Speaker or headphones for audio output
-   Python 3.8 or higher

### Hardware Setup

1. **Connect the camera** to the Raspberry Pi (USB or CSI port)
2. **Plug in the barcode scanner** to any USB port
3. **Connect audio output** (3.5mm jack or HDMI)
4. **Mount in 3D printed enclosure** (STL files available upon request)

### Software Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/vision-shopping-assistant.git
cd vision-shopping-assistant
```

2. **Install system dependencies:**

```bash
sudo apt-get update
sudo apt-get install -y \
    tesseract-ocr \
    python3-opencv \
    espeak \
    sqlite3
```

3. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

4. **Install web interface dependencies:**

```bash
cd client
npm install
npm run build
cd ..
```

5. **Run the application:**

```bash
python main.py
```

6. **Access the web interface:**
    - Open a browser and navigate to `http://<raspberry-pi-ip>:5173`

## 📖 Usage

### Basic Operation

1. **Start the device** - The system automatically initializes all components
2. **Point camera at products** - OCR will read visible text automatically
3. **Scan barcodes** - Use the barcode scanner for instant product identification
4. **Listen to audio feedback** - The device announces all detected information

### Web Configuration

Access the web interface to:

-   **Adjust TTS speed** to match your preference
-   **Configure image processing** for your lighting conditions
-   **Manage barcode database** - Add products you frequently purchase
-   **Customize announcement templates** for personalized feedback

### Debug Mode

Enable debug mode to see the image processing pipeline:

```python
# In main.py, uncomment:
Config.enable_debug()
```

## 🔌 API Documentation

### Configuration Endpoints

**GET /api/settings**

-   Retrieve current configuration settings

**POST /api/settings**

-   Update configuration settings
-   Body: JSON object with setting key-value pairs

### Barcode Management Endpoints

**GET /api/barcodes**

-   Get all barcode entries

**POST /api/barcodes**

-   Add new barcode entry
-   Required fields: `barcode`, `product_name`, `brand`
-   Optional: `allergies`

**DELETE /api/barcodes/:barcode**

-   Delete a barcode entry

## 🛠️ Development

### Project Structure

```
vision-shopping-assistant/
├── src/
│   ├── barcode/          # Barcode scanning logic
│   ├── camera/           # Camera management
│   ├── db/               # Database models and operations
│   ├── image_processing/ # Image preprocessing pipeline
│   ├── ocr/              # Text detection and OCR
│   ├── speech/           # Text-to-speech engine
│   ├── visualization/    # Debug display utilities
│   └── web/              # REST API server
├── client/               # Svelte web interface
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/  # UI components
│   │   │   └── stores/      # State management
│   │   └── App.svelte       # Main application
├── main.py               # Application entry point
└── requirements.txt      # Python dependencies
```

### Key Design Decisions

1. **Threaded Architecture**: Barcode scanning runs in a separate thread to prevent blocking the OCR pipeline
2. **Modular Design**: Each component is independently testable and maintainable
3. **Configuration Management**: Centralized configuration allows runtime adjustments without code changes
4. **Error Recovery**: Comprehensive error handling ensures the device continues operating even with component failures

## 📊 Performance

-   **OCR Processing**: ~200ms per frame on Raspberry Pi 4
-   **Barcode Recognition**: Instant (<50ms)
-   **TTS Latency**: <100ms from detection to speech
-   **Power Consumption**: ~5W during operation

## 🎓 Educational Impact

This project was developed as part of the Project Lead The Way (PLTW) Engineering Design and Development course. Key learning outcomes included:

-   **Engineering Design Process**: Problem identification through solution validation
-   **Budget Management**: Delivered working prototype within $75 constraint
-   **User-Centered Design**: Extensive research on vision impairment challenges
-   **Systems Integration**: Combined hardware, software, and user interface design
-   **Documentation**: Technical writing and presentation skills

<!-- ## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

-   Bug fixes
-   Feature enhancements
-   Documentation improvements
-   Hardware compatibility updates -->

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

---

_"Technology should empower everyone, regardless of ability. This project is my contribution to making shopping accessible for all."_
