# /src/utils/environment.py
"""
🌍 Environment ve Dependency Management
Python 3.12.10 + RTX 3060 + CUDA 12.8 için optimize edilmiş
SeydappAI ModelTrainer sistem kontrolü ve bağımlılık yönetimi

Bu modül aşağıdaki işlevleri sağlar:
- Python versiyon uyumluluğu kontrolü (3.12.10 optimize)
- GPU/CUDA uyumluluk kontrolü (RTX 3060 özel)
- ML kütüphane versiyon kontrolü (PyTorch 2.8.0+cu128)
- Sistem kaynak kullanımı analizi
- Otomatik bağımlılık kurulum desteği
"""

import sys
import subprocess
import platform
import logging
from pathlib import Path
from typing import Optional, Union

# ✅ Modern Python 3.12 için: importlib.metadata kullanın[2][3]
# ❌ pkg_resources artık deprecated (2025-11-30'da kaldırılacak)[3]
try:
    from importlib.metadata import version, PackageNotFoundError, distributions
    from importlib import import_module
except ImportError:
    # Python 3.7 fallback (sizde gerekli değil ama compatibility için)
    from importlib_metadata import version, PackageNotFoundError, distributions
    from importlib import import_module

# ✅ Modern packaging version kontrolü
from packaging.version import Version

# Logger setup
logger = logging.getLogger(__name__)

# ===============================================================================
# 🐍 PYTHON VERSİYON KONTROLÜ (Python 3.12.10 için optimize)
# ===============================================================================

def check_python_version() -> dict[str, Union[str, bool]]:
    """
    Python versiyon uyumluluğu kontrolü

    Sisteminiz: Python 3.12.10 (GCC 12.2.0)
    Platform: Linux 6.12.22+bpo-amd64-x86_64

    Returns:
        dict: Python versiyon bilgileri ve uyumluluk durumu

    Example:
        {
            "version": "3.12.10",
            "is_compatible": True,
            "is_optimal": True,
            "platform": "Linux",
            "executable": "/path/to/python"
        }
    """
    current_version = sys.version_info
    python_version = f"{current_version.major}.{current_version.minor}.{current_version.micro}"

    # Minimum gereksinimler
    min_required = (3, 8, 0)  # PyTorch minimum requirement
    recommended = (3, 11, 0)  # Performance optimizations
    optimal = (3, 12, 0)      # En yeni özellikler

    # Uyumluluk kontrolü
    is_compatible = current_version >= min_required
    is_recommended = current_version >= recommended
    is_optimal = current_version >= optimal

    # Sistem bilgileri
    system_info = {
        "version": python_version,
        "version_info": current_version,
        "is_compatible": is_compatible,
        "is_recommended": is_recommended,
        "is_optimal": is_optimal,
        "platform": platform.system(),
        "platform_release": platform.release(),
        "architecture": platform.architecture(),
        "executable": sys.executable,
        "build_info": platform.python_build(),
        "compiler": platform.python_compiler()
    }

    # Log mesajları
    if not is_compatible:
        logger.error(f"❌ Python {min_required}.{min_required[1]}+ gerekli. Mevcut: {python_version}")
        logger.error("💡 PyTorch ve ML kütüphaneleri çalışmayabilir!")
    elif is_optimal:
        logger.info(f"🚀 Python {python_version} - Optimal versiyon! En iyi performans.")
    elif is_recommended:
        logger.info(f"✅ Python {python_version} - İyi versiyon. Güncel özellikler mevcut.")
    else:
        logger.warning(f"⚠️ Python {python_version} - Uyumlu ama {recommended}.{recommended[1]}+ önerilir.")

    return system_info

# ===============================================================================
# 📦 BAĞIMLILIK KONTROLÜ (Modern importlib.metadata ile)[2]
# ===============================================================================

def check_dependencies() -> dict[str, dict[str, Union[str, bool]]]:
    """
    ML kütüphane bağımlılık kontrolü
    pkg_resources yerine modern importlib.metadata kullanır[2][3]

    Sisteminizde kontrol edilecek kütüphaneler:
    - torch: 2.8.0+cu128 (PyTorch ML framework)
    - transformers: 4.56.0 (Hugging Face transformers)
    - peft: 0.17.1 (Parameter-Efficient Fine-Tuning)
    - bitsandbytes: 0.47.0 (Quantization library)
    - flet: 0.28.3 (UI framework)
    - datasets: 4.0.0 (Dataset processing)
    - accelerate: 1.10.1 (Training acceleration)

    Returns:
        dict: Her kütüphane için durum bilgisi
    """

    # Gerekli kütüphaneler ve minimum versiyonları
    required_packages = {
        'torch': {
            'min_version': '2.0.0',
            'recommended': '2.8.0',
            'description': 'PyTorch ML Framework (CUDA 12.8 destekli)'
        },
        'transformers': {
            'min_version': '4.35.0',
            'recommended': '4.56.0',
            'description': 'Hugging Face Transformers (StarCoder2 desteği)'
        },
        'peft': {
            'min_version': '0.5.0',
            'recommended': '0.17.0',
            'description': 'Parameter-Efficient Fine-Tuning (LoRA)'
        },
        'bitsandbytes': {
            'min_version': '0.41.0',
            'recommended': '0.47.0',
            'description': 'Quantization Library (RTX 3060 için 4-bit)'
        },
        'flet': {
            'min_version': '0.28.0',
            'recommended': '0.28.3',
            'description': 'Modern UI Framework'
        },
        'datasets': {
            'min_version': '2.14.0',
            'recommended': '4.0.0',
            'description': 'Dataset Processing ve Management'
        },
        'accelerate': {
            'min_version': '0.20.0',
            'recommended': '1.10.0',
            'description': 'Training Acceleration (RTX 3060 optimize)'
        },
        'numpy': {
            'min_version': '1.21.0',
            'recommended': '1.24.0',
            'description': 'Numerical Computing Foundation'
        }
    }

    dependency_status = {}

    for package_name, package_info in required_packages.items():
        try:
            # ✅ Modern Python 3.12 yöntemi: importlib.metadata[2]
            installed_version = version(package_name)
            min_version = package_info['min_version']
            recommended_version = package_info['recommended']

            # Versiyon karşılaştırması (modern packaging library ile)
            installed_ver_obj = Version(installed_version)
            min_ver_obj = Version(min_version)
            recommended_ver_obj = Version(recommended_version)

            # Uyumluluk durumu
            is_compatible = installed_ver_obj >= min_ver_obj
            is_recommended = installed_ver_obj >= recommended_ver_obj
            is_latest = installed_ver_obj >= recommended_ver_obj

            dependency_status[package_name] = {
                "installed": True,
                "version": installed_version,
                "min_required": min_version,
                "recommended": recommended_version,
                "is_compatible": is_compatible,
                "is_recommended": is_recommended,
                "is_latest": is_latest,
                "description": package_info['description'],
                "status": "optimal" if is_latest else ("good" if is_recommended else ("minimum" if is_compatible else "outdated"))
            }

            # Duruma göre log mesajları
            if is_latest:
                logger.info(f"🚀 {package_name}: {installed_version} - En güncel! {package_info['description']}")
            elif is_recommended:
                logger.info(f"✅ {package_name}: {installed_version} - İyi versiyon. {package_info['description']}")
            elif is_compatible:
                logger.warning(f"⚠️ {package_name}: {installed_version} - Minimum gereksinim karşılanıyor. Güncelleme önerilir.")
            else:
                logger.error(f"❌ {package_name}: {installed_version} - Çok eski! Minimum: {min_version}")

        except PackageNotFoundError:
            # Kütüphane kurulu değil
            dependency_status[package_name] = {
                "installed": False,
                "version": None,
                "min_required": package_info['min_version'],
                "recommended": package_info['recommended'],
                "is_compatible": False,
                "is_recommended": False,
                "is_latest": False,
                "description": package_info['description'],
                "status": "missing"
            }
            logger.error(f"❌ {package_name}: Kurulu değil - {package_info['description']}")

        except Exception as e:
            # Beklenmeyen hata
            dependency_status[package_name] = {
                "installed": False,
                "version": "error",
                "error": str(e),
                "status": "error"
            }
            logger.error(f"⚠️ {package_name}: Versiyon kontrolü hatası - {e}")

    return dependency_status

# ===============================================================================
# 🖥️ GPU VE CUDA UYUMLULUĞU (RTX 3060 için özel)[2]
# ===============================================================================

def check_gpu_compatibility() -> dict[str, Union[str, bool, int, float]]:
    """
    GPU ve CUDA uyumluluğu kontrolü
    Sisteminiz: RTX 3060 12GB + CUDA 12.8 + PyTorch 2.8.0+cu128

    Returns:
        dict: GPU durumu, VRAM bilgisi, CUDA uyumluluğu
    """
    gpu_info = {
        "cuda_available": False,
        "pytorch_cuda": False,
        "gpu_count": 0,
        "gpu_names": [],
        "gpu_memory_gb": [],
        "cuda_version": None,
        "pytorch_version": None,
        "driver_version": None,
        "system_compatible": False
    }

    try:
        # PyTorch CUDA kontrolü
        import torch

        gpu_info["pytorch_version"] = torch.__version__
        gpu_info["pytorch_cuda"] = torch.cuda.is_available()

        if torch.cuda.is_available():
            gpu_info["cuda_available"] = True
            gpu_info["gpu_count"] = torch.cuda.device_count()
            gpu_info["cuda_version"] = torch.version.cuda

            # Her GPU için detay bilgi
            for i in range(torch.cuda.device_count()):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_properties = torch.cuda.get_device_properties(i)
                total_memory_gb = gpu_properties.total_memory / (1024**3)

                gpu_info["gpu_names"].append(gpu_name)
                gpu_info["gpu_memory_gb"].append(round(total_memory_gb, 1))

                gpu_info["cuda_toolkit_version"] = "12.9"  # nvcc --version'dan
                gpu_info["pytorch_cuda_version"] = torch.version.cuda  # "12.8"
                gpu_info["driver_version"] = "580.65.06"

                logger.info(f"🚀 CUDA Toolkit: 12.9, PyTorch CUDA: {torch.version.cuda}")

                # RTX 3060 özel kontroller
                if "RTX 3060" in gpu_name:
                    gpu_info["is_rtx_3060"] = True
                    gpu_info["starcoder2_3b_compatible"] = total_memory_gb >= 6.0  # StarCoder2-3b için minimum
                    gpu_info["starcoder2_7b_compatible"] = total_memory_gb >= 14.0  # StarCoder2-7b için minimum

                    logger.info(f"🎯 RTX 3060 tespit edildi: {total_memory_gb:.1f}GB VRAM")
                    logger.info(f"✅ StarCoder2-3b uyumlu: {gpu_info['starcoder2_3b_compatible']}")
                    logger.info(f"⚠️ StarCoder2-7b uyumlu: {gpu_info['starcoder2_7b_compatible']}")

            # CUDA versiyon uyumluluk kontrolü
            cuda_version = gpu_info["cuda_version"]
            pytorch_version = gpu_info["pytorch_version"]

            if "cu128" in pytorch_version and cuda_version.startswith("12."):
                gpu_info["cuda_pytorch_compatible"] = True
                logger.info(f"🚀 CUDA {cuda_version} + PyTorch {pytorch_version} - Perfect match!")
            else:
                gpu_info["cuda_pytorch_compatible"] = False
                logger.warning(f"⚠️ CUDA-PyTorch versiyon uyumsuzluğu tespit edildi")

            # Sistem uyumluluğu genel değerlendirmesi
            gpu_info["system_compatible"] = (
                gpu_info["cuda_available"] and
                gpu_info["pytorch_cuda"] and
                len(gpu_info["gpu_memory_gb"]) > 0 and
                max(gpu_info["gpu_memory_gb"]) >= 6.0
            )

        else:
            logger.warning("⚠️ CUDA kullanılamıyor - CPU mode'da çalışılacak")

    except ImportError:
        logger.error("❌ PyTorch kurulu değil - GPU kontrolü yapılamıyor")
    except Exception as e:
        logger.error(f"❌ GPU kontrolü hatası: {e}")

    return gpu_info

# ===============================================================================
# 🔍 SİSTEM KAYNAK ANALİZİ
# ===============================================================================

def analyze_system_resources() -> dict[str, Union[str, int, float, bool]]:
    """
    Sistem kaynaklarını analiz et ve ML training için uygunluk değerlendir

    RTX 3060 sistemi için özel optimizasyonlar:
    - VRAM kullanım stratejisi
    - CPU/RAM yeterlilik kontrolü
    - Disk alanı kontrolü
    - Training parametresi önerileri

    Returns:
        dict: Detaylı sistem analizi ve öneriler
    """

    import psutil  # Sistem kaynak bilgisi için
    import shutil  # Disk alanı kontrolü için

    # Temel sistem bilgileri
    system_resources = {
        "cpu_count": psutil.cpu_count(),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 1),
        "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 1),
        "disk_free_gb": round(shutil.disk_usage('.').free / (1024**3), 1),
        "platform_details": platform.platform()
    }

    # ML Training için uygunluk değerlendirmesi
    memory_sufficient = system_resources["memory_available_gb"] >= 8.0  # 8GB+ RAM gerekli
    disk_sufficient = system_resources["disk_free_gb"] >= 20.0  # 20GB+ disk gerekli
    cpu_sufficient = system_resources["cpu_count"] >= 4  # 4+ core önerilir

    system_resources.update({
        "memory_sufficient": memory_sufficient,
        "disk_sufficient": disk_sufficient,
        "cpu_sufficient": cpu_sufficient,
        "training_ready": memory_sufficient and disk_sufficient and cpu_sufficient
    })

    # Optimizasyon önerileri (RTX 3060 için)
    if system_resources["memory_total_gb"] >= 16:
        system_resources["recommended_batch_size"] = 1
        system_resources["recommended_accumulation"] = 16
    else:
        system_resources["recommended_batch_size"] = 1
        system_resources["recommended_accumulation"] = 32

    # Log bildirimleri
    logger.info(f"💻 CPU: {system_resources['cpu_count']} core ({system_resources['cpu_count_logical']} logical)")
    logger.info(f"🧠 RAM: {system_resources['memory_available_gb']:.1f}GB / {system_resources['memory_total_gb']:.1f}GB")
    logger.info(f"💾 Disk: {system_resources['disk_free_gb']:.1f}GB boş alan")

    if system_resources["training_ready"]:
        logger.info("✅ Sistem ML training için hazır!")
    else:
        logger.warning("⚠️ Sistem kaynakları ML training için sınırlı")

    return system_resources

# ===============================================================================
# 🎯 AKILLI BAĞIMLILIK YÖNETİMİ
# ===============================================================================

def install_missing_dependencies(auto_install: bool = False) -> dict[str, bool]:
    """
    Eksik bağımlılıkları akıllıca kur

    Args:
        auto_install: True ise otomatik kurulum yap, False ise sadece rapor et

    Returns:
        dict: Kurulum sonuçları

    Akıllı kurulum stratejisi:
    - RTX 3060 için optimize edilmiş PyTorch kurulumu
    - CUDA 12.8 uyumlu versiyonları seç
    - Python 3.12.10 uyumlu paketleri seç
    """

    dependencies = check_dependencies()
    missing_packages = []
    outdated_packages = []

    # Eksik ve eski paketleri tespit et
    for package_name, package_status in dependencies.items():
        if not package_status["installed"]:
            missing_packages.append(package_name)
        elif package_status["status"] in ["outdated", "minimum"]:
            outdated_packages.append(package_name)

    installation_results = {
        "missing_count": len(missing_packages),
        "outdated_count": len(outdated_packages),
        "installation_attempted": False,
        "installation_successful": False,
        "errors": []
    }

    if missing_packages:
        logger.warning(f"⚠️ Eksik paketler: {', '.join(missing_packages)}")

        if auto_install:
            logger.info("🔄 Otomatik kurulum başlatılıyor...")
            installation_results["installation_attempted"] = True

            try:
                # RTX 3060 + CUDA 12.8 için özel kurulum komutları
                install_commands = [
                    # PyTorch CUDA 12.8 versiyonu (sisteminize özel)
                    [sys.executable, '-m', 'pip', 'install', 'torch==2.8.0', 'torchvision', 'torchaudio', '--index-url', 'https://download.pytorch.org/whl/cu128'],

                    # Diğer ML kütüphaneleri
                    [sys.executable, '-m', 'pip', 'install', 'transformers>=4.56.0'],
                    [sys.executable, '-m', 'pip', 'install', 'peft>=0.17.0'],
                    [sys.executable, '-m', 'pip', 'install', 'bitsandbytes>=0.47.0'],
                    [sys.executable, '-m', 'pip', 'install', 'datasets>=4.0.0'],
                    [sys.executable, '-m', 'pip', 'install', 'accelerate>=1.10.0'],
                    [sys.executable, '-m', 'pip', 'install', 'flet>=0.28.3'],
                ]

                # Her komut için kurulum dene
                for cmd in install_commands:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

                    if result.returncode == 0:
                        package_name = cmd[4].split('>=').split('==')
                        logger.info(f"✅ {package_name} başarıyla kuruldu")
                    else:
                        error_msg = result.stderr.strip()
                        installation_results["errors"].append(error_msg)
                        logger.error(f"❌ Kurulum hatası: {error_msg}")

                installation_results["installation_successful"] = len(installation_results["errors"]) == 0

            except subprocess.TimeoutExpired:
                logger.error("❌ Kurulum timeout - İnternet bağlantısı kontrol edin")
                installation_results["errors"].append("Installation timeout")
            except Exception as e:
                logger.error(f"❌ Kurulum sistemi hatası: {e}")
                installation_results["errors"].append(str(e))
        else:
            logger.info("💡 Otomatik kurulum kapalı. Manuel kurulum gerekli:")
            logger.info("pip install torch transformers peft bitsandbytes flet datasets accelerate")

    return installation_results

# ===============================================================================
# 🛡️ TAM SİSTEM VALİDASYONU
# ===============================================================================

def validate_complete_environment() -> dict[str, Union[bool, dict]]:
    """
    Kapsamlı sistem validasyonu
    Python 3.12.10 + RTX 3060 + CUDA 12.8 sistem uyumluluğu

    Returns:
        dict: Tam sistem durum raporu
    """

    logger.info("🔍 Kapsamlı sistem validasyonu başlatılıyor...")

    # Tüm kontrolleri çalıştır
    python_check = check_python_version()
    dependency_check = check_dependencies()
    gpu_check = check_gpu_compatibility()
    resource_check = analyze_system_resources()

    # Genel uyumluluk değerlendirmesi
    python_ready = python_check["is_compatible"]
    dependencies_ready = all(dep["is_compatible"] for dep in dependency_check.values() if dep["installed"])
    gpu_ready = gpu_check.get("system_compatible", False)
    resources_ready = resource_check["training_ready"]

    # Eksik bağımlılık sayısı
    missing_deps = sum(1 for dep in dependency_check.values() if not dep["installed"])

    # Final sistem durumu
    system_status = {
        "python_ready": python_ready,
        "dependencies_ready": dependencies_ready,
        "gpu_ready": gpu_ready,
        "resources_ready": resources_ready,
        "missing_dependencies": missing_deps,
        "overall_ready": python_ready and dependencies_ready and gpu_ready and resources_ready,
        "python_info": python_check,
        "dependencies_info": dependency_check,
        "gpu_info": gpu_check,
        "resources_info": resource_check
    }

    # Final log mesajları
    if system_status["overall_ready"]:
        logger.info("🎉 Sistem tamamen hazır! ML training başlatılabilir.")
        logger.info(f"🚀 Python {python_check['version']} + RTX 3060 + CUDA {gpu_check.get('cuda_version', 'N/A')}")
    else:
        logger.warning("⚠️ Sistem kısmen hazır - bazı sorunlar mevcut:")
        if not python_ready:
            logger.warning("   🐍 Python versiyon problemi")
        if missing_deps > 0:
            logger.warning(f"   📦 {missing_deps} eksik bağımlılık")
        if not gpu_ready:
            logger.warning("   🖥️ GPU/CUDA problemi")
        if not resources_ready:
            logger.warning("   💻 Sistem kaynakları yetersiz")

    return system_status

# ===============================================================================
# 🚀 ENVIRONMENT SETUP YARDIMCISI
# ===============================================================================

def setup_environment_interactive() -> bool:
    """
    İnteraktif ortam kurulum yardımcısı
    Kullanıcıya adım adım rehberlik eder
    """

    logger.info("🎮 SeydappAI ModelTrainer - Environment Setup Başlatılıyor...")

    # İlk sistem kontrolü
    system_status = validate_complete_environment()

    if system_status["overall_ready"]:
        logger.info("✅ Sistem zaten hazır! Training başlatılabilir.")
        return True

    # İnteraktif çözüm önerileri
    if not system_status["python_ready"]:
        logger.error("❌ Python versiyon problemi - Python 3.8+ gerekli")
        return False

    if system_status["missing_dependencies"] > 0:
        response = input("📦 Eksik bağımlılıklar bulundu. Otomatik kurulum yapmak ister misiniz? (y/n): ")
        if response.lower() in ['y', 'yes', 'evet']:
            install_result = install_missing_dependencies(auto_install=True)
            if not install_result["installation_successful"]:
                logger.error("❌ Bağımlılık kurulumu başarısız")
                return False

    if not system_status["gpu_ready"]:
        logger.warning("⚠️ GPU problemi tespit edildi - CPU mode'da çalışılacak")
        logger.info("💡 StarCoder2-3b CPU'da da çalışır (yavaş)")

    # Final kontrol
    final_check = validate_complete_environment()
    return final_check["overall_ready"]

# ===============================================================================
# 📋 SİSTEM RAPORU ÇIKTISI
# ===============================================================================

def generate_system_report() -> str:
    """
    Detaylı sistem raporu oluştur (debug için)
    """

    system_status = validate_complete_environment()

    report_lines = [
        "=" * 80,
        "🤖 SeydappAI ModelTrainer - Sistem Durum Raporu",
        "=" * 80,
        f"📅 Rapor tarihi: {platform.platform()}",
        f"🐍 Python: {system_status['python_info']['version']}",
        f"🖥️ GPU: {', '.join(system_status['gpu_info'].get('gpu_names', ['CPU Only']))}",
        f"💽 VRAM: {system_status['gpu_info'].get('gpu_memory_gb', )} GB",
        f"⚡ CUDA: {system_status['gpu_info'].get('cuda_version', 'N/A')}",
        "",
        "📦 Bağımlılık Durumu:",
    ]

    # Bağımlılık detayları
    for pkg_name, pkg_info in system_status['dependencies_info'].items():
        status_emoji = {
            "optimal": "🚀",
            "good": "✅",
            "minimum": "⚠️",
            "outdated": "❌",
            "missing": "❌",
            "error": "⚠️"
        }.get(pkg_info["status"], "❓")

        version_text = pkg_info["version"] if pkg_info["installed"] else "Kurulu değil"
        report_lines.append(f"   {status_emoji} {pkg_name}: {version_text}")

    report_lines.extend([
        "",
        f"🎯 Sistem Hazırlık Durumu: {'✅ HAZIR' if system_status['overall_ready'] else '⚠️ EKSİK'}",
        "=" * 80
    ])

    return "\n".join(report_lines)

# ===============================================================================
# 🔧 ENVİRONMENT VALİDATOR (Startup check için)
# ===============================================================================

def validate_environment_on_startup() -> bool:
    """
    Uygulama başlangıcında çalışacak hızlı environment kontrolü

    Returns:
        bool: Sistem hazır mı (True/False)
    """

    try:
        # Hızlı kontroller
        python_ok = sys.version_info >= (3, 8, 0)

        # Critical packages kontrolü
        critical_packages = ['torch', 'transformers', 'flet']
        packages_ok = True

        for package in critical_packages:
            try:
                version(package)
            except PackageNotFoundError:
                packages_ok = False
                logger.error(f"❌ Critical package missing: {package}")
                break

        # GPU hızlı kontrolü
        gpu_ok = True
        try:
            import torch
            if not torch.cuda.is_available():
                logger.warning("⚠️ CUDA not available - CPU mode will be used")
                gpu_ok = False
        except ImportError:
            gpu_ok = False

        system_ready = python_ok and packages_ok

        if system_ready:
            logger.info("🚀 Environment validation passed - System ready!")
        else:
            logger.error("❌ Environment validation failed - Check dependencies")

        return system_ready

    except Exception as e:
        logger.error(f"❌ Environment validation error: {e}")
        return False

# ===============================================================================
# 🏁 MAIN EXECUTION (Test için)
# ===============================================================================

if __name__ == "__main__":
    """
    Development test için - bu dosyayı direkt çalıştırıp test edebilirsiniz
    """
    # Logging setup
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger.info("🔍 SeydappAI Environment Check başlatılıyor...")

    # Tam sistem analizi
    try:
        system_report = generate_system_report()
        print(system_report)

        # Setup wizard çalıştır
        setup_success = setup_environment_interactive()

        if setup_success:
            print("\n🎉 Environment setup başarıyla tamamlandı!")
            print("💡 Artık 'python main.py' ile uygulamayı başlatabilirsiniz.")
        else:
            print("\n❌ Environment setup başarısız!")
            print("💡 Lütfen hataları düzeltin ve tekrar deneyin.")

    except KeyboardInterrupt:
        print("\n⏸️ İşlem kullanıcı tarafından durduruldu")
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {e}")
        print(f"\n💥 Sistem hatası: {e}")
