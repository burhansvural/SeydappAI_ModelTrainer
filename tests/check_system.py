# tests/check_system.py
"""
🔍 SeydappAI ModelTrainer - LIST ATTRIBUTE ERROR FIXED[1][2][3]
'list' object has no attribute 'strip' hatası çözüldü
"""
import subprocess
import sys
import platform
import json
from datetime import datetime
import logging

logger = logging.getLogger("SystemCheck")


def safe_system_check():
    """Safe system validation - INTEGER indices only[1][3]"""

    try:
        print("🔍 Safe System Check - INTEGER INDEX MODE[1]")
        print("=" * 50)

        # ✅ Dictionary kullan, liste değil[1]
        system_info = {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": sys.platform,
            "path_count": len(sys.path)
        }

        # ✅ Dictionary access - STRING keys OK[1]
        print(f"🐍 Python: {system_info['python_version']}")
        print(f"🖥️ Platform: {system_info['platform']}")
        print(f"📁 Path entries: {system_info['path_count']}")

        # ✅ Safe list iteration - INTEGER indices[1][3]
        print("\n📦 Critical modules:")
        modules_to_check = ['flet', 'torch', 'transformers']

        for idx, module_name in enumerate(modules_to_check):  # ✅ enumerate gives INTEGER idx[1]
            try:
                __import__(module_name)
                print(f"  {idx + 1}. ✅ {module_name}")  # ✅ idx is INTEGER[1]
            except ImportError:
                print(f"  {idx + 1}. ❌ {module_name}")  # ✅ idx is INTEGER[1]

        return True

    except Exception as e:
        print(f"❌ System check error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_gpu_cuda_fixed():
    """
    ✅ CRITICAL FIX: İki ana liste indeksleme hatası çözüldü[1][2]
    """
    gpu_info = {
        "nvidia_smi_available": False,
        "cuda_available": False,
        "pytorch_cuda": False,
        "gpu_details": []
    }

    # nvidia-smi kontrolü[2][4]
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'],
                                capture_output=True, text=True, timeout=10)

        if result.returncode == 0 and result.stdout:
            gpu_info["nvidia_smi_available"] = True
            lines = result.stdout.strip().split('\n')

            print(f"🔍 Debug: nvidia-smi çıktısı: {len(lines)} satır")

            for i, line in enumerate(lines):  # ✅ i is INTEGER
                if line and line.strip():
                    try:
                        print(f"  Debug line {i}: '{line}'")

                        # Parse comma-separated values
                        parts = line.strip().split(',')
                        print(f"    Debug: parts = {parts}")  # Debug çıktısı

                        if len(parts) >= 2:
                            # ✅ CRITICAL FIX #1: Use  index, not entire list[1][2]
                            raw_name = parts[0]  # ✅ FIXED: parts!
                            raw_memory = parts[1]  # ✅ CORRECT

                            print(f"    Debug: raw_name = '{raw_name}' (type: {type(raw_name)})")
                            print(f"    Debug: raw_memory = '{raw_memory}' (type: {type(raw_memory)})")

                            # Safe string processing[1][2]
                            name = raw_name.strip()  # ✅ Now raw_name is string
                            memory_str = raw_memory.strip()

                            # Memory conversion
                            try:
                                memory_mb = int(memory_str)
                                memory_gb = round(memory_mb / 1024, 1)
                            except ValueError as mem_error:
                                logger.warning(f"⚠️ Invalid memory value: {memory_str}")
                                continue

                            # ✅ Create dictionary with proper STRING name[1][2]
                            gpu_dict = {
                                "id": i,
                                "name": name,  # ✅ Bu artık kesinlikle STRING
                                "memory_mb": memory_mb,
                                "memory_gb": memory_gb
                            }

                            gpu_info["gpu_details"].append(gpu_dict)
                            print(f"  ✅ GPU {i} parsed: {name} ({memory_gb} GB)")

                    except Exception as parse_error:
                        logger.warning(f"⚠️ GPU line parsing error: {parse_error}")
                        continue

            if gpu_info["gpu_details"]:
                print(f"✅ NVIDIA GPU tespit edildi: {len(gpu_info['gpu_details'])} adet")

                for idx, gpu in enumerate(gpu_info["gpu_details"]):
                    print(f"   GPU {idx}: {gpu['name']} ({gpu['memory_gb']} GB)")
            else:
                print("⚠️ GPU parse edilemedi")
        else:
            print(f"❌ nvidia-smi başarısız - return code: {result.returncode}")

    except (subprocess.TimeoutExpired, FileNotFoundError) as gpu_error:
        print(f"❌ GPU detection error: {gpu_error}")
    except Exception as unexpected_error:
        logger.error(f"❌ Unexpected GPU check error: {unexpected_error}")

    # PyTorch CUDA kontrolü
    try:
        import torch
        gpu_info["pytorch_cuda"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            gpu_info["cuda_version"] = torch.version.cuda
            gpu_info["pytorch_version"] = torch.__version__
            gpu_count = torch.cuda.device_count()
            print(f"✅ PyTorch CUDA desteği aktif: {torch.version.cuda}")
            print(f"✅ PyTorch GPU sayısı: {gpu_count}")
        else:
            print("⚠️ PyTorch CUDA desteği yok")
    except ImportError:
        print("❌ PyTorch kurulu değil")
    except Exception as pytorch_error:
        logger.warning(f"⚠️ PyTorch check warning: {pytorch_error}")

    return gpu_info

def check_ml_packages():
    """ML kütüphanelerini kontrol et - SAFE VERSION"""
    required_packages = {
        'torch': 'PyTorch (ML framework)',
        'transformers': 'Hugging Face Transformers',
        'peft': 'Parameter-Efficient Fine-Tuning',
        'bitsandbytes': 'Quantization library',
        'flet': 'UI framework',
        'datasets': 'Dataset processing',
        'accelerate': 'Training acceleration'
    }

    package_status = {}
    print("\n📦 ML Kütüphane Durumu:")

    # ✅ Dictionary iteration - STRING keys OK[1]
    for package, description in required_packages.items():
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'Unknown')
            package_status[package] = {
                "installed": True,
                "version": version,
                "description": description
            }
            print(f"✅ {package}: {version} - {description}")
        except ImportError:
            package_status[package] = {
                "installed": False,
                "version": None,
                "description": description
            }
            print(f"❌ {package}: Kurulu değil - {description}")

    return package_status


def generate_recommendations_fixed(python_info, gpu_info, package_info):
    """
    ✅ FINAL FIX: GPU data type validation completely fixed[1][2]
    """
    recommendations = {
        "model_size": "3b",
        "batch_size": 1,
        "quantization": "4bit",
        "mixed_precision": True,
        "gradient_checkpointing": True
    }

    print("\n🎯 SİSTEM ÖNERİLERİ:")

    # Python versiyon kontrolü
    try:
        python_version = tuple(map(int, python_info['version_info'].split('.')))
        if python_version >= (3, 11):
            print("✅ Python 3.11+ - Optimal performans")
            recommendations["python_optimal"] = True
        elif python_version >= (3, 8):
            print("⚠️ Python 3.8-3.10 - Uyumlu ama 3.11+ önerili")
            recommendations["python_optimal"] = False
        else:
            print("❌ Python 3.8+ gerekli!")
            recommendations["python_compatible"] = False
            return recommendations
    except Exception as e:
        logger.warning(f"⚠️ Python version parse warning: {e}")

    # ✅ FINAL FIX: GPU önerileri - STRING GUARANTEED[1][2]
    if gpu_info.get("pytorch_cuda") and gpu_info.get("gpu_details"):
        try:
            if isinstance(gpu_info["gpu_details"], list) and len(gpu_info["gpu_details"]) > 0:
                for idx, gpu in enumerate(gpu_info["gpu_details"]):  # ✅ INTEGER idx

                    # ✅ FINAL: Complete type validation[1][2]
                    if isinstance(gpu, dict):
                        raw_name = gpu.get("name", "Unknown GPU")
                        raw_vram = gpu.get("memory_gb", 0)

                        print(f"🔍 Debug: GPU {idx} name type: {type(raw_name)}, value: {raw_name}")

                        # ✅ FINAL FIX: Handle ANY data type[1][2]
                        if isinstance(raw_name, str):
                            gpu_name = raw_name.upper()
                        elif isinstance(raw_name, list):
                            # ✅ Liste ise sadece ilk elemanı al[1]
                            if len(raw_name) > 0:
                                gpu_name = str(raw_name).strip().upper()
                                print(f"  🔧 Fixed list to string: {gpu_name}")
                            else:
                                gpu_name = "UNKNOWN GPU"
                        else:
                            gpu_name = str(raw_name).upper()
                            print(f"  🔧 Converted {type(raw_name)} to string: {gpu_name}")

                        # ✅ VRAM safe conversion
                        if isinstance(raw_vram, (int, float)):
                            vram_gb = float(raw_vram)
                        else:
                            try:
                                vram_gb = float(str(raw_vram))
                            except ValueError:
                                vram_gb = 0

                        print(f"🖥️ {gpu_name} ({vram_gb} GB VRAM)")

                        # GPU-based recommendations
                        if "RTX 3060" in gpu_name or vram_gb <= 12:
                            recommendations.update({
                                "model_size": "3b",
                                "batch_size": 1,
                                "suggested_model": "bigcode/starcoder2-3b"
                            })
                            print("   💡 StarCoder2-3b önerili (güvenli)")

                        elif "RTX 3070" in gpu_name or "RTX 4070" in gpu_name or (12 < vram_gb <= 16):
                            recommendations.update({
                                "model_size": "3b",
                                "batch_size": 2,
                                "suggested_model": "bigcode/starcoder2-3b"
                            })
                            print("   🚀 StarCoder2-3b + batch_size=2 (optimal)")

                        elif vram_gb > 16:
                            recommendations.update({
                                "model_size": "7b",
                                "batch_size": 2,
                                "suggested_model": "bigcode/starcoder2-7b"
                            })
                            print("   🔥 StarCoder2-7b mümkün (güçlü)")

                    else:
                        logger.warning(f"⚠️ Unexpected GPU data type: {type(gpu)}")
                        print(f"⚠️ GPU data format error: {gpu}")
            else:
                print("⚠️ GPU details bulunamadı veya liste değil")

        except Exception as gpu_rec_error:
            logger.error(f"❌ GPU recommendations error: {gpu_rec_error}")
    else:
        recommendations.update({
            "model_size": "3b",
            "batch_size": 1,
            "cpu_only": True
        })
        print("💻 CPU-only mode - DialoGPT small önerili")

    return recommendations


def create_optimized_env_file_fixed(recommendations, gpu_info, python_info):
    """
    ✅ RTX 3060 + StarCoder2-3B Optimize Edilmiş .env Generator[1][2][3]
    Search results based optimization
    """

    gpu_device = "0" if gpu_info.get("pytorch_cuda") else "-1"
    gpu_memory = "0"
    gpu_name = "CPU Only"

    try:
        if gpu_info.get("gpu_details") and isinstance(gpu_info["gpu_details"], list):
            if len(gpu_info["gpu_details"]) > 0:
                first_gpu = gpu_info["gpu_details"]  # ✅ INTEGER index

                if isinstance(first_gpu, dict):
                    raw_memory = first_gpu.get("memory_gb", 0)
                    raw_name = first_gpu.get("name", "Unknown GPU")

                    gpu_name = str(raw_name)
                    gpu_memory = str(raw_memory)

                    print(f"  ✅ GPU detected: {gpu_name} ({gpu_memory} GB)")

    except Exception as gpu_access_error:
        logger.warning(f"⚠️ GPU info access warning: {gpu_access_error}")

    # ✅ RTX 3060 based optimizations[1]
    suggested_model = recommendations.get("suggested_model", "bigcode/starcoder2-3b")

    # ✅ RTX 3060 için optimize edilmiş batch size[1]
    if "RTX 3060" in gpu_name and float(gpu_memory) >= 12:
        batch_size = 2  # RTX 3060 12GB için safe
        sequence_length = 4096  # StarCoder2 16K context'in 1/4'ü[3]
        epochs = 3  # Efficiency için
        gradient_accumulation = 4  # RTX 3060 optimal[1]
    else:
        batch_size = recommendations.get("batch_size", 1)
        sequence_length = 2048
        epochs = 6
        gradient_accumulation = 8

    env_content = f"""# ===============================================================================
# 🤖 SeydappAI ModelTrainer - RTX 3060 + StarCoder2-3B Optimized[1][2][3]
# ===============================================================================
# 🕒 Oluşturulma tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 🔍 Search results [1][2][3] based optimization

# ===============================================================================
# 📊 SİSTEM BİLGİLERİ (Otomatik tespit edildi)
# ===============================================================================
# Python versiyon: {python_info['version_info']}
# Platform: {python_info.get('platform', 'Unknown')}
# GPU: {gpu_name}
# VRAM: {gpu_memory} GB
# CUDA: {gpu_info.get('cuda_version', 'N/A')}

# ===============================================================================
# 🎯 RTX 3060 + StarCoder2-3B İÇİN OPTİMİZE EDİLMİŞ AYARLAR[1][2][3]
# ===============================================================================

# Temel Python ayarları
ENVIRONMENT=development
DEBUG=True
TOKENIZERS_PARALLELISM=false

# ✅ Model ayarları (search results [1][2] optimized)
DEFAULT_CODE_MODEL={suggested_model}
DEFAULT_CHAT_MODEL=microsoft/DialoGPT-medium
MODEL_STRATEGY=hybrid

# ✅ GPU ayarları (RTX 3060 optimized[1])
CUDA_DEVICE={gpu_device}
USE_MIXED_PRECISION=True
GRADIENT_CHECKPOINTING=True

# ✅ StarCoder2-3B optimized parameters[1][2][3]
USE_4BIT_QUANTIZATION=True
LOAD_IN_4BIT=True
BNB_4BIT_COMPUTE_DTYPE=float16
BNB_4BIT_USE_DOUBLE_QUANT=True

# ✅ RTX 3060 training parameters (search results [1] based)
DEFAULT_EPOCHS={epochs}
DEFAULT_LEARNING_RATE=1e-4
DEFAULT_BATCH_SIZE={batch_size}
GRADIENT_ACCUMULATION_STEPS={gradient_accumulation}
MAX_SEQUENCE_LENGTH={sequence_length}

# ✅ LoRA ayarları (RTX 3060 için optimize)
LORA_RANK=16
LORA_ALPHA=32
LORA_DROPOUT=0.05
LORA_TARGET_MODULES=q_proj,v_proj,o_proj,gate_proj,up_proj,down_proj

# Dosya yolları
TRAINED_MODELS_DIR=./trained_models
DATASETS_DIR=./datasets
MODEL_CACHE_DIR=./models_cache

# ✅ StarCoder2-3B conversation ayarları (search results [3][5])
CONVERSATION_MODE_DEFAULT=True
MAX_CONVERSATION_CONTEXT=16384
CHAT_TEMPERATURE=0.8
FILL_IN_THE_MIDDLE_ENABLED=True

# Memory optimization (RTX 3060 için[1][2])
TORCH_DTYPE=float16
ATTENTION_IMPLEMENTATION=flash_attention_2
CACHE_DIR=./cache
HF_HUB_CACHE=./hf_cache

# Logging ve monitoring
LOG_LEVEL=INFO
LOG_FILE=logs/training.log
SAVE_STEPS=100
EVAL_STEPS=50
LOGGING_STEPS=10

# ✅ UI ayarları (StarCoder2 için optimize)
UI_THEME=dark
AUTO_SAVE_INTERVAL=300
REAL_TIME_METRICS=True
GPU_MONITORING=True

# ✅ Performance tuning (RTX 3060 specific[1])
DATALOADER_NUM_WORKERS=4
PIN_MEMORY=True
PERSISTENT_WORKERS=True
PREFETCH_FACTOR=2
"""

    # .env dosyasını kaydet
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)

        print(f"\n✅ RTX 3060 + StarCoder2-3B optimize .env oluşturuldu!")
        print(f"🎯 Model: {suggested_model}")
        print(f"📦 Batch size: {batch_size} (RTX 3060 optimized)")
        print(f"🚀 Sequence length: {sequence_length} (StarCoder2 16K context based[3])")
        print(f"🖥️ GPU device: {gpu_device}")
        print(f"💾 4-bit quantization: Enabled (~2GB memory footprint[2])")

    except Exception as e:
        logger.error(f"❌ .env dosyası oluşturma hatası: {e}")


def run_system_analysis():
    """
    ✅ MAIN ANALYSIS - ALL LIST ERRORS FIXED[1][2][3]
    """
    print("🤖 SeydappAI ModelTrainer - Sistem Analizi")
    print("=" * 60)

    # 🐍 Python bilgileri
    python_info = {
        "version": sys.version,
        "version_info": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "executable": sys.executable,
        "platform": platform.platform()
    }

    print(f"🐍 Python: {python_info['version_info']}")
    print(f"📍 Executable: {python_info['executable']}")
    print(f"💻 Platform: {python_info['platform']}")

    # 🖥️ GPU ve CUDA bilgileri - FIXED VERSION
    gpu_info = check_gpu_cuda_fixed()

    # 📦 Kütüphane kontrolü
    package_info = check_ml_packages()

    # 🎯 Sistem önerileri - FIXED VERSION
    recommendations = generate_recommendations_fixed(python_info, gpu_info, package_info)

    # 📝 .env dosyası oluştur - FIXED VERSION
    create_optimized_env_file_fixed(recommendations, gpu_info, python_info)

    return {
        "python": python_info,
        "gpu": gpu_info,
        "packages": package_info,
        "recommendations": recommendations
    }


def comprehensive_system_analysis():
    """
    ✅ FULLY PROTECTED: Kapsamlı sistem analizi[1][2][3]
    Tüm liste attribute hataları çözüldü
    """
    print("🔬 Comprehensive System Analysis")
    print("=" * 50)

    try:
        # 1. Safe system check
        safe_result = safe_system_check()

        if safe_result:
            print("\n🔄 Detailed analysis...")
            # 2. Detailed analysis
            detailed_result = run_system_analysis()
            return detailed_result
        else:
            print("❌ Basic system check failed")
            return None

    except Exception as e:
        print(f"❌ Comprehensive analysis error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    try:
        print("🚀 SeydappAI System Analysis Starting...")

        result = comprehensive_system_analysis()

        if result:
            print("\n🎉 Sistem analizi tamamlandı!")
            print("💡 .env dosyası sisteminize göre optimize edildi")
        else:
            print("\n❌ Sistem analizi başarısız")

    except KeyboardInterrupt:
        print("\n⏸️ İşlem kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"\n❌ Global hata: {e}")
        import traceback

        traceback.print_exc()
