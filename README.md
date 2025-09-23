# 🤖 SeydappAI ModelTrainer (v2.1.0)

**StarCoder2 Conversation Training Toolkit** - RTX 3060 için optimize edilmiş AI model eğitim platformu

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Flet](https://img.shields.io/badge/Flet-0.28.3%2B-purple.svg)](https://flet.dev)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org)
[![Transformers](https://img.shields.io/badge/Transformers-4.35%2B-orange.svg)](https://huggingface.co/transformers)

## 📋 İçindekiler

- [🎯 Proje Hakkında](#-proje-hakkında)
- [✨ Özellikler](#-özellikler)
- [🏗️ Mimari](#️-mimari)
- [⚙️ Kurulum](#️-kurulum)
- [🚀 Kullanım](#-kullanım)
- [📊 RTX 3060 Optimizasyonları](#-rtx-3060-optimizasyonları)
- [🧪 Test](#-test)
- [📁 Proje Yapısı](#-proje-yapısı)
- [🔧 Konfigürasyon](#-konfigürasyon)
- [🤝 Katkıda Bulunma](#-katkıda-bulunma)
- [📄 Lisans](#-lisans)

## 🎯 Proje Hakkında

SeydappAI ModelTrainer, **StarCoder2** modellerini konuşma verileri ile fine-tune etmek için geliştirilmiş modern bir eğitim platformudur. RTX 3060 12GB gibi orta seviye GPU'lar için özel olarak optimize edilmiştir.

### 🎪 Ana Hedefler

- **🎯 Kolay Kullanım**: Modern Flet UI ile kullanıcı dostu arayüz
- **⚡ Performans**: RTX 3060 için memory-aware optimizasyonlar
- **🔄 Otomasyon**: Autonomous training ve intelligent web scraping
- **📊 İzleme**: Real-time progress monitoring ve sistem kaynak takibi
- **🧠 Akıllı Öğrenme**: RAG (Retrieval-Augmented Generation) entegrasyonu

## ✨ Özellikler

### 🎨 Modern UI/UX
- **Ultra-Modern Interface**: Flet tabanlı responsive tasarım
- **Real-time Dashboard**: Canlı eğitim metrikleri ve sistem durumu
- **🎯 Training Configuration Panel**: Gelişmiş model ve profil seçimi
  - **🤖 Model Selector**: 5 farklı model seçeneği (dropdown)
  - **⚙️ Profile Selector**: 3 training profili (dinamik açıklama)
  - **🚀 Start Training**: Büyük gradient buton (glow efekti)
- **💬 AI Chat Interface**: Akıllı programlama asistanı
  - **🧠 Self-Learning AI**: Her etkileşimde kendini geliştiren yapay zeka
  - **🔍 Programming Question Detection**: Android, Python, JavaScript, Flask, React soruları otomatik tespit
  - **🌐 Web Search Integration**: Bilgi yoksa internetten araştırma
  - **📚 Knowledge Learning**: Yeni bilgileri otomatik öğrenme ve saklama
  - **🎓 Learning Dashboard**: Öğrenme istatistikleri ve bilgi yönetimi
  - **🔧 Backend Framework Support**: Flask, Django, Express.js için özel çözümler
  - **⚡ Frontend Framework Support**: React, Vue, Angular için kapsamlı rehberler
  - **📝 Code Examples**: Detaylı kod örnekleri ve açıklamalar
  - **🧵 Thread-Safe Processing**: UI donmadan arka plan işlemi
- **📊 Multi-View System**: Dashboard, Training, Models, Analytics, Logs, Settings
- **Progress Monitoring**: Memory-aware ilerleme takibi
- **Dark Theme**: Göz dostu karanlık tema
- **Factory Pattern**: Modüler UI component sistemi

### 🚀 Eğitim Özellikleri
- **LoRA Fine-tuning**: Parameter-efficient training
- **4-bit Quantization**: BitsAndBytes ile memory optimization
- **Gradient Checkpointing**: Memory usage reduction
- **Autonomous Training**: Otomatik konu seçimi ve eğitim
- **Micro Training**: 5 dakikalık hızlı test eğitimleri

### 🧠 Akıllı Sistemler
- **🤖 Self-Learning AI Chat Assistant**: Kendini geliştiren programlama asistanı
  - **🧠 Continuous Learning**: Her soru-cevap etkileşiminde öğrenme
  - **📚 Knowledge Base**: Öğrenilen bilgileri kalıcı saklama
  - **🎯 Smart Categorization**: Soruları otomatik kategorize etme
  - **⭐ Quality Assessment**: Cevap kalitesini 0-10 arası puanlama
  - **📊 Usage Statistics**: Hangi bilgilerin ne kadar kullanıldığını takip
  - **Android ListView**: XML layout + Java kod örnekleri
  - **Python Programming**: List comprehension, loops, functions
  - **JavaScript**: Async/await, DOM manipulation, array methods
- **Web Scraping**: Intelligent content extraction
- **Knowledge Graph**: Bilgi ağı oluşturma ve yönetimi
- **RAG Integration**: Retrieval-Augmented Generation
- **Context Building**: Akıllı bağlam oluşturma
- **Real-time Web Search**: Programming questions için canlı arama

### 🔧 RTX 3060 Optimizasyonları
- **Memory Management**: Akıllı bellek yönetimi
- **SWAP Monitoring**: Swap kullanım takibi ve temizleme
- **GPU Cleanup**: Otomatik GPU bellek temizleme
- **Adaptive Batch Sizing**: Dinamik batch boyutu ayarlama

## 🆕 Yeni Özellikler (v1.3)

### 🧠 Self-Learning AI System (YENİ!)
- **🎓 Continuous Learning**: AI her etkileşimde kendini geliştiriyor
- **📚 Knowledge Database**: SQLite tabanlı bilgi saklama sistemi
- **🎯 Smart Categorization**: Soruları otomatik kategorize etme (android, python, web, vb.)
- **⭐ Quality Assessment**: Cevap kalitesini akıllı algoritma ile puanlama
- **📊 Learning Dashboard**: Detaylı öğrenme istatistikleri ve yönetim paneli
- **🧹 Knowledge Cleanup**: Eski/gereksiz bilgileri otomatik temizleme
- **🔄 Usage Tracking**: Hangi bilgilerin ne kadar kullanıldığını takip

### 💬 AI Chat Interface (Yeni Güncellemeler!)
- **🤖 Akıllı Programlama Asistanı**: Android, Python, JavaScript, Flask, React soruları için özel asistan
- **🧠 Self-Learning System**: Her etkileşimde kendini geliştiren yapay zeka
- **🔍 Enhanced Question Detection**: 
  - **Backend Frameworks**: Flask, Django, Express.js otomatik tespit
  - **Frontend Frameworks**: React, Vue, Angular özel çözümler
  - **Mobile Development**: Android, Flutter, iOS desteği
  - **Database Systems**: SQL, MongoDB, PostgreSQL rehberleri
- **🌐 Web Search + Learning**: RAG bilgisi yoksa internetten arar ve öğrenir
- **📚 Knowledge Management**: 
  - Öğrenilen bilgileri kategorize etme
  - Kalite değerlendirmesi (0-10 puan)
  - Kullanım istatistikleri takibi
- **🔧 Project-Specific Solutions**:
  - **Flask Blog**: Kapsamlı blog uygulaması (11,638 karakter)
  - **React E-commerce**: Tam e-ticaret çözümü
  - **Android Apps**: ListView, RecyclerView örnekleri
- **📝 Detailed Code Examples**: XML layout, Java kod, Python, HTML, CSS örnekleri
- **🧵 Thread-Safe Processing**: UI donmadan arka plan işlemi
- **💬 Chat UI**: Modern chat arayüzü, typing indicator, message bubbles

### 📊 Enhanced View System
- **🎯 Analytics View**: Eğitim analitikleri ve performans metrikleri
- **🤖 Models View**: Model yönetimi ve karşılaştırma
- **🎓 Training View**: Detaylı eğitim konfigürasyonu
- **📝 Logs View**: Gelişmiş log filtreleme ve arama
- **⚙️ Settings View**: Kapsamlı ayarlar paneli

### 🎯 Gelişmiş Training Configuration Panel
- **🤖 Model Selector**: 5 farklı model seçeneği ile dropdown menü
- **⚙️ Profile Selector**: 3 training profili + dinamik açıklama sistemi
- **🚀 Start Training Button**: Büyük gradient buton + glow efekti
- **🏗️ Factory Pattern**: Modüler UI component architecture
- **🎮 Event Handler System**: Gelişmiş event management
- **📊 Real-time Feedback**: Seçim değişikliklerinde anlık güncelleme

### 🎨 UI/UX İyileştirmeleri
- **Organize Layout**: Training Configuration ve Advanced Features ayrımı
- **Visual Feedback**: Renk kodlaması ve icon sistemi
- **Double-click Protection**: Hızlı tıklamalara karşı koruma
- **Status Integration**: Seçimler status bar'da görüntülenir
- **Log Integration**: Tüm seçimler log sistemine kaydedilir

## 🏗️ Mimari

```
SeydappAI ModelTrainer
├── 🎨 UI Layer (Flet)
│   ├── Ultra-Modern Interface
│   ├── Responsive Components
│   └── Real-time Monitoring
├── 🧠 Core Engine
│   ├── Training Coordinator
│   ├── Model Loader
│   └── Memory Manager
├── 🔍 Research Module
│   ├── Web Scraper
│   ├── Content Filter
│   └── Knowledge Extractor
├── 📊 Data Pipeline
│   ├── Dataset Manager
│   ├── Preprocessor
│   └── Validator
└── 🎯 Training Engine
    ├── StarCoder2 Trainer
    ├── LoRA Configuration
    └── RTX 3060 Optimizer
```

## ⚙️ Kurulum

### 📋 Sistem Gereksinimleri

- **Python**: 3.8+ (3.9+ önerilir)
- **GPU**: NVIDIA RTX 3060 12GB (veya benzer)
- **RAM**: 16GB+ (32GB önerilir)
- **Disk**: 50GB+ boş alan
- **OS**: Linux/Windows/macOS

### 🔧 Kurulum Adımları

1. **Repository'yi klonlayın**:
```bash
git clone https://github.com/your-username/SeydappAI_ModelTrainer.git
cd SeydappAI_ModelTrainer
```

2. **Virtual environment oluşturun**:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# veya .venv\Scripts\activate  # Windows
```

3. **Dependencies'leri kurun**:
```bash
pip install -r requirements.txt
```

4. **Development dependencies (opsiyonel)**:
```bash
pip install -e ".[dev]"
```

5. **GPU dependencies (opsiyonel)**:
```bash
pip install -e ".[gpu]"
```

## 🆕 Son Güncellemeler (v2.1.0)

### 🔧 Flask Blog Sorunu Çözüldü!
- **✅ Import Hatası Düzeltildi**: `RAGRetriever` import sorunu çözüldü
- **✅ Backend Framework Detection**: Flask, Django projelerinin doğru tespiti
- **✅ Self-Learning System İyileştirildi**: Eksik alanlar için güvenli erişim
- **✅ Knowledge Management**: Öğrenilen bilgilerde hata kontrolü

### 🎯 AI Chat Geliştirmeleri
- **🔍 Enhanced Question Detection**: Backend/Frontend framework'leri ayrı tespit
- **📚 Knowledge Quality Scoring**: 0-10 arası kalite puanlama sistemi
- **🔧 Project-Specific Solutions**: Flask blog, React e-ticaret özel çözümleri
- **📊 Learning Statistics**: Detaylı öğrenme istatistikleri ve kullanım takibi

### 🛠️ Teknik İyileştirmeler
- **Thread-Safe Processing**: Güvenli arka plan işleme
- **Error Handling**: Gelişmiş hata yönetimi
- **Memory Management**: Daha verimli bellek kullanımı
- **Code Quality**: Defensive programming yaklaşımı

## 🚀 Kullanım

### 🎯 Temel Kullanım

```bash
# Ana uygulamayı çalıştır
python main.py

# Debug mode ile çalıştır
python main.py --debug

# Sadece UI test
python main.py --test-ui

# Sistem kontrolü
python main.py --check-system
```

**🎯 Yeni Training Configuration Panel:**

1. **🤖 Model Seçimi**:
   - Dropdown menüden model seçin
   - 5 farklı seçenek: StarCoder2-3b/7b, CodeBERT, CodeBERTa
   - Varsayılan: `bigcode/starcoder2-3b` (RTX 3060 için optimize)

2. **⚙️ Profil Seçimi**:
   - Training profili seçin
   - `micro_test`: 5 dakikalık hızlı test
   - `rtx3060_optimized`: RTX 3060 için optimize (varsayılan)
   - `production`: Tam kapsamlı training
   - Dinamik açıklama: Profil seçildiğinde açıklama güncellenir

3. **🚀 Training Başlatma**:
   - Büyük turuncu "Start Training" butonuna tıklayın
   - Seçilen model ve profil otomatik uygulanır
   - Real-time monitoring başlar

**Arayüz Özellikleri:**
- 🎛️ **Control Panel**: Gelişmiş model/profil seçimi + eğitim kontrolü
- 📊 **Dashboard**: Real-time sistem durumu ve training metrikleri
- 🧠 **AI Chat**: Self-Learning programlama asistanı (YENİ!)
  - **🎓 Learning Dashboard**: Öğrenme istatistikleri ve bilgi yönetimi
  - **📚 Knowledge Base**: SQLite tabanlı bilgi saklama
  - **🔄 Continuous Learning**: Her etkileşimde kendini geliştirme
- 🎓 **Training**: Detaylı eğitim konfigürasyonu
- 🤖 **Models**: Model yönetimi ve karşılaştırma
- 🎯 **Analytics**: Eğitim analitikleri ve performans metrikleri
- 📝 **Logs**: Gelişmiş log filtreleme ve arama
- ⚙️ **Settings**: Kapsamlı konfigürasyon ayarları

### 🎪 Komut Satırı Aracı

```bash
# Package kurulumu sonrası
seydappai-trainer

# Veya direkt çalıştırma
python -m src.ui.model_egit_ui
```

### 📊 Micro Training (Hızlı Test)

```python
from src.training.micro_lora_training import start_micro_training

# 5 dakikalık test eğitimi
start_micro_training()
```

## 📊 RTX 3060 Optimizasyonları

### 🎯 Memory Management
- **Adaptive Batch Size**: Dinamik batch boyutu (1-4)
- **Gradient Accumulation**: 32 step accumulation
- **Memory Monitoring**: %85 RAM, %95 kritik eşikler
- **SWAP Cleanup**: Agresif swap temizleme

### ⚡ Training Configuration
```yaml
training:
  batch_size: 1
  gradient_accumulation_steps: 32
  learning_rate: 5e-5
  bf16: true
  gradient_checkpointing: true
  quantization:
    bits: 4
    type: "nf4"
```

### 🔧 LoRA Settings
```yaml
lora:
  r: 16
  alpha: 32
  dropout: 0.1
  target_modules: ["q_proj", "v_proj"]
```

## 🧪 Test

### 🔍 Sistem Kontrolü
```bash
python tests/check_system.py
```

### 🧪 Unit Tests
```bash
pytest tests/
```

### 🎯 Specific Tests
```bash
# UI testi
python tests/test_ui.py

# Training testi
python tests/test_training.py

# Dataset testi
python tests/test_dataset.py
```

## 📁 Proje Yapısı

```
SeydappAI_ModelTrainer/
├── 📄 main.py                    # Ana uygulama giriş noktası
├── 📄 pyproject.toml            # Proje konfigürasyonu
├── 📄 requirements.txt          # Python dependencies
├── 📁 src/                      # Ana kaynak kodu
│   ├── 🎨 ui/                   # Kullanıcı arayüzü
│   │   ├── ultra_modern_training_ui.py
│   │   ├── ai_chat_interface.py # AI Chat sistemi (YENİ!)
│   │   ├── builder/             # UI bileşenleri
│   │   │   ├── control_panel/   # Kontrol paneli
│   │   │   ├── dashboard_cards/ # Dashboard kartları
│   │   │   └── responsive_sidebar/ # Yan menü
│   │   └── views/               # UI görünümleri
│   │       ├── chat_view.py     # AI Chat arayüzü (YENİ!)
│   │       ├── analytics_view.py # Analytics görünümü (YENİ!)
│   │       ├── models_view.py   # Model yönetimi (YENİ!)
│   │       ├── training_view.py # Training konfigürasyonu
│   │       ├── logs_view.py     # Log görünümü
│   │       └── settings_view.py # Ayarlar
│   ├── 🧠 core/                 # Temel sistem
│   │   ├── config.py           # Konfigürasyon yönetimi
│   │   └── app_manager.py      # Uygulama yöneticisi
│   ├── 🎯 training/             # Eğitim modülleri
│   │   ├── starcoder2_trainer.py
│   │   ├── rtx3060_training.py
│   │   ├── autonomous_trainer.py
│   │   └── micro_lora_training.py
│   ├── 🤖 models/               # Model yönetimi
│   │   ├── model_loader.py
│   │   ├── core/               # Temel model işlemleri
│   │   ├── memory/             # Bellek yönetimi
│   │   └── training/           # Eğitim utilities
│   ├── 🔍 research/             # Araştırma modülleri
│   │   ├── web_scraper.py
│   │   ├── intelligent_web_scraper.py
│   │   ├── web_search_utils.py  # Programming question search (YENİ!)
│   │   ├── real_web_scraper.py  # Gerçek web scraping (YENİ!)
│   │   └── knowledge_extractor.py
│   ├── 🧠 knowledge/            # Bilgi yönetimi
│   │   ├── rag_retriever.py
│   │   ├── knowledge_graph.py
│   │   └── context_builder.py
│   ├── 📊 data/                 # Veri işleme
│   │   ├── dataset_manager.py
│   │   └── preprocessor.py
│   ├── 🔧 utils/                # Yardımcı araçlar
│   │   ├── logger.py
│   │   ├── gpu_monitor.py
│   │   └── environment.py
│   └── 🎓 learning/             # Öğrenme algoritmaları
│       ├── incremental_trainer.py
│       ├── confidence_scorer.py
│       └── knowledge_merger.py
├── 📁 configs/                  # Konfigürasyon dosyaları
│   ├── app_config.yaml
│   ├── training_profiles.yaml
│   └── self_learning_config.yaml
├── 📁 tests/                    # Test dosyaları
│   ├── test_ui.py
│   ├── test_training.py
│   ├── test_dataset.py
│   └── check_system.py
├── 📁 datasets/                 # Eğitim verileri
│   └── conversations/
├── 📁 storage/                  # Veri depolama
│   ├── data/
│   └── backups/
├── 📁 trained_models/           # Eğitilmiş modeller
├── 📁 model_output/             # Model çıktıları
└── 📁 logs/                     # Log dosyaları
```

## 🔧 Konfigürasyon

### 📄 app_config.yaml
```yaml
app:
  title: "SeydappAI Model Trainer"
  version: "1.0.0"
  window:
    width: 1200
    height: 1000
  theme: "dark"

training:
  default_epochs: 6
  default_batch_size: 1
  default_learning_rate: 1e-4
  max_sequence_length: 2048
  output_dir: "./trained_models"

models:
  starcoder2:
    base_models:
      - "bigcode/starcoder2-3b"
      - "bigcode/starcoder2-7b"
    quantization:
      enabled: true
      bits: 4
      type: "nf4"
```

### 🎯 Training Profiles
```yaml
profiles:
  rtx3060_safe:
    batch_size: 1
    gradient_accumulation_steps: 32
    learning_rate: 5e-5
    memory_threshold: 85
    
  rtx3060_aggressive:
    batch_size: 2
    gradient_accumulation_steps: 16
    learning_rate: 1e-4
    memory_threshold: 90
```

## 🧠 Self-Learning AI Mimarisi

### 📚 Knowledge Database Schema
```sql
-- Öğrenilen bilgileri saklayan ana tablo
CREATE TABLE learned_knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,                    -- Kullanıcı sorusu
    response TEXT NOT NULL,                 -- AI cevabı
    category TEXT NOT NULL,                 -- Kategori (android, python, vb.)
    keywords TEXT NOT NULL,                 -- Anahtar kelimeler (JSON)
    quality_score REAL NOT NULL,           -- Kalite puanı (0-10)
    usage_count INTEGER DEFAULT 0,         -- Kaç kez kullanıldı
    learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performans için indexler
CREATE INDEX idx_category ON learned_knowledge(category);
CREATE INDEX idx_quality ON learned_knowledge(quality_score);
CREATE INDEX idx_usage ON learned_knowledge(usage_count);
```

### 🎯 Learning Algorithm
```python
def analyze_and_learn(self, user_query: str, ai_response: str, web_content: str = ""):
    """
    🧠 Akıllı öğrenme algoritması
    
    1. Kategori Tespiti: Soruyu otomatik kategorize et
    2. Anahtar Kelime Çıkarımı: Önemli kelimeleri tespit et
    3. Kalite Değerlendirmesi: Cevabı 0-10 arası puanla
    4. Veritabanı Kayıt: Bilgiyi kalıcı olarak sakla
    """
    category = self._detect_category(user_query)
    keywords = self._extract_keywords(user_query)
    quality_score = self._assess_quality(ai_response)
    
    # Yüksek kaliteli bilgileri sakla (>= 5.0)
    if quality_score >= 5.0:
        self._save_knowledge(user_query, ai_response, category, keywords, quality_score)
        return True
    return False
```

### 🔍 Smart Search Algorithm
```python
def search_learned_knowledge(self, query: str) -> Optional[Dict]:
    """
    🎯 Akıllı arama algoritması
    
    1. Anahtar Kelime Eşleştirme: Query'deki kelimeleri ara
    2. Kategori Filtreleme: İlgili kategorilerde ara
    3. Kalite Sıralaması: En kaliteli cevapları öncelikle
    4. Kullanım Güncellemesi: Bulunan bilginin kullanım sayısını artır
    """
    keywords = self._extract_keywords(query)
    category = self._detect_category(query)
    
    # Veritabanında ara
    results = self._search_by_keywords_and_category(keywords, category)
    
    if results:
        best_match = max(results, key=lambda x: x['quality_score'])
        self._increment_usage_count(best_match['id'])
        return best_match
    
    return None
```

## 🛠️ Geliştirme

### 🔧 Development Setup
```bash
# Development dependencies kur
pip install -e ".[dev]"

# Code formatting
black src/ tests/

# Linting
flake8 src/ tests/

# Type checking (opsiyonel)
mypy src/
```

### 📝 Logging
```python
import logging
logger = logging.getLogger(__name__)

# Log levels
logger.debug("Debug mesajı")
logger.info("Info mesajı")
logger.warning("Uyarı mesajı")
logger.error("Hata mesajı")
```

### 🧹 Temizlik Komutları
```bash
# Pycache temizleme
find . -type d -name "__pycache__" -exec rm -rf {} +

# Log temizleme
rm -rf logs/*.log

# Model cache temizleme
rm -rf models_cache/*
```

## 🎯 Kullanım Örnekleri

### 🤖 Basit Model Eğitimi
```python
from src.training.starcoder2_trainer import StarCoder2Trainer

trainer = StarCoder2Trainer(
    model_name="bigcode/starcoder2-3b",
    output_dir="./my_model"
)

trainer.train(
    dataset_path="./datasets/conversations",
    epochs=3,
    batch_size=1
)
```

### 💬 AI Chat Kullanımı (YENİ!)
```python
from src.ui.ai_chat_interface import AIChatInterface

# AI Chat başlatma
ai_chat = AIChatInterface(page)

# Programlama sorusu sorma
response = await ai_chat.get_ai_response(
    "Android için java programlama dili ile basit bir listview layout dosyası ile birlikte nasıl oluşturulur?"
)

# Detaylı XML ve Java kod örnekleri alırsınız!
```

### 🔍 Web Search Utils
```python
from src.research.web_search_utils import search_programming_question

# Programming question detection ve web search
results = await search_programming_question("Python list comprehension nasıl kullanılır?")
for result in results:
    print(f"Title: {result['title']}")
    print(f"Content: {result['content']}")
```

### 🔍 Web Scraping
```python
from src.research.intelligent_web_scraper import IntelligentWebScraper

scraper = IntelligentWebScraper()
content = scraper.scrape_topic("Python machine learning")
```

### 🧠 RAG Kullanımı
```python
from src.knowledge.rag_retriever import RAGRetriever

rag = RAGRetriever()
context = rag.retrieve("How to train neural networks?")
```

## 🚨 Sorun Giderme

### ❌ Yaygın Hatalar

1. **CUDA Out of Memory**:
   - Batch size'ı azaltın (1'e düşürün)
   - Gradient checkpointing aktif edin
   - Model quantization kullanın

2. **Flet UI Hatası**:
   - Flet versiyonunu kontrol edin (0.28.3+)
   - `pip install --upgrade flet`

3. **Import Hatası**:
   - Virtual environment aktif mi kontrol edin
   - `pip install -r requirements.txt` çalıştırın

4. **AI Chat Yanıt Vermiyor (YENİ!)**:
   - Thread durumunu kontrol edin: `threading.active_count()`
   - RAG sistemini test edin: `from src.knowledge.rag_retriever import RAGRetriever`
   - Web search test edin: `from src.research.web_search_utils import search_programming_question`

5. **AI Chat UI Donuyor**:
   - Background processing aktif mi kontrol edin
   - Event loop conflict olabilir - uygulamayı yeniden başlatın
   - Thread-safe processing kontrolü yapın

### 🔧 Debug Mode
```bash
python main.py --debug
```

### 📊 Sistem Durumu
```bash
python tests/check_system.py
```

### 🤖 AI Chat Test (YENİ!)
```bash
# AI Chat sistemini test edin
python -c "
from src.ui.ai_chat_interface import AIChatInterface
print('✅ AI Chat system - OK')
"

# Web search test
python -c "
from src.research.web_search_utils import search_programming_question
import asyncio
result = asyncio.run(search_programming_question('Python test'))
print(f'✅ Web search - {len(result)} results found')
"
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### 📋 Katkı Kuralları
- Code style: Black formatter kullanın
- Tests: Yeni özellikler için test yazın
- Documentation: README'yi güncelleyin
- Commit messages: Açıklayıcı mesajlar yazın

## 📊 Performans Metrikleri

### 🎯 RTX 3060 Benchmarks
- **3B Model**: ~2GB VRAM, 45 dakika/epoch
- **7B Model**: ~6GB VRAM, 2 saat/epoch
- **Micro Training**: 5 dakika, test amaçlı

### 📈 Memory Usage
- **Base Memory**: ~2GB sistem
- **Model Loading**: +2-6GB (model boyutuna göre)
- **Training**: +1-3GB (batch size'a göre)

## 🔗 Faydalı Linkler

- [Flet Documentation](https://flet.dev)
- [Transformers Library](https://huggingface.co/transformers)
- [PEFT (LoRA) Guide](https://huggingface.co/docs/peft)
- [StarCoder2 Models](https://huggingface.co/bigcode)
- [BitsAndBytes](https://github.com/TimDettmers/bitsandbytes)

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- **Hugging Face**: Transformers ve model hub için
- **Flet Team**: Modern UI framework için
- **BigCode**: StarCoder2 modelleri için
- **PyTorch Team**: Deep learning framework için

---

<div align="center">

**🤖 SeydappAI ModelTrainer ile AI modellerinizi kolayca eğitin! 🚀**

[⭐ Star](https://github.com/your-username/SeydappAI_ModelTrainer) | [🐛 Issues](https://github.com/your-username/SeydappAI_ModelTrainer/issues) | [📖 Wiki](https://github.com/your-username/SeydappAI_ModelTrainer/wiki)

</div>