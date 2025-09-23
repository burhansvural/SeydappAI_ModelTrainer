```text
src/ui/builder/
├── control_panel/
│   ├── __init__.py                    # Ana import ve factory
│   ├── control_panel_base.py          # Temel sınıf ve konfigürasyon
│   ├── ui_components.py               # UI bileşenleri oluşturma
│   ├── event_handlers.py              # Button click ve event handler'lar  
│   ├── autonomous_manager.py          # Otonom öğrenme sistemi
│   ├── training_coordinator.py        # Training ve memory management
│   ├── progress_monitor.py            # İlerleme takip sistemi
│   └── ui_helpers.py                  # Yardımcı UI fonksiyonları
...
...
...
```

---

# 🎮 Control Panel Sistemi - Detaylı Açıklama Dosyası

## 📋 İçindekiler
1. [Genel Bakış](#genel-bakış)
2. [Dizin Yapısı](#dizin-yapısı)
3. [Dosya Açıklamaları](#dosya-açıklamaları)
4. [Python Sınıf Yapıları](#python-sınıf-yapıları)
5. [Çalışma Şekilleri](#çalışma-şekilleri)
6. [RTX 3060 Optimizasyonları](#rtx-3060-optimizasyonları)
7. [Thread Management](#thread-management)
8. [Error Handling](#error-handling)
9. [Kullanım Kılavuzu](#kullanım-kılavuzu)

## 🔍 Genel Bakış

Bu control panel sistemi, RTX 3060 GPU'su için optimize edilmiş otonom öğrenme ve model eğitimi sistemini yönetir. Python'ın nesne tabanlı programlama (OOP) özelliklerini kullanarak modüler, maintainable ve scalable bir yapı sağlar.

### Sistem Özellikleri:
- **Flet 0.28.3 uyumlu modern UI**
- **RTX 3060 için bellek optimizasyonları**
- **Thread-safe concurrent operations**
- **Memory-aware progress monitoring**
- **Async web scraping ile autonomous learning**
- **Priority-based training queue sistemi**

## 📁 Dizin Yapısı
```text
src/ui/builder/control_panel/
├── init.py # Ana factory ve import orchestrator
├── control_panel_base.py # Temel sınıf, konfigürasyon, state management
├── ui_components.py # Modern Flet UI bileşenleri
├── event_handlers.py # User interaction event management
├── autonomous_manager.py # Otonom öğrenme sistemi koordinatörü
├── training_coordinator.py # RTX 3060 için eğitim koordinasyonu
├── progress_monitor.py # Memory-aware progress tracking
└──  ui_helpers.py # UI utility fonksiyonları
```

---

## 📄 Dosya Açıklamaları

### 🏭 `__init__.py` - Ana Factory
**Amaç**: Tüm bileşenleri orchestrate eden ana factory sınıfı

**İçerik**:
- `ControlPanel` ana sınıfı - composition pattern ile tüm manager'ları bir araya getirir
- `ControlPanelConfig` dataclass'ı - type-safe konfigürasyon
- Clean import interface - client code için basit kullanım

**Python Özellikleri**:
```python
# Composition pattern örneği
class ControlPanel(ControlPanelBase):
    def __init__(self, log_system, dashboard_cards, config=None):
        super().__init__(log_system, dashboard_cards, config)  # Inheritance
        self.ui_builder = UIComponentBuilder()                 # Composition
        self.event_handlers = EventHandlers(self)             # Composition
```

---

### 🎯 control_panel_base.py - Temel Yapı

Amaç: Tüm diğer sınıfların inherit ettiği base class

Python Sınıf Özellikleri:

    Constructor (__init__): Instance initialization

Instance nitelikleri: self.variable ile state management

    Dataclass kullanımı: Type-safe configuration

    Thread-safe operations: Lock mekanizmaları

Önemli Method'lar:
```python
def _load_configuration(self, config: Optional[Dict]) -> ControlPanelConfig:
    """Konfigürasyon yükleme ve doğrulama - defensive programming"""
    
def cleanup_threads(self):
    """Memory-efficient thread cleanup - RTX 3060 için kritik"""
```

---

### 🎨 ui_components.py - UI Bileşenleri

Amaç: Modern Flet UI widget'larını oluşturan factory class

Design Pattern'ler:

    Static Factory Methods: @staticmethod ile utility functions

    Builder Pattern: Complex UI objects'leri step-by-step oluşturma

    Consistent Styling: RTX 3060 tema renkleri

Örnek UI Bileşeni:
```python
@staticmethod
def create_autonomous_button(on_click: Callable) -> ft.Container:
    """
    Ana otonom öğrenme butonu - modern gradient design
    - Purple/Indigo tema (RTX 3060 colors)
    - Shadow effects ile depth
    - Animation support
    """
    return ft.Container(
        content=...,
        gradient=ft.LinearGradient(...),  # Modern gradient
        shadow=ft.BoxShadow(...),         # Depth effect
        animate=ft.Animation(...)         # Smooth transitions
    )
```

---

### ⚡ event_handlers.py - Event Yönetimi

Amaç: Tüm user interaction'ları handle eden event management sistemi

Python Method Türleri:

    Public Methods: Client interface (toggle_autonomous_learning)

    Private Methods: Implementation details (_handle_start_autonomous)

    Error Handling: Comprehensive exception management

Event Flow Örneği:
```python
def toggle_autonomous_learning(self, event):
    """Public interface - user click handler"""
    try:
        with self._event_lock:  # Thread safety
            if self.control_panel.autonomous_running:
                self._handle_stop_autonomous()    # Private implementation
            else:
                self._handle_start_autonomous()   # Private implementation
    except Exception as ex:
        self._handle_event_error("Toggle hatası", str(ex))  # Error handling

```

---

### 🤖 autonomous_manager.py - Otonom Öğrenme

Amaç: Web scraping ve autonomous learning workflow'unu yöneten ana manager

Async Programming Pattern'leri:

    Async/Await: Non-blocking web operations

    asyncio Event Loop: Cooperative multitasking

    Graceful Shutdown: threading.Event ile clean termination

Async Workflow Örneği:
```python
async def _async_learning_worker(self):
    """Ana async öğrenme loop'u"""
    try:
        for topic_index, topic in enumerate(self.current_topics):
            if self._shutdown_event.is_set():  # Graceful shutdown check
                break
            
            # Async research operation
            examples = await self._scraper_instance.research_and_generate_examples(topic)
            
            # Training trigger
            self._trigger_training_for_topic(examples, topic)
            
            await asyncio.sleep(3.0)  # Non-blocking delay
    except asyncio.CancelledError:
        logger.info("🛑 Async worker cancelled")
```

---

### 🎯 training_coordinator.py - Eğitim Koordinasyonu

Amaç: RTX 3060 için memory-aware training queue sistemi

Design Pattern'ler:

    * Priority Queue: queue.PriorityQueue ile öncelikli işlem sırası
    * Global State Management: _training_lock ile single training garantisi
    * Dataclass: Type-safe job representation

RTX 3060 Memory Management:
```python
def _process_training_job(self, job: TrainingJob):
    """RTX 3060 için single-threaded training"""
    global _training_lock, _active_model
    
    with _training_lock:  # Global lock - tek seferde bir eğitim
        try:
            _active_model = job.topic
            self._perform_memory_cleanup()    # Pre-training cleanup
            result = self._execute_training(job.examples, job.topic)
            self._perform_memory_cleanup()    # Post-training cleanup
        finally:
            _active_model = None  # Always release lock

```

---

### 📊 progress_monitor.py - İlerleme Takibi

Amaç: Real-time system monitoring ve memory management

Memory Monitoring Features:

    psutil Integration: System resource monitoring

    Adaptive Sleep: Memory pressure'a göre monitoring frequency

    Emergency Cleanup: Critical memory durumunda agressive cleanup

Memory-Aware Monitoring:
```python
def _monitor_memory_usage(self):
    """RTX 3060 için kritik memory monitoring"""
    memory = psutil.virtual_memory()
    
    if memory.percent > self.memory_critical_threshold:  # %95
        logger.warning(f"🚨 CRITICAL MEMORY: {memory.percent}%")
        self._trigger_emergency_cleanup()  # Agressive cleanup
    elif memory.percent > self.memory_warning_threshold:  # %85
        logger.warning(f"⚠️ HIGH MEMORY: {memory.percent}%")
        self._trigger_memory_cleanup()     # Regular cleanup
```

---

### 🛠️ ui_helpers.py - Utility Fonksiyonları

Amaç: UI operations için reusable utility functions

Static Method Pattern:
```python
class UIHelpers:
    @staticmethod
    def safe_update_text(text_widget: Optional[ft.Text], new_value: str):
        """Thread-safe UI update with null safety"""
        try:
            if text_widget:
                text_widget.value = new_value
                text_widget.update()
        except Exception as e:
            logger.debug(f"UI update error: {e}")  # Silent fail
```

---

### 🐍 Python Sınıf Yapıları
Constructor Pattern (__init__)
```python
def __init__(self, control_panel_instance):
    """
    Python sınıf constructor'ı[1]
    - self parametresi: instance referansı[2]
    - Instance nitelikleri tanımlanır[2]
    - Composition pattern ile dependency injection
    """
    self.control_panel = control_panel_instance  # Composition
    self.is_running = False                      # Instance niteliği[2]
    self._shutdown_event = threading.Event()     # Private nitelik[1]
```
### Method Türleri

    1. Public Methods: Dışarıdan çağrılabilir interface
    2. Private Methods: _underscore ile başlar, internal use
    3. Static Methods: @staticmethod, instance'a ihtiyaç duymaz

### Inheritance vs Composition

    Inheritance: class ControlPanel(ControlPanelBase) - "is-a" relationship
    Composition: self.ui_builder = UIComponentBuilder() - "has-a" relationship

### ⚙️ Çalışma Şekilleri
1. Initialization Flow
```text
1. ControlPanel.__init__()
   ├── ControlPanelBase.__init__()  # Parent constructor
   ├── UIComponentBuilder()         # UI factory
   ├── EventHandlers(self)          # Event management  
   ├── AutonomousManager(self)      # Learning system
   ├── TrainingCoordinator(self)    # Training queue
   └── ProgressMonitor(self)        # System monitoring
```
2. Autonomous Learning Flow
```text
1. User clicks "Otonom Öğrenme" button
2. EventHandlers.toggle_autonomous_learning()
3. AutonomousManager.start_learning()
4. Async worker thread başlar
5. Web scraping ve example generation
6. TrainingCoordinator.queue_training()
7. RTX 3060 memory-aware training
8. ProgressMonitor real-time updates
```
3. Memory Management Flow
```text
1. ProgressMonitor sürekli memory izler
2. %85 RAM usage → Regular cleanup
3. %95 RAM usage → Emergency cleanup
4. Training öncesi/sonrası cleanup
5. Thread cleanup cycles
6. Garbage collection triggers
```

---

### 🎮 RTX 3060 Optimizasyonları
Memory Constraints

    * 12GB VRAM limit: Tek seferde bir model eğitimi
    * Global training lock: _training_lock ile coordination
    * Priority queue: Memory-efficient job scheduling
    * Adaptive monitoring: Memory pressure'a göre frequency

Memory Management Strategies
```python
# Pre-training cleanup
def _perform_memory_cleanup(self):
    from src.models.model_loader import force_gpu_cleanup
    cleanup_success = force_gpu_cleanup()
    
# Emergency cleanup trigger
if memory_percent > 95:
    self._trigger_emergency_cleanup()
    
# Thread cleanup cycles  
def cleanup_threads(self):
    alive_threads = [t for t in self.active_threads if t.is_alive()]
    self.active_threads = alive_threads
    gc.collect()  # Force garbage collection
```
Performance Optimizations

    * Lazy initialization: Scraper sadece ihtiyaç duyulduğunda
    * Batch processing: Multiple examples birlikte işleme
    * Adaptive sleep: System load'a göre timing adjustments
    * Resource pooling: Thread reuse ile memory efficiency

---

## 🧵 Thread Management
Thread Hierarchy
```text
MainThread (UI)
├── AutonomousLearning Worker Thread
├── TrainingCoordinator Thread  
├── ProgressMonitor Thread
└── Individual Training Threads (Sequential)
```
Thread Safety Mechanisms

    * threading.Lock(): Critical sections protection
    * threading.Event(): Graceful shutdown signaling
    * queue.PriorityQueue(): Thread-safe job queue
    * Atomic operations: Single-assignment variables

Graceful Shutdown Pattern
```python
def stop_learning(self):
    self._shutdown_event.set()                    # Signal shutdown
    if self._worker_thread.is_alive():
        self._worker_thread.join(timeout=10.0)    # Wait with timeout
    self._cleanup_after_stop()                    # Resource cleanup
```

---

## 🚨 Error Handling
Error Handling Hierarchy

    1. UI Level: Silent fail with debug logs
    2. Manager Level: Graceful degradation
    3. System Level: Emergency stops and cleanup

Exception Patterns
```python
try:
    # Risky operation
    result = self._execute_training(examples, topic)
except torch.cuda.OutOfMemoryError:
    # RTX 3060 specific error
    logger.error("❌ RTX 3060 OOM!")
    self._handle_oom_error()
except Exception as e:
    # General error handling
    logger.error(f"❌ Training failed: {e}")
    self._handle_training_failure(job, str(e))
finally:
    # Always execute cleanup
    _active_model = None
```
Error Recovery Strategies

    * Fallback UI: Emergency UI when main UI fails
    * Memory cleanup: Automatic cleanup on errors
    * Queue clearing: Remove pending jobs on shutdown
    * State reset: Clean state restoration

---

## 📖 Kullanım Kılavuzu
Basic Usage
```python
# Control panel oluşturma
control_panel = ControlPanel(log_system, dashboard_cards, config)

# UI oluşturma  
control_panel.create_controls(page)

# Control container'ı alma
controls = control_panel.get_controls()
```
Configuration
```python
config = {
    'max_cycles': 10,              # Maksimum öğrenme döngüsü
    'cycle_duration_seconds': 60,  # Döngü süresi
    'research_depth': 'detailed',  # Araştırma derinliği
    'max_threads': 3,              # RTX 3060 için thread limiti
    'cleanup_interval': 30         # Memory cleanup aralığı
}
```
Event Monitoring
```python
# Progress monitoring
progress_info = control_panel.autonomous_manager.get_progress_info()
queue_status = control_panel.training_coordinator.get_queue_status()

# Manual cleanup trigger
control_panel.cleanup_threads()
```

---

## 🔧 Maintenance ve Geliştirme
Adding New Features

    1. Yeni manager class'ı oluştur
    2. __init__.py'a composition olarak ekle
    3. Event handler'larda hook'ları implement et
    4. UI component'lerini ui_components.py'a ekle

Performance Tuning

    * Memory threshold'ları ayarla (progress_monitor.py)
    * Queue size limit'lerini optimize et (training_coordinator.py)
    * Monitoring interval'larını fine-tune et

Debugging

    * Log level'ları ayarla (logging.DEBUG for detailed logs)
    * Memory profiling için psutil metrics kullan
    * Thread health monitoring aktif et

Bu sistem RTX 3060'ın sınırlarını göz önünde bulundurarak, Python'ın OOP özelliklerini
maksimum verimlilikle kullanır ve maintainable, scalable bir architecture sağlar.