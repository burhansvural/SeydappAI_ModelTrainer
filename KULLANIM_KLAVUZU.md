# 📖 SeydappAI ModelTrainer - Kullanım Klavuzu

**Kapsamlı Kullanım Rehberi (v2.1.0)** - Başlangıçtan ileri seviyeye kadar tüm özellikler

## 🆕 v2.1.0 Güncellemeleri
- ✅ **Flask Blog Sorunu Çözüldü**: Import hatası ve backend detection iyileştirildi
- 🔧 **Enhanced AI Chat**: Backend/Frontend framework'leri için özel çözümler
- 📚 **Self-Learning System**: Defensive programming ve hata kontrolü
- 🎯 **Project-Specific Solutions**: Flask blog, React e-ticaret kapsamlı rehberleri

---

## 📋 İçindekiler

1. [🚀 Hızlı Başlangıç](#-hızlı-başlangıç)
2. [🎮 Ana Arayüz Kullanımı](#-ana-arayüz-kullanımı)
3. [🧠 Self-Learning AI Chat (YENİ!)](#-self-learning-ai-chat-yeni)
4. [🤖 Model Eğitimi](#-model-eğitimi)
5. [🔍 Araştırma ve Web Scraping](#-araştırma-ve-web-scraping)
6. [📊 İzleme ve Monitoring](#-izleme-ve-monitoring)
7. [⚙️ Konfigürasyon](#️-konfigürasyon)
8. [🧪 Test ve Debug](#-test-ve-debug)
9. [🚨 Sorun Giderme](#-sorun-giderme)
10. [💡 İpuçları ve Püf Noktaları](#-ipuçları-ve-püf-noktaları)

---

## 🚀 Hızlı Başlangıç

### 1️⃣ İlk Kurulum ve Çalıştırma

```bash
# 1. Projeyi klonlayın
git clone https://github.com/your-username/SeydappAI_ModelTrainer.git
cd SeydappAI_ModelTrainer

# 2. Virtual environment oluşturun
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Dependencies kurun
pip install -r requirements.txt

# 4. İlk çalıştırma
python main.py
```

### 2️⃣ İlk Test Eğitimi (5 Dakika)

```bash
# Sistem kontrolü
python tests/check_system.py

# Micro test eğitimi
python -c "from src.training.micro_lora_training import start_micro_training; start_micro_training()"
```

---

## 🎮 Ana Arayüz Kullanımı

### 🖥️ Arayüz Bileşenleri

#### 📊 **Dashboard (Ana Ekran)**
- **Sistem Durumu**: CPU, RAM, GPU kullanımı
- **Eğitim Metrikleri**: Loss, accuracy, progress
- **Aktif İşlemler**: Çalışan thread'ler ve görevler
- **Bellek Durumu**: Memory usage ve cleanup durumu

#### 🎛️ **Kontrol Paneli**

**🎯 Training Configuration Bölümü:**
- **🤖 Model Seçimi**: Dropdown menü ile 5 farklı model seçeneği
  - `bigcode/starcoder2-3b` (Varsayılan - RTX 3060 için önerilen)
  - `bigcode/starcoder2-7b` (Daha büyük model)
  - `microsoft/CodeBERT-base`
  - `microsoft/codebert-base-mlm`
  - `huggingface/CodeBERTa-small-v1`

- **⚙️ Training Profil Seçimi**: Dropdown menü ile 3 profil seçeneği
  - `micro_test`: 5-Minute Test - Hızlı test için minimal ayarlar
  - `rtx3060_optimized`: RTX 3060 Optimized - RTX 3060 için optimize edilmiş (Varsayılan)
  - `production`: Production Training - Tam kapsamlı production training
  - **Dinamik Açıklama**: Profil seçildiğinde açıklama otomatik güncellenir

- **🚀 Start Training**: Büyük turuncu gradient buton ile training başlatma
  - Seçilen model ve profil ile otomatik training başlatır
  - Visual feedback ve glow efekti
  - Double-click koruması

**🤖 Advanced Features Bölümü:**
- **Autonomous Mode**: Otomatik eğitim modu
- **Quick Research**: Hızlı araştırma modu
- **Stop All**: Tüm işlemleri durdurma

#### 📝 **Enhanced View System (YENİ!)**
- **💬 AI Chat**: Akıllı programlama asistanı
- **🎯 Analytics**: Eğitim analitikleri ve performans metrikleri
- **🤖 Models**: Model yönetimi ve karşılaştırma
- **🎓 Training**: Detaylı eğitim konfigürasyonu
- **📝 Logs**: Gelişmiş log filtreleme ve arama
- **⚙️ Settings**: Kapsamlı ayarlar paneli

#### 📝 **Log Sistemi**
- **Real-time Logs**: Canlı log akışı
- **Log Filtreleme**: Seviye bazlı filtreleme (DEBUG, INFO, WARNING, ERROR)
- **Log Export**: Log dosyalarını dışa aktarma

### 🎯 Temel Kullanım Adımları

#### **Adım 1: Sistem Kontrolü**
1. Uygulamayı başlatın: `python main.py`
2. Dashboard'da sistem durumunu kontrol edin
3. GPU ve RAM kullanımını gözlemleyin
4. Gerekirse sistem optimizasyonu yapın

#### **Adım 2: Model ve Profil Seçimi**

**🎯 Training Configuration Paneli Kullanımı:**

1. **🤖 Model Seçimi (Dropdown)**:
   - Kontrol panelinde "Model Selection" dropdown'ını açın
   - 5 farklı model seçeneği:
     - `bigcode/starcoder2-3b` ⭐ (Varsayılan - RTX 3060 için önerilen)
     - `bigcode/starcoder2-7b` (Daha büyük model - daha fazla VRAM gerekir)
     - `microsoft/CodeBERT-base` (Code understanding için)
     - `microsoft/codebert-base-mlm` (Masked language modeling)
     - `huggingface/CodeBERTa-small-v1` (Küçük ve hızlı)
   - Model seçildiğinde status bar'da seçim görünür

2. **⚙️ Training Profil Seçimi (Dropdown)**:
   - "Training Profile" dropdown'ını açın
   - 3 profil seçeneği:
     - `micro_test`: **5-Minute Test** - Hızlı test için minimal ayarlar
     - `rtx3060_optimized`: **RTX 3060 Optimized** ⭐ (Varsayılan) - RTX 3060 için optimize edilmiş
     - `production`: **Production Training** - Tam kapsamlı production training
   - **Dinamik Açıklama**: Profil seçildiğinde altında açıklama otomatik güncellenir
   - Profil seçildiğinde log sisteminde bilgi görünür

3. **🎨 Görsel Feedback**:
   - Model seçimi: Mavi tema, psychology icon
   - Profil seçimi: Yeşil tema, settings icon
   - Her seçim log sistemine kaydedilir
   - Status bar'da seçimler görüntülenir

#### **Adım 3: Dataset Hazırlama**
1. `datasets/conversations/` klasörüne veri dosyalarınızı koyun
2. JSON Lines (.jsonl) formatında olmalı:
```json
{"text": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"}
{"text": "# Python list comprehension örneği\nnumbers = [x**2 for x in range(10)]"}
```

#### **Adım 4: Eğitimi Başlatma**

**🚀 Yeni Start Training Sistemi:**

1. **Training Başlatma**:
   - **🚀 Start Training** büyük turuncu butonuna tıklayın
   - Buton seçilen model ve profil bilgilerini kullanır
   - **Double-click koruması**: Hızlı tıklamalara karşı korumalı
   - **Visual feedback**: Glow efekti ve animasyon

2. **Otomatik İşlemler**:
   - Training state otomatik başlatılır
   - Dashboard monitoring aktif edilir
   - Log sistemine başlatma kaydı düşer
   - Status bar "🔥 Training Active" olarak güncellenir

3. **İzleme ve Takip**:
   - **Dashboard Cards**: Real-time güncelleme başlar
   - **Progress Bar**: Adım bazlı ilerleme takibi
   - **Log Sistemi**: Detaylı training logları
   - **Memory Monitoring**: GPU ve RAM kullanımı takibi

4. **Training Süreci**:
   - Seçilen model otomatik yüklenir
   - Profil ayarları uygulanır
   - Dataset işleme başlar
   - LoRA adapter training başlatılır

---

## 🧠 Self-Learning AI Chat (YENİ!)

### 🎓 Kendini Geliştiren Yapay Zeka Asistanı

SeydappAI ModelTrainer artık **Self-Learning AI Chat** ile donatılmış! Bu özellik sadece programlama sorularınızı cevaplamakla kalmaz, **her etkileşimde kendini geliştirerek daha akıllı hale gelir**.

#### **🚀 Self-Learning Özellikleri**
- **🧠 Continuous Learning**: Her soru-cevap etkileşiminde yeni bilgi öğrenir
- **📚 Knowledge Database**: Öğrenilen bilgileri SQLite veritabanında saklar
- **🎯 Smart Categorization**: Soruları otomatik kategorize eder (android, python, web, vb.)
- **⭐ Quality Assessment**: Cevap kalitesini 0-10 arası akıllı algoritma ile puanlar
- **📊 Learning Dashboard**: Detaylı öğrenme istatistikleri ve yönetim paneli
- **🔄 Usage Tracking**: Hangi bilgilerin ne kadar kullanıldığını takip eder
- **🧹 Smart Cleanup**: Eski/gereksiz bilgileri otomatik temizler

#### **🎯 Chat Özellikleri (v2.1.0 Güncellemesi)**
- **🔍 Enhanced Programming Question Detection**: 
  - **Backend Frameworks**: Flask, Django, Express.js otomatik tespit
  - **Frontend Frameworks**: React, Vue, Angular özel çözümler
  - **Mobile Development**: Android, Flutter, iOS desteği
  - **Database Systems**: SQL, MongoDB, PostgreSQL rehberleri
- **🧠 Advanced Memory System**: Önceki sorulara verilen cevapları hatırlar
- **🌐 Web Search + Learning**: RAG bilgisi yoksa internetten arar ve öğrenir
- **🔧 Project-Specific Solutions**:
  - **Flask Blog**: Kapsamlı blog uygulaması (11,638 karakter)
  - **React E-commerce**: Tam e-ticaret çözümü
  - **Android Apps**: ListView, RecyclerView örnekleri
- **📝 Detailed Code Examples**: XML, Java, Python, HTML, CSS, JavaScript örnekleri
- **🧵 Thread-Safe Processing**: UI donmadan arka plan işlemi
- **💬 Modern Chat UI**: Typing indicator, message bubbles, smooth animations

#### **📱 Desteklenen Konular (Genişletildi!)**

**🔧 Backend Development:**
- **Flask**: Blog uygulaması, API geliştirme, SQLite entegrasyonu
- **Django**: Web framework, ORM kullanımı, admin panel
- **Express.js**: Node.js backend, REST API, middleware

**⚡ Frontend Development:**
- **React**: E-ticaret sitesi, component yapısı, Redux kullanımı
- **Vue.js**: SPA geliştirme, Vuex state management
- **Angular**: TypeScript, component architecture

**🤖 Android Development:**
- ListView oluşturma (XML + Java)
- RecyclerView ve Custom Adapter
- Event handling ve lifecycle
- Material Design layout

**🐍 Python Programming:**
- List comprehension ve generators
- Functions, classes ve inheritance
- Loops, conditionals ve exception handling
- Data structures ve algorithms

**🌐 JavaScript:**
- Async/await patterns ve promises
- DOM manipulation ve event handling
- Array methods ve functional programming
- ES6+ features

**🗄️ Database Systems:**
- SQL queries ve joins
- MongoDB document operations
- PostgreSQL advanced features
- Database design patterns

#### **🚀 Self-Learning Kullanım Adımları**

1. **AI Chat Tab'ına Geçin**:
   - Ana arayüzde "AI Chat" sekmesine tıklayın
   - Modern chat arayüzü açılır
   - Header'da öğrenilen konu sayısını görebilirsiniz

2. **İlk Soru (Öğrenme Başlar)**:
   ```
   🔧 Backend Framework Örnekleri:
   - "Python Flask ile bir blog uygulaması yap. Ana sayfa, yazı ekleme, yazı düzenleme sayfaları olsun. SQLite veritabanı kullan."
   - "Django ile REST API nasıl oluşturulur?"
   - "Express.js ile authentication sistemi nasıl kurulur?"
   
   ⚡ Frontend Framework Örnekleri:
   - "React ile bir e-ticaret sitesi yap. Ürün listesi, sepet, ödeme sayfaları olsun. Redux kullan."
   - "Vue.js ile SPA nasıl geliştirilir?"
   - "Angular ile component nasıl oluşturulur?"
   
   🤖 Mobile Development Örnekleri:
   - "Android için java programlama dili ile basit bir listview layout dosyası ile birlikte nasıl oluşturulur?"
   - "Flutter ile cross-platform uygulama nasıl geliştirilir?"
   
   🐍 Python Örnekleri:
   - "Python'da list comprehension nasıl kullanılır?"
   - "Python ile web scraping nasıl yapılır?"
   
   🌐 JavaScript Örnekleri:
   - "JavaScript'te async await örneği verebilir misin?"
   - "Node.js ile API nasıl geliştirilir?"
   ```

3. **AI Öğrenme Süreci**:
   - AI sorunuzu analiz eder
   - Önce öğrendiği bilgilerde arar
   - Bilgi yoksa web'den araştırır
   - **Yeni bilgiyi öğrenir ve saklar**
   - Detaylı kod örnekleri ile cevap verir

4. **İkinci Soru (Hafıza Testi)**:
   - Aynı konuda tekrar soru sorun
   - AI artık **öğrendiği bilgiyi kullanır**
   - "🧠 Self-Learning AI Response" etiketi görürsünüz
   - Çok daha hızlı cevap alırsınız

5. **Learning Dashboard'u Açın**:
   - Chat header'ındaki 🧠 butonuna tıklayın
   - Öğrenme istatistiklerini görün
   - Kategorilere göre bilgi dağılımını inceleyin

#### **💡 Örnek Kullanım**

**Soru**: "Android için java programlama dili ile basit bir listview layout dosyası ile birlikte nasıl oluşturulur?"

**AI Cevabı**:
```xml
<!-- activity_main.xml -->
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">

    <ListView
        android:id="@+id/listView"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

</LinearLayout>
```

```java
// MainActivity.java
public class MainActivity extends AppCompatActivity {
    private ListView listView;
    private ArrayAdapter<String> adapter;
    private ArrayList<String> itemList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        listView = findViewById(R.id.listView);
        
        itemList = new ArrayList<>();
        itemList.add("Item 1");
        itemList.add("Item 2");
        
        adapter = new ArrayAdapter<>(this, 
            android.R.layout.simple_list_item_1, itemList);
        listView.setAdapter(adapter);
    }
}
```

#### **🔧 Teknik Detaylar**

**Thread-Safe Processing:**
```python
def handle_chat_message(e):
    # UI thread'de user message eklenir
    add_user_message(message)
    
    # Background thread'de AI processing
    def process_ai_response():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            ai_response = loop.run_until_complete(
                ai_chat.get_ai_response(message)
            )
            # UI thread'de response eklenir
            e.page.run_thread(lambda: add_ai_message(ai_response))
        finally:
            loop.close()
    
    threading.Thread(target=process_ai_response, daemon=True).start()
```

**Question Detection:**
```python
def _is_android_listview_question(query: str) -> bool:
    android_keywords = ['android', 'listview', 'java', 'layout', 'xml']
    query_lower = query.lower()
    return sum(1 for keyword in android_keywords if keyword in query_lower) >= 2
```

#### **🎨 UI Components**

**Chat Messages:**
- **User Messages**: Sağ tarafta mor bubble
- **AI Messages**: Sol tarafta gri bubble + AI icon
- **Typing Indicator**: "🤔 Thinking..." mesajı
- **Smooth Animations**: Message appear/disappear efektleri

**Input Area:**
- **Multi-line TextField**: 1-3 satır otomatik genişleme
- **Send Button**: Turuncu gradient buton
- **Placeholder**: "Android ListView, Python, Java... herhangi bir programlama sorusu sorun!"

### 🎓 Learning Dashboard Kullanımı

#### **📊 Dashboard Açma**
1. Chat ekranında sağ üstteki **🧠 Psychology** butonuna tıklayın
2. "Self-Learning Dashboard" penceresi açılır
3. Detaylı öğrenme istatistiklerini görürsünüz

#### **📈 Dashboard Bileşenleri**

**📚 Genel İstatistikler:**
```
📚 Total Learned: 15 topics
🎯 Categories: 4 categories
```

**📊 Kategori Dağılımı:**
```
Android: 5 topics
Python: 4 topics  
Web: 3 topics
JavaScript: 3 topics
```

**⭐ En Çok Kullanılan Bilgiler:**
```
1. Android ListView - Used 8 times | Quality: 9.2/10
2. Python List Comprehension - Used 5 times | Quality: 8.8/10
3. JavaScript Async/Await - Used 3 times | Quality: 9.0/10
```

#### **🔧 Dashboard Kontrolleri**

**🧹 Cleanup Old Knowledge:**
- 30 günden eski bilgileri temizler
- Minimum 1 kez kullanılmış olması gerekir
- Temizlenen bilgi sayısını gösterir

**🧠 Learning Enabled/Disabled:**
- Öğrenme sistemini açıp kapatabilirsiniz
- Kapalıyken sadece mevcut bilgileri kullanır
- Açıkken yeni bilgileri öğrenmeye devam eder

#### **💡 Learning Quality Scoring**

AI cevapları şu kriterlere göre puanlanır:

**📏 Cevap Uzunluğu (0-2 puan):**
- Çok kısa (< 50 karakter): 0 puan
- Optimal (50-2000 karakter): 2 puan
- Çok uzun (> 2000 karakter): 1 puan

**💻 Kod Blokları (0-3 puan):**
- Kod bloğu yok: 0 puan
- 1-2 kod bloğu: 2 puan
- 3+ kod bloğu: 3 puan

**📋 Yapılandırılmış İçerik (0-2 puan):**
- Başlık/liste var: +1 puan
- İyi organize edilmiş: +1 puan

**🔧 Teknik Terimler (0-2 puan):**
- Programming terimleri: +1 puan
- Çok sayıda teknik terim: +1 puan

**😊 Kullanıcı Dostu (0-1 puan):**
- Emoji kullanımı: +1 puan

#### **🚀 Self-Learning Avantajları**

**⚡ Hızlı Cevaplar:**
- Öğrenilen konularda anında cevap
- Web araması gerektirmez
- Düşük gecikme süresi

**🎯 Kişiselleştirilmiş:**
- Kullanıcının sorduğu konularda uzmanlaşır
- Sık sorulan konulara odaklanır
- Kullanım geçmişine göre optimize olur

**📈 Sürekli Gelişim:**
- Her etkileşimde daha akıllı
- Bilgi kalitesi zamanla artar
- Kategori çeşitliliği genişler

**💾 Verimli Bellek:**
- Sadece kaliteli bilgileri saklar
- Eski bilgileri otomatik temizler
- Optimize edilmiş veritabanı yapısı

---

## 🎨 Yeni UI Özellikleri (v1.2)

### 🎯 Training Configuration Panel

**Yeni eklenen gelişmiş model ve profil seçimi sistemi:**

#### **🤖 Model Selector Component**
```python
# Kullanılabilir modeller
models = [
    "bigcode/starcoder2-3b",      # RTX 3060 için optimize
    "bigcode/starcoder2-7b",      # Daha büyük model
    "microsoft/CodeBERT-base",    # Code understanding
    "microsoft/codebert-base-mlm", # Masked language modeling
    "huggingface/CodeBERTa-small-v1" # Küçük ve hızlı
]
```

**Özellikler:**
- 🎨 **Mavi tema**: Psychology icon ile görsel tasarım
- 📋 **Dropdown menü**: Kolay model seçimi
- 🔄 **Event handling**: Seçim değişikliği otomatik algılanır
- 📊 **Status güncelleme**: Seçim status bar'da görünür
- 📝 **Log kaydı**: Her seçim log sistemine kaydedilir

#### **⚙️ Profile Selector Component**
```python
# Training profilleri
profiles = {
    "micro_test": "5-Minute Test - Hızlı test için minimal ayarlar",
    "rtx3060_optimized": "RTX 3060 Optimized - RTX 3060 için optimize edilmiş",
    "production": "Production Training - Tam kapsamlı production training"
}
```

**Özellikler:**
- 🎨 **Yeşil tema**: Settings icon ile görsel tasarım
- 📋 **Dropdown menü**: Profil seçimi
- 📝 **Dinamik açıklama**: Seçim yapıldığında açıklama güncellenir
- 🔄 **Event handling**: Profil değişikliği otomatik algılanır
- 📊 **Status güncelleme**: Profil bilgisi status bar'da görünür

#### **🚀 Start Training Button**
```python
# Büyük training butonu
button_features = {
    "size": "350x80 px",
    "gradient": "Orange to Red",
    "animation": "Ease-in-out transition",
    "shadow": "Glow effect",
    "protection": "Double-click protection"
}
```

**Özellikler:**
- 🎨 **Turuncu gradient**: Dikkat çekici tasarım
- ✨ **Glow efekti**: Box shadow ile görsel feedback
- 🔒 **Double-click koruması**: Hızlı tıklamalara karşı korumalı
- 🔄 **Animasyon**: Smooth transition efektleri
- 📊 **Training başlatma**: Seçilen model ve profil ile otomatik başlatır

### 🏗️ Factory Pattern Architecture

**UI Component Factory sistemi:**

```python
from src.ui.builder.control_panel.ui_components import UIComponentFactory

# Factory kullanımı
factory = UIComponentFactory()

# Model selector oluşturma
model_selector = factory.create_component(
    'model_selector',
    on_change=self.on_model_change
)

# Profile selector oluşturma
profile_selector = factory.create_component(
    'profile_selector', 
    on_change=self.on_profile_change
)

# Start training button oluşturma
start_btn = factory.create_component(
    'start_training_button',
    on_click=self.start_training
)
```

**Avantajları:**
- 🏗️ **Modüler tasarım**: Her component bağımsız
- 🔧 **Kolay genişletme**: Yeni componentler kolayca eklenebilir
- 🎯 **Separation of concerns**: UI logic ayrılmış
- 🔄 **Reusability**: Componentler tekrar kullanılabilir

### 🎮 Event Handler Sistemi

**Yeni event handler metodları:**

```python
class EventHandlers:
    def on_model_change(self, event):
        """Model seçimi değiştiğinde çağrılır"""
        new_model = event.control.value
        self.selected_model = new_model
        # Log ve status güncelleme
    
    def on_profile_change(self, event):
        """Profil seçimi değiştiğinde çağrılır"""
        new_profile = event.control.value
        self.selected_profile = new_profile
        # Açıklama ve status güncelleme
    
    def start_training(self, event):
        """Training başlatma event handler"""
        # Training config hazırla
        # Training state başlat
        # Dashboard monitoring aktif et
```

---

## 🤖 Model Eğitimi

### 🎯 Eğitim Türleri

#### **1. Micro Training (Test Amaçlı)**
```python
from src.training.micro_lora_training import start_micro_training

# 5 dakikalık hızlı test
result = start_micro_training()
print(f"Test sonucu: {result}")
```

**Özellikler:**
- ⏱️ Süre: ~5 dakika
- 📊 Dataset: 3 örnek
- 🎯 Amaç: Sistem testi
- 💾 Output: `./micro_test_results/`

#### **2. RTX 3060 Optimized Training**
```python
from src.training.rtx3060_training import start_optimized_training

# RTX 3060 için optimize edilmiş eğitim
config = {
    "model_name": "bigcode/starcoder2-3b",
    "dataset_path": "./datasets/conversations/",
    "output_dir": "./trained_models/my_model",
    "epochs": 3,
    "batch_size": 1,
    "learning_rate": 5e-5
}

result = start_optimized_training(config)
```

**Özellikler:**
- ⏱️ Süre: 1-3 saat (dataset boyutuna göre)
- 📊 Memory: ~6GB VRAM kullanımı
- 🎯 Amaç: Production-ready model
- 💾 Output: `./trained_models/`

#### **3. Autonomous Training**
```python
from src.training.autonomous_trainer import AutonomousTrainer

# Otomatik araştırma ve eğitim
trainer = AutonomousTrainer(knowledge_rag_system)
result = await trainer.trigger_autonomous_training()
```

**Özellikler:**
- 🔍 Web scraping ile otomatik veri toplama
- 🧠 RAG entegrasyonu
- 📈 Incremental learning
- 🎯 Sürekli öğrenme

### 📊 Eğitim Parametreleri

#### **LoRA (Low-Rank Adaptation) Ayarları**
```yaml
lora_config:
  r: 16                    # Rank (8-32 arası önerilir)
  alpha: 32               # Alpha değeri (genelde r*2)
  dropout: 0.1            # Dropout oranı
  target_modules:         # Hedef modüller
    - "q_proj"
    - "v_proj"
    - "k_proj"
    - "o_proj"
```

#### **Training Arguments**
```yaml
training_args:
  per_device_train_batch_size: 1    # RTX 3060 için güvenli
  gradient_accumulation_steps: 32   # Effective batch = 32
  num_train_epochs: 3               # Epoch sayısı
  learning_rate: 5e-5              # Öğrenme oranı
  warmup_steps: 100                # Warmup adımları
  logging_steps: 10                # Log aralığı
  save_steps: 100                  # Kaydetme aralığı
  bf16: true                       # Mixed precision
  gradient_checkpointing: true     # Memory optimization
```

### 🔧 Memory Optimization

#### **RTX 3060 için Özel Ayarlar**
```python
# Memory-aware batch sizing
def calculate_optimal_batch_size(available_vram_gb):
    if available_vram_gb >= 10:
        return 2
    elif available_vram_gb >= 8:
        return 1
    else:
        return 1  # Güvenli mod

# Gradient accumulation
effective_batch_size = batch_size * gradient_accumulation_steps
```

#### **Memory Monitoring**
- **%85 RAM**: Warning seviyesi
- **%95 RAM**: Critical seviye - otomatik cleanup
- **SWAP > %50**: Agresif temizlik başlatılır

---

## 🔍 Araştırma ve Web Scraping

### 🌐 Intelligent Web Scraper

#### **Temel Kullanım**
```python
from src.research.intelligent_web_scraper import IntelligentWebScraper

scraper = IntelligentWebScraper()

# Konu bazlı araştırma
content = scraper.scrape_topic("Python machine learning")
print(f"Toplanan içerik: {len(content)} sayfa")

# Belirli URL'lerden veri toplama
urls = [
    "https://docs.python.org/3/tutorial/",
    "https://pytorch.org/tutorials/"
]
data = scraper.scrape_urls(urls)
```

#### **Gelişmiş Filtreleme**
```python
from src.research.content_filter import ContentFilter

filter = ContentFilter()

# İçerik kalitesi filtreleme
filtered_content = filter.filter_by_quality(content, min_score=0.7)

# Dil filtreleme
turkish_content = filter.filter_by_language(content, language="tr")

# Konu relevansı filtreleme
relevant_content = filter.filter_by_relevance(content, topic="Python")
```

### 🧠 Knowledge Extraction

#### **Bilgi Çıkarma**
```python
from src.research.knowledge_extractor import KnowledgeExtractor

extractor = KnowledgeExtractor()

# Metin'den bilgi çıkarma
knowledge = extractor.extract_knowledge(text_content)

# Kod örnekleri çıkarma
code_examples = extractor.extract_code_examples(content)

# Kavram haritası oluşturma
concept_map = extractor.create_concept_map(knowledge)
```

#### **Knowledge Graph**
```python
from src.knowledge.knowledge_graph import SeydappAIKnowledgeGraph

kg = SeydappAIKnowledgeGraph()

# Bilgi ağı oluşturma
kg.add_knowledge_node("Python", "Python programming content", 0.9)

# İlişki kurma
kg.create_relationships(["Python", "Machine Learning", "AI"])

# Sorgu yapma
context = kg.retrieve_relevant_context("Python machine learning")
```

---

## 📊 İzleme ve Monitoring

### 📈 Real-time Dashboard

#### **🎮 Dashboard Cards**
1. **🔥 Training Status Card**
   - Dinamik durum göstergesi (Ready/Training Active/GPU Active)
   - Anlık GPU kullanımı (% ve renk kodlaması)
   - VRAM kullanımı (Kullanılan/Toplam GB)
   - CPU ve RAM kullanımı
   - GPU sıcaklığı (°C)
   - Sistem uptime

2. **📊 Progress Card**
   - Adım takibi (Current/Total steps)
   - Training loss (3 ondalık hassasiyet)
   - ETA (Tahmini bitiş süresi)
   - Circular progress bar

3. **🖥️ System Info Card**
   - GPU model bilgisi
   - Disk boş alanı
   - Network trafiği
   - CPU frekansı

#### **🔄 Canlı Veri Sistemi**
- **2 saniye aralık**: Otomatik güncelleme
- **Renk kodlaması**: Durum bazlı görsel feedback
- **Thread-safe**: Güvenli arka plan işlemi
- **Hata toleransı**: Bir component hata verse diğerleri çalışır

#### **Sistem Metrikleri**
- **CPU Usage**: İşlemci kullanımı (% ve renk kodlu)
- **RAM Usage**: Bellek kullanımı (% ve renk kodlu)
- **GPU Usage**: VRAM kullanımı (% ve renk kodlu)
- **Disk I/O**: Disk okuma/yazma
- **Network**: Ağ trafiği (MB)

#### **Eğitim Metrikleri**
- **Loss**: Training ve validation loss
- **Learning Rate**: Öğrenme oranı değişimi
- **Steps/Second**: Eğitim hızı
- **ETA**: Tahmini bitiş süresi (HH:MM formatında)
- **Progress**: Görsel ilerleme çemberi

#### **🎯 Training State Management**
```python
from src.utils.training_state import training_state

# Training başlatma
config = {
    "model_name": "bigcode/starcoder2-3b",
    "epochs": 3,
    "max_steps": 100,
    "learning_rate": 5e-5
}
training_state.start_training(config)

# Progress güncelleme (training loop içinde)
training_state.update_progress(
    current_step=25,
    train_loss=1.5,
    eval_loss=1.7,
    learning_rate=4e-5
)

# Durum kontrolü
if training_state.is_training():
    progress = training_state.get_progress_percentage()
    print(f"Training progress: {progress:.1f}%")

# Training durdurma
training_state.stop_training()
```

#### **Memory Monitoring**
```python
from src.utils.gpu_monitor import SystemMonitor

# Sistem durumu
real_status = SystemMonitor.get_real_training_status()
print(f"GPU: {real_status['gpu_usage']:.1f}%")
print(f"VRAM: {real_status['vram_used']:.1f}GB")

# Detaylı sistem bilgileri
detailed_stats = SystemMonitor.get_detailed_system_stats()
gpu_info = detailed_stats.get('gpu_info', {})
print(f"GPU Model: {gpu_info.get('name', 'Unknown')}")

# Training metrikleri
metrics = SystemMonitor.get_training_metrics()
print(f"Current step: {metrics['current_step']}/{metrics['total_steps']}")
print(f"Training loss: {metrics['train_loss']:.3f}")
```

### 📝 Logging System

#### **Log Seviyeleri**
- **DEBUG**: Detaylı debug bilgileri
- **INFO**: Genel bilgi mesajları
- **WARNING**: Uyarı mesajları
- **ERROR**: Hata mesajları
- **CRITICAL**: Kritik hatalar

#### **Log Filtreleme**
```python
import logging

# Belirli modül için log seviyesi
logging.getLogger("src.training").setLevel(logging.DEBUG)
logging.getLogger("src.ui").setLevel(logging.INFO)

# Custom logger
logger = logging.getLogger(__name__)
logger.info("🚀 Training başlatıldı")
logger.warning("⚠️ Memory usage yüksek")
logger.error("❌ Model yükleme hatası")
```

---

## ⚙️ Konfigürasyon

### 📄 Ana Konfigürasyon (app_config.yaml)

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

logging:
  level: "INFO"
  file: "logs/training.log"
  max_size_mb: 10
  backup_count: 3
```

### 🎯 Training Profiles (training_profiles.yaml)

```yaml
training_profiles:
  micro_test:
    name: "5-Minute Test"
    description: "Hızlı test için minimal ayarlar"
    model: "bigcode/starcoder2-3b"
    max_steps: 2
    epochs: 1
    learning_rate: 1e-4
    batch_size: 1
    lora_rank: 8

  rtx3060_optimized:
    name: "RTX 3060 Optimized"
    description: "RTX 3060 için optimize edilmiş ayarlar"
    model: "bigcode/starcoder2-3b"
    max_steps: 100
    epochs: 3
    learning_rate: 5e-5
    batch_size: 1
    lora_rank: 16

  production:
    name: "Production Training"
    description: "Tam kapsamlı production training"
    model: "bigcode/starcoder2-3b"
    max_steps: 1000
    epochs: 5
    learning_rate: 2e-5
    batch_size: 4
    lora_rank: 32

hardware_profiles:
  rtx3060:
    vram_gb: 12
    recommended_batch_size: 2
    max_sequence_length: 512
    quantization: "4bit"
    mixed_precision: true
```

### 🧠 Self-Learning Config (self_learning_config.yaml)

```yaml
autonomous_learning:
  enabled: true
  research_topics:
    - "Python machine learning"
    - "Deep learning tutorials"
    - "PyTorch optimization"
    - "Transformer models"
  
  scraping:
    max_pages_per_topic: 50
    content_quality_threshold: 0.7
    language_filter: ["en", "tr"]
  
  training:
    incremental_steps: 100
    confidence_threshold: 0.8
    max_learning_cycles: 10
```

---

## 🧪 Test ve Debug

### 🔍 Sistem Kontrolü

```bash
# Kapsamlı sistem kontrolü
python tests/check_system.py

# Çıktı örneği:
# 🔍 Safe System Check - INTEGER INDEX MODE
# ==================================================
# 🐍 Python: 3.9.7
# 🖥️ Platform: linux
# 📁 Path entries: 15
# 
# 📦 Critical modules:
# ✅ flet: 0.28.3
# ✅ torch: 2.0.1
# ✅ transformers: 4.35.2
```

### 🧪 Unit Tests

```bash
# Tüm testleri çalıştır
pytest tests/ -v

# Belirli test dosyası
pytest tests/test_training.py -v

# Coverage ile
pytest tests/ --cov=src --cov-report=html
```

### 🐛 Debug Mode

```bash
# Debug mode ile çalıştırma
python main.py --debug

# Sadece UI test
python main.py --test-ui

# Verbose logging
PYTHONPATH=. python main.py --log-level=DEBUG
```

### 📊 Memory Profiling

```python
from src.utils.gpu_monitor import GPUMonitor
import psutil

# System memory
memory = psutil.virtual_memory()
print(f"RAM: {memory.percent}% used")

# GPU memory
gpu_monitor = GPUMonitor()
gpu_stats = gpu_monitor.get_detailed_stats()
print(f"GPU Memory: {gpu_stats}")
```

---

## 🚨 Sorun Giderme

### ❌ Yaygın Hatalar ve Çözümleri

#### **🆕 1. AI Chat Import Hatası (v2.1.0'da Çözüldü)**
```
ImportError: cannot import name 'RAGRetriever' from 'src.knowledge.rag_retriever'
```

**✅ Çözüm:**
- Bu hata v2.1.0 güncellemesi ile çözülmüştür
- Eğer hala görüyorsanız:
```bash
# Uygulamayı yeniden başlatın
python main.py

# Veya cache'i temizleyin
rm -rf __pycache__/
rm -rf src/__pycache__/
```

#### **🆕 2. Self-Learning System Hatası**
```
KeyError: 'keywords' / 'query' / 'quality_score'
```

**✅ Çözüm:**
- Bu hata v2.1.0'da defensive programming ile çözülmüştür
- Eski öğrenme verilerini temizlemek için:
```bash
rm -rf storage/data/learned_knowledge.json
```

#### **🆕 3. Flask Blog Sorusu Cevap Alamama**
```
AI Chat'te Flask sorusu sorulduğunda cevap gelmiyor
```

**✅ Çözüm:**
- v2.1.0'da Flask detection iyileştirilmiştir
- Backend framework'leri artık doğru tespit edilir
- Flask blog sorusu için 11,638 karakter kapsamlı cevap verilir

#### **4. CUDA Out of Memory**
```
RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB
```

**Çözümler:**
```bash
# Batch size'ı azaltın
# configs/training_profiles.yaml'da:
batch_size: 1  # 2'den 1'e düşürün

# Gradient accumulation artırın
gradient_accumulation_steps: 64  # 32'den 64'e çıkarın

# Model quantization aktif edin
quantization:
  enabled: true
  bits: 4
```

#### **2. Flet UI Hatası**
```
ImportError: cannot import name 'ControlState' from 'flet'
```

**Çözümler:**
```bash
# Flet'i güncelleyin
pip install --upgrade flet>=0.28.3

# Virtual environment'i yeniden oluşturun
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### **3. Model Loading Hatası**
```
OSError: Can't load tokenizer for 'bigcode/starcoder2-3b'
```

**Çözümler:**
```bash
# Internet bağlantısını kontrol edin
ping huggingface.co

# Cache'i temizleyin
rm -rf ~/.cache/huggingface/

# Manuel model indirme
python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('bigcode/starcoder2-3b')"
```

#### **4. Permission Denied**
```
PermissionError: [Errno 13] Permission denied: './logs/training.log'
```

**Çözümler:**
```bash
# Klasör izinlerini düzeltin
chmod -R 755 logs/
mkdir -p logs trained_models datasets

# Farklı output directory kullanın
export OUTPUT_DIR="$HOME/seydappai_output"
python main.py
```

#### **5. AI Chat Yanıt Vermiyor (YENİ!)**
```
AI Chat'te mesaj gönderiyorum ama yanıt gelmiyor
```

**Çözümler:**
```bash
# 1. Thread durumunu kontrol edin
python -c "
import threading
print(f'Active threads: {threading.active_count()}')
for thread in threading.enumerate():
    print(f'  - {thread.name}: {thread.is_alive()}')
"

# 2. RAG sistemini test edin
python -c "
from src.knowledge.rag_retriever import RAGRetriever
rag = RAGRetriever()
result = rag.retrieve('test query')
print(f'RAG working: {result is not None}')
"

# 3. Web search test edin
python -c "
from src.research.web_search_utils import search_programming_question
import asyncio
result = asyncio.run(search_programming_question('Python test'))
print(f'Web search working: {len(result) > 0}')
"
```

#### **6. AI Chat UI Donuyor**
```
AI Chat'e mesaj yazdıktan sonra UI donuyor
```

**Çözümler:**
- **Thread-safe processing** aktif mi kontrol edin
- **Background processing** çalışıyor mu kontrol edin
- **Event loop** conflict'i olabilir - uygulamayı yeniden başlatın

```python
# Debug için AI Chat thread durumunu kontrol edin
def debug_ai_chat():
    import threading
    import asyncio
    
    print("🔍 AI Chat Debug Info:")
    print(f"Active threads: {threading.active_count()}")
    print(f"Current thread: {threading.current_thread().name}")
    
    try:
        loop = asyncio.get_event_loop()
        print(f"Event loop running: {loop.is_running()}")
    except RuntimeError:
        print("No event loop in current thread")
```

### 🔧 Debug Komutları

```bash
# Sistem durumu kontrolü
python -c "
import torch
print(f'PyTorch: {torch.__version__}')
print(f'CUDA Available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB')
"

# Flet versiyonu kontrolü
python -c "import flet; print(f'Flet: {flet.__version__}')"

# Transformers kontrolü
python -c "from transformers import AutoTokenizer; print('Transformers OK')"
```

### 📊 Performance Monitoring

```python
# Training sırasında performance monitoring
import time
import psutil
from src.utils.gpu_monitor import GPUMonitor

def monitor_training():
    gpu_monitor = GPUMonitor()
    
    while training_active:
        # System stats
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        
        # GPU stats
        gpu_stats = gpu_monitor.get_gpu_stats()
        
        print(f"CPU: {cpu_percent}% | RAM: {memory.percent}% | GPU: {gpu_stats['memory_percent']}%")
        
        time.sleep(5)
```

---

## 💡 İpuçları ve Püf Noktaları

### 🎯 Performans Optimizasyonu

#### **RTX 3060 için En İyi Ayarlar**
```yaml
# Optimal configuration
training_config:
  batch_size: 1
  gradient_accumulation_steps: 32
  learning_rate: 5e-5
  max_sequence_length: 512
  bf16: true
  gradient_checkpointing: true
  
lora_config:
  r: 16
  alpha: 32
  dropout: 0.1
```

#### **Memory Management**
```python
# Training öncesi memory cleanup
import gc
import torch

def cleanup_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

# Her epoch sonrası cleanup
cleanup_memory()
```

### 🔍 Dataset Hazırlama İpuçları

#### **Kaliteli Dataset Oluşturma**
```python
# İyi örnek
good_example = {
    "text": "def calculate_fibonacci(n):\n    \"\"\"Calculate nth Fibonacci number.\"\"\"\n    if n <= 1:\n        return n\n    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)"
}

# Kötü örnek (çok kısa)
bad_example = {
    "text": "print('hello')"
}
```

#### **Dataset Validation**
```python
from src.data.dataset_manager import DatasetManager

manager = DatasetManager()

# Dataset kalitesi kontrolü
quality_score = manager.validate_dataset("./datasets/conversations/")
print(f"Dataset Quality: {quality_score}/10")

# Öneriler al
suggestions = manager.get_improvement_suggestions()
for suggestion in suggestions:
    print(f"💡 {suggestion}")
```

### 💬 AI Chat İpuçları (YENİ!)

#### **En İyi Soru Sorma Teknikleri**
```
✅ İyi sorular:
- "Android için java programlama dili ile basit bir listview layout dosyası ile birlikte nasıl oluşturulur?"
- "Python'da list comprehension ile çift sayıları filtreleme örneği"
- "JavaScript'te async/await kullanarak API çağrısı nasıl yapılır?"

❌ Belirsiz sorular:
- "Kod yaz"
- "Nasıl yapılır?"
- "Yardım et"
```

#### **AI Chat Performance İpuçları**
```python
# AI Chat yanıt süresini optimize etmek için:

# 1. Spesifik sorular sorun
"Android ListView XML layout + Java adapter kodu"

# 2. Programlama dili belirtin
"Python ile" / "JavaScript'te" / "Java'da"

# 3. Örnek istediğinizi belirtin
"örnek kod ile açıkla" / "detaylı örnek ver"
```

#### **Desteklenen Soru Türleri**
- **🤖 Android**: ListView, RecyclerView, Layout, Activity
- **🐍 Python**: List comprehension, Functions, Classes, Loops
- **🌐 JavaScript**: Async/await, DOM, Arrays, Events
- **☕ Java**: OOP, Collections, Exception handling
- **📱 Mobile**: UI components, Event handling

#### **AI Chat Thread Monitoring**
```python
# AI Chat performance monitoring
def monitor_ai_chat():
    import threading
    import time
    
    start_time = time.time()
    active_threads = threading.active_count()
    
    print(f"🤖 AI Chat Monitoring:")
    print(f"Active threads: {active_threads}")
    print(f"Response time: {time.time() - start_time:.2f}s")
```

### 🚀 Hızlı Geliştirme

#### **Development Workflow**
```bash
# 1. Hızlı test
python -c "from src.training.micro_lora_training import start_micro_training; start_micro_training()"

# 2. AI Chat test
python -c "
from src.ui.ai_chat_interface import AIChatInterface
print('AI Chat system test - OK')
"

# 3. Code formatting
black src/ tests/

# 4. Linting
flake8 src/ tests/

# 5. Tests
pytest tests/ -x  # İlk hatada dur

# 6. Full training
python main.py
```

#### **Custom Training Script**
```python
# custom_training.py
from src.training.starcoder2_trainer import StarCoder2Trainer

def my_custom_training():
    config = {
        "model_name": "bigcode/starcoder2-3b",
        "dataset_path": "./my_dataset/",
        "output_dir": "./my_model/",
        "epochs": 2,
        "batch_size": 1,
        "learning_rate": 1e-4
    }
    
    trainer = StarCoder2Trainer(config)
    result = trainer.train()
    
    print(f"Training completed: {result}")

if __name__ == "__main__":
    my_custom_training()
```

### 📊 Monitoring ve Alerting

#### **Custom Alerts**
```python
# alerts.py
import smtplib
from email.mime.text import MIMEText

def send_training_alert(message):
    """Training tamamlandığında email gönder"""
    msg = MIMEText(f"SeydappAI Training Update: {message}")
    msg['Subject'] = 'Training Alert'
    msg['From'] = 'seydappai@example.com'
    msg['To'] = 'your-email@example.com'
    
    # SMTP server configuration
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.send_message(msg)

# Training callback'inde kullanım
def on_training_complete(result):
    send_training_alert(f"Training completed with loss: {result['final_loss']}")
```

#### **Slack Integration**
```python
# slack_notifier.py
import requests

def notify_slack(message):
    webhook_url = "YOUR_SLACK_WEBHOOK_URL"
    payload = {
        "text": f"🤖 SeydappAI: {message}",
        "username": "SeydappAI Bot"
    }
    requests.post(webhook_url, json=payload)

# Kullanım
notify_slack("Training başlatıldı! 🚀")
```

---

## 🎓 İleri Seviye Kullanım

### 🧠 RAG Integration

```python
from src.knowledge.rag_retriever import RAGRetriever
from src.knowledge.context_builder import ContextBuilder

# RAG sistemi kurulumu
rag = RAGRetriever()
context_builder = ContextBuilder()

# Knowledge base oluşturma
knowledge_base = rag.build_knowledge_base("./datasets/knowledge/")

# Context-aware training
def enhanced_training_with_rag(query):
    # İlgili context'i al
    context = rag.retrieve(query)
    
    # Training data'yı context ile zenginleştir
    enhanced_data = context_builder.enhance_with_context(training_data, context)
    
    # Eğitimi başlat
    return trainer.train(enhanced_data)
```

### 🔄 Continuous Learning

```python
from src.learning.incremental_trainer import IncrementalTrainer

# Sürekli öğrenme sistemi
incremental_trainer = IncrementalTrainer()

# Yeni veri geldiğinde
def on_new_data(new_data):
    # Veri kalitesini değerlendir
    quality_score = incremental_trainer.evaluate_data_quality(new_data)
    
    if quality_score > 0.8:
        # Incremental training başlat
        result = incremental_trainer.incremental_update(new_data)
        print(f"Model updated: {result}")
```

### 🌐 Multi-GPU Training

```python
# multi_gpu_training.py
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel

def setup_distributed_training():
    if torch.cuda.device_count() > 1:
        dist.init_process_group(backend='nccl')
        local_rank = int(os.environ['LOCAL_RANK'])
        torch.cuda.set_device(local_rank)
        
        # Model'i distributed wrapper'a sar
        model = DistributedDataParallel(model, device_ids=[local_rank])
        
    return model

# Çalıştırma
# torchrun --nproc_per_node=2 multi_gpu_training.py
```

---

## 📚 Ek Kaynaklar

### 🔗 Faydalı Linkler
- [StarCoder2 Documentation](https://huggingface.co/bigcode/starcoder2-3b)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [Flet Documentation](https://flet.dev/docs/)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)

### 📖 Önerilen Okumalar
- "Attention Is All You Need" - Transformer paper
- "LoRA: Low-Rank Adaptation of Large Language Models"
- "Parameter-Efficient Transfer Learning for NLP"

### 🎥 Video Tutorials
- Hugging Face Transformers Course
- PyTorch Lightning Tutorials
- LoRA Fine-tuning Guides

---

## 🤝 Topluluk ve Destek

### 💬 İletişim Kanalları
- **GitHub Issues**: Bug reports ve feature requests
- **Discord**: Real-time chat ve destek
- **Email**: contact@seydappai.com

### 🆘 Destek Alma
1. **GitHub Issues**: Teknik problemler için
2. **Documentation**: Bu klavuz ve README
3. **Community**: Discord kanalında soru sorma
4. **Stack Overflow**: `seydappai` tag'i ile

---

<div align="center">

**🎯 Bu klavuz ile SeydappAI ModelTrainer'ı etkili şekilde kullanabilirsiniz!**

**Sorularınız için:** [GitHub Issues](https://github.com/your-username/SeydappAI_ModelTrainer/issues) | [Discord](https://discord.gg/seydappai)

---

*Son güncelleme: 2024*

</div>