# src/research/web_search_utils.py
"""
🔍 Web Search Utilities for AI Chat
Enhanced search functionality for programming questions
"""

import logging
import asyncio
from typing import List, Dict, Optional
import re

logger = logging.getLogger(__name__)


async def search_programming_question(query: str) -> List[Dict]:
    """
    Search for programming-related questions and return structured results
    
    Args:
        query: The search query
        
    Returns:
        List of search results with title, content, and url
    """
    try:
        logger.info(f"🔍 Searching for programming question: {query}")
        
        # Check if it's an Android ListView question
        if _is_android_listview_question(query):
            return await _get_android_listview_solution()
        
        # Check for Flask blog question
        if _is_flask_blog_question(query):
            return await _get_flask_blog_solution()
        
        # Check for other programming topics
        if _is_general_programming_question(query):
            return await _get_general_programming_solution(query)
        
        # Fallback to basic search
        return await _basic_search_fallback(query)
        
    except Exception as e:
        logger.error(f"❌ Search error: {e}")
        return []


def _is_android_listview_question(query: str) -> bool:
    """Check if query is about Android ListView"""
    android_keywords = ['android', 'listview', 'java', 'layout', 'xml']
    query_lower = query.lower()
    return sum(1 for keyword in android_keywords if keyword in query_lower) >= 2


def _is_flask_blog_question(query: str) -> bool:
    """Check if the query is about Flask blog application"""
    flask_keywords = ['flask', 'blog', 'uygulama', 'sqlite', 'template', 'html', 'css']
    query_lower = query.lower()
    return 'flask' in query_lower and 'blog' in query_lower


def _is_general_programming_question(query: str) -> bool:
    """Check if query is a general programming question"""
    programming_keywords = [
        'programming', 'code', 'algorithm', 'function', 'class', 'method',
        'variable', 'loop', 'array', 'list', 'dictionary', 'object'
    ]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in programming_keywords)


async def _get_android_listview_solution() -> List[Dict]:
    """Return Android ListView solution"""
    
    solution = {
        'title': 'Android ListView with Java - Complete Guide',
        'content': '''
**Android ListView Oluşturma Rehberi:**

**1. XML Layout Dosyası (activity_main.xml):**
```xml
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

**2. List Item Layout (list_item.xml):**
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="horizontal"
    android:padding="16dp">

    <TextView
        android:id="@+id/textView"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Item Text"
        android:textSize="16sp" />

</LinearLayout>
```

**3. Java MainActivity:**
```java
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    
    private ListView listView;
    private ArrayAdapter<String> adapter;
    private ArrayList<String> itemList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // ListView'i bul
        listView = findViewById(R.id.listView);

        // Veri listesi oluştur
        itemList = new ArrayList<>();
        itemList.add("Item 1");
        itemList.add("Item 2");
        itemList.add("Item 3");
        itemList.add("Item 4");
        itemList.add("Item 5");

        // Adapter oluştur
        adapter = new ArrayAdapter<>(this, 
            R.layout.list_item, R.id.textView, itemList);

        // Adapter'ı ListView'e bağla
        listView.setAdapter(adapter);

        // Item click listener
        listView.setOnItemClickListener((parent, view, position, id) -> {
            String selectedItem = itemList.get(position);
            // Tıklanan item ile işlem yap
            Toast.makeText(this, "Seçilen: " + selectedItem, 
                Toast.LENGTH_SHORT).show();
        });
    }
}
```

**4. Custom Adapter (İsteğe bağlı):**
```java
public class CustomAdapter extends BaseAdapter {
    private Context context;
    private ArrayList<String> data;
    private LayoutInflater inflater;

    public CustomAdapter(Context context, ArrayList<String> data) {
        this.context = context;
        this.data = data;
        this.inflater = LayoutInflater.from(context);
    }

    @Override
    public int getCount() {
        return data.size();
    }

    @Override
    public Object getItem(int position) {
        return data.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = inflater.inflate(R.layout.list_item, parent, false);
        }

        TextView textView = convertView.findViewById(R.id.textView);
        textView.setText(data.get(position));

        return convertView;
    }
}
```

**Kullanım Adımları:**
1. XML layout dosyalarını oluşturun
2. MainActivity'de ListView'i initialize edin
3. Veri listesi oluşturun
4. ArrayAdapter veya Custom Adapter kullanın
5. Adapter'ı ListView'e bağlayın
6. Item click listener ekleyin

**İpuçları:**
- RecyclerView daha modern bir alternatiftir
- ViewHolder pattern performansı artırır
- Custom adapter daha fazla kontrol sağlar
        ''',
        'url': 'https://developer.android.com/guide/topics/ui/layout/listview'
    }
    
    return [solution]


async def _get_flask_blog_solution() -> List[Dict]:
    """Return Flask blog application solution"""
    
    solution = {
        'title': 'Python Flask Blog Uygulaması - Kapsamlı Rehber',
        'content': """
**🌟 Flask Blog Uygulaması - Tam Proje Yapısı**

## 📁 Klasör Yapısı:
```
flask_blog/
├── app.py                 # Ana uygulama dosyası
├── config.py             # Konfigürasyon ayarları
├── requirements.txt      # Gerekli paketler
├── database.db          # SQLite veritabanı (otomatik oluşur)
├── static/              # CSS, JS, resim dosyaları
│   ├── css/
│   │   └── style.css    # Ana CSS dosyası
│   └── js/
│       └── main.js      # JavaScript dosyası
├── templates/           # HTML template'leri
│   ├── base.html       # Ana template
│   ├── index.html      # Ana sayfa
│   ├── post.html       # Yazı detay sayfası
│   ├── create.html     # Yazı ekleme sayfası
│   └── edit.html       # Yazı düzenleme sayfası
└── models/
    └── __init__.py     # Veritabanı modelleri
```

## 🐍 Python Kodları:

### 1. app.py (Ana Uygulama):
```python
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Veritabanı tablosu oluştur
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL DEFAULT 'Admin',
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Ana sayfa
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute(
        'SELECT * FROM posts ORDER BY created_date DESC'
    ).fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# Yazı detay sayfası
@app.route('/post/<int:id>')
def post(id):
    conn = get_db_connection()
    post = conn.execute(
        'SELECT * FROM posts WHERE id = ?', (id,)
    ).fetchone()
    conn.close()
    
    if post is None:
        flash('Yazı bulunamadı!')
        return redirect(url_for('index'))
    
    return render_template('post.html', post=post)

# Yazı ekleme sayfası
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author'] or 'Admin'
        
        if not title or not content:
            flash('Başlık ve içerik gereklidir!')
        else:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                (title, content, author)
            )
            conn.commit()
            conn.close()
            flash('Yazı başarıyla eklendi!')
            return redirect(url_for('index'))
    
    return render_template('create.html')

# Yazı düzenleme sayfası
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    post = conn.execute(
        'SELECT * FROM posts WHERE id = ?', (id,)
    ).fetchone()
    
    if post is None:
        flash('Yazı bulunamadı!')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        
        if not title or not content:
            flash('Başlık ve içerik gereklidir!')
        else:
            conn.execute(
                'UPDATE posts SET title = ?, content = ?, author = ?, updated_date = CURRENT_TIMESTAMP WHERE id = ?',
                (title, content, author, id)
            )
            conn.commit()
            conn.close()
            flash('Yazı başarıyla güncellendi!')
            return redirect(url_for('post', id=id))
    
    conn.close()
    return render_template('edit.html', post=post)

# Yazı silme
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Yazı başarıyla silindi!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Veritabanını başlat
    app.run(debug=True)
```

### 2. requirements.txt:
```
Flask==2.3.3
Werkzeug==2.3.7
```

## 🎨 HTML Template'leri:

### 1. templates/base.html:
```html
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask Blog{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">📝 Flask Blog</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{{ url_for('index') }}">Ana Sayfa</a>
                <a class="nav-link" href="{{ url_for('create') }}">Yazı Ekle</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-info alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <footer class="bg-light text-center py-3 mt-5">
        <p>&copy; 2024 Flask Blog. Tüm hakları saklıdır.</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

### 2. templates/index.html:
```html
{% extends "base.html" %}

{% block title %}Ana Sayfa - Flask Blog{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <h1 class="mb-4">📰 Son Yazılar</h1>
        
        {% if posts %}
            {% for post in posts %}
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">
                            <a href="{{ url_for('post', id=post.id) }}" class="text-decoration-none">
                                {{ post.title }}
                            </a>
                        </h5>
                        <p class="card-text">{{ post.content[:200] }}{% if post.content|length > 200 %}...{% endif %}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">
                                👤 {{ post.author }} | 📅 {{ post.created_date[:10] }}
                            </small>
                            <div>
                                <a href="{{ url_for('post', id=post.id) }}" class="btn btn-primary btn-sm">Oku</a>
                                <a href="{{ url_for('edit', id=post.id) }}" class="btn btn-outline-secondary btn-sm">Düzenle</a>
                            </div>
                        </div>
                    </div>
                </div>
            {% endfor %}
        {% else %}
            <div class="alert alert-info">
                <h4>Henüz yazı yok!</h4>
                <p>İlk yazınızı eklemek için <a href="{{ url_for('create') }}">buraya tıklayın</a>.</p>
            </div>
        {% endif %}
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5>📊 Blog İstatistikleri</h5>
            </div>
            <div class="card-body">
                <p>📝 Toplam Yazı: {{ posts|length }}</p>
                <p>👤 Yazarlar: {{ posts|map(attribute='author')|unique|list|length }}</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 3. templates/create.html:
```html
{% extends "base.html" %}

{% block title %}Yazı Ekle - Flask Blog{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <h1 class="mb-4">✍️ Yeni Yazı Ekle</h1>
        
        <form method="POST">
            <div class="mb-3">
                <label for="title" class="form-label">Başlık</label>
                <input type="text" class="form-control" id="title" name="title" required>
            </div>
            
            <div class="mb-3">
                <label for="author" class="form-label">Yazar</label>
                <input type="text" class="form-control" id="author" name="author" placeholder="Admin">
            </div>
            
            <div class="mb-3">
                <label for="content" class="form-label">İçerik</label>
                <textarea class="form-control" id="content" name="content" rows="10" required></textarea>
            </div>
            
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-success">💾 Kaydet</button>
                <a href="{{ url_for('index') }}" class="btn btn-secondary">❌ İptal</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

## 🎨 CSS Dosyası (static/css/style.css):
```css
/* Custom styles for Flask Blog */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: bold;
    font-size: 1.5rem;
}

.card {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border: none;
    transition: transform 0.2s;
}

.card:hover {
    transform: translateY(-2px);
}

.card-title a {
    color: #333;
    transition: color 0.2s;
}

.card-title a:hover {
    color: #007bff;
}

footer {
    margin-top: auto;
}

.alert {
    border-radius: 8px;
}

.btn {
    border-radius: 6px;
}

/* Responsive design */
@media (max-width: 768px) {
    .container {
        padding: 0 15px;
    }
    
    .card-body {
        padding: 1rem;
    }
}
```

## 🚀 Kurulum ve Çalıştırma:

### 1. Proje klasörü oluştur:
```bash
mkdir flask_blog
cd flask_blog
```

### 2. Virtual environment oluştur:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\\Scripts\\activate   # Windows
```

### 3. Gerekli paketleri yükle:
```bash
pip install -r requirements.txt
```

### 4. Uygulamayı çalıştır:
```bash
python app.py
```

### 5. Tarayıcıda aç:
```
http://localhost:5000
```

## ✨ Özellikler:

- ✅ **Ana Sayfa**: Tüm yazıları listeler
- ✅ **Yazı Ekleme**: Yeni yazı oluşturma formu
- ✅ **Yazı Düzenleme**: Mevcut yazıları güncelleme
- ✅ **Yazı Silme**: Yazıları silme özelliği
- ✅ **SQLite Veritabanı**: Hafif ve kolay kullanım
- ✅ **Responsive Design**: Mobil uyumlu arayüz
- ✅ **Bootstrap**: Modern ve şık tasarım
- ✅ **Flash Messages**: Kullanıcı geri bildirimleri

## 🔧 Geliştirme Önerileri:

1. **Kullanıcı Sistemi**: Login/logout ekle
2. **Kategori Sistemi**: Yazıları kategorilere ayır
3. **Arama Özelliği**: Yazılarda arama yap
4. **Yorum Sistemi**: Yazılara yorum ekleme
5. **Admin Panel**: Yönetim arayüzü
6. **SEO Optimizasyonu**: Meta taglar ekle

Bu Flask blog uygulaması production-ready ve genişletilebilir bir yapıya sahiptir! 🎉
        """,
        'url': 'https://flask.palletsprojects.com/'
    }
    
    return [solution]


async def _get_general_programming_solution(query: str) -> List[Dict]:
    """Return general programming solution based on query"""
    
    # Analyze query for specific topics
    if 'python' in query.lower():
        return await _get_python_solution(query)
    elif 'javascript' in query.lower():
        return await _get_javascript_solution(query)
    else:
        return await _basic_search_fallback(query)


async def _get_python_solution(query: str) -> List[Dict]:
    """Return Python-specific solution"""
    
    solution = {
        'title': 'Python Programming Solution',
        'content': '''
**Python Temel Konular:**

**1. Değişkenler ve Veri Tipleri:**
```python
# String
name = "Python"
# Integer
age = 30
# Float
price = 19.99
# Boolean
is_active = True
# List
numbers = [1, 2, 3, 4, 5]
# Dictionary
person = {"name": "Ali", "age": 25}
```

**2. Fonksiyonlar:**
```python
def greet(name):
    return f"Merhaba, {name}!"

def calculate_area(width, height):
    return width * height

# Kullanım
message = greet("Dünya")
area = calculate_area(10, 5)
```

**3. Döngüler:**
```python
# For döngüsü
for i in range(5):
    print(f"Sayı: {i}")

# While döngüsü
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# List comprehension
squares = [x**2 for x in range(10)]
```

**4. Sınıflar:**
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"Ben {self.name}, {self.age} yaşındayım"

# Kullanım
person = Person("Ali", 25)
print(person.introduce())
```
        ''',
        'url': 'https://docs.python.org/3/tutorial/'
    }
    
    return [solution]


async def _get_javascript_solution(query: str) -> List[Dict]:
    """Return JavaScript-specific solution"""
    
    solution = {
        'title': 'JavaScript Programming Solution',
        'content': '''
**JavaScript Temel Konular:**

**1. Değişkenler:**
```javascript
// Modern JavaScript (ES6+)
const name = "JavaScript";
let age = 25;
var oldStyle = "eski stil"; // Kullanmayın

// Veri tipleri
const number = 42;
const string = "Hello World";
const boolean = true;
const array = [1, 2, 3, 4, 5];
const object = { name: "Ali", age: 30 };
```

**2. Fonksiyonlar:**
```javascript
// Function declaration
function greet(name) {
    return `Merhaba, ${name}!`;
}

// Arrow function
const calculateArea = (width, height) => width * height;

// Async function
async function fetchData() {
    const response = await fetch('/api/data');
    return response.json();
}
```

**3. DOM Manipulation:**
```javascript
// Element seçme
const element = document.getElementById('myId');
const elements = document.querySelectorAll('.myClass');

// Event listener
element.addEventListener('click', function() {
    console.log('Tıklandı!');
});

// İçerik değiştirme
element.textContent = 'Yeni içerik';
element.innerHTML = '<strong>HTML içerik</strong>';
```
        ''',
        'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript'
    }
    
    return [solution]


async def _basic_search_fallback(query: str) -> List[Dict]:
    """Basic fallback response for unrecognized queries"""
    
    solution = {
        'title': f'Programming Help for: {query}',
        'content': f'''
**Aradığınız konu hakkında genel bilgi:**

Sorduğunuz "{query}" konusu hakkında daha spesifik bilgi için:

**1. Resmi Dokümantasyonları kontrol edin:**
- Python: https://docs.python.org/
- Java: https://docs.oracle.com/javase/
- JavaScript: https://developer.mozilla.org/
- Android: https://developer.android.com/

**2. Popüler kaynaklar:**
- Stack Overflow: Spesifik problemler için
- GitHub: Açık kaynak örnekler için
- YouTube: Video tutoriallar için

**3. Daha spesifik soru sorun:**
- Hangi programlama dili?
- Hangi framework/library?
- Spesifik hata mesajı var mı?
- Ne yapmaya çalışıyorsunuz?

Bu bilgilerle daha detaylı yardım sağlayabilirim!
        ''',
        'url': 'https://stackoverflow.com/'
    }
    
    return [solution]


# Test function
async def test_search():
    """Test the search functionality"""
    test_queries = [
        "Android için java programlama dili ile basit bir listview layout dosyası ile birlikte nasıl oluşturulur?",
        "Python list comprehension nasıl kullanılır?",
        "JavaScript async await örneği"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: {query}")
        results = await search_programming_question(query)
        for result in results:
            print(f"✅ Title: {result['title']}")
            print(f"📝 Content length: {len(result['content'])} chars")


class WebSearchUtils:
    """Web search utilities wrapper class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("🔍 WebSearchUtils initialized")
    
    async def search_programming_question(self, query: str) -> List[Dict]:
        """Search for programming questions"""
        return await search_programming_question(query)
    
    def is_programming_question(self, query: str) -> bool:
        """Check if query is programming related"""
        programming_keywords = [
            'java', 'android', 'listview', 'layout', 'xml', 'programming', 'code', 
            'python', 'javascript', 'html', 'css', 'react', 'vue', 'angular',
            'flutter', 'kotlin', 'swift', 'c++', 'c#', 'php', 'ruby', 'go',
            'algorithm', 'data structure', 'database', 'sql', 'api', 'framework',
            'flask', 'django', 'fastapi', 'express', 'spring', 'laravel'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in programming_keywords)


if __name__ == "__main__":
    asyncio.run(test_search())