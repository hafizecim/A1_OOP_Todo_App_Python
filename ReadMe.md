

# 📌 Flask Task Manager — Görev Takip Sistemi

Bu proje, Flask ve SQLite kullanılarak geliştirilmiş **tam işlevli bir Görev Yönetim Sistemi**dir.
Kullanıcılar görev oluşturabilir, başlatabilir, durdurabilir, tamamlayabilir ve tüm aşamaları adım adım takip edebilir.

Ayrıca görevlerin:

* Zaman takibi ⏳
* Açıklama ekleme 📝
* Durum yönetimi 🔄
* Filtreleme ve sıralama 🧭
* Başlama/Bitiş zamanları 📅
* Kalan süre hesaplama ⏱
* Detay sayfası ve modal görünüm 📄

gibi özellikleri bulunmaktadır.

---

# 🚀 Özellikler (Features)

### ✔ Görev Ekleme

Kullanıcılar başlık ve açıklama ile yeni görev oluşturabilir.

### ✔ Görev Durum Yönetimi

Görevler aşağıdaki statüler arasında otomatik veya manuel geçiş yapar:

* `pending` — Beklemede
* `in_progress` — Devam Ediyor
* `paused` — Duraklatıldı
* `completed` — Tamamlandı

### ✔ Zaman Takibi

Sistem, göreve başlandığı, durdurulduğu ve tamamlandığı zamanı kaydeder.

### ✔ Kalan Süre Hesaplama

Görevin bitiş tarihi ile şimdiki zaman arasındaki fark hesaplanır.

### ✔ Görev Düzenleme

Başlık ve açıklama güncellenebilir.

### ✔ Görev Silme

Görev tamamen kaldırılabilir.

### ✔ Filtreleme

Kullanıcılar görevleri statülerine göre listeleyebilir.

### ✔ Aktif Görev Kartı

Devam eden görevi ekranda kart olarak gösterir.

### ✔ Responsive Bootstrap Arayüzü

Mobil ve masaüstü uyumlu modern bir UI.

---

# 📁 Proje Yapısı

```
/project-folder
│
├── app.py                # Flask uygulaması
├── todo.db               # SQLite veritabanı
│
├── /templates
│   └── index.html        # Ana sayfa
│   └── edit.html         # Ana sayfa
│   └── new_task.html     # Ana sayfa
│
├── /static
│   └── style.css         # Ek CSS (isteğe bağlı)
│
└── README.md             # Bu dosya
```

---

# 🔧 Kullanılan Teknolojiler

| Teknoloji            | Açıklama                 |
| -------------------- | ------------------------ |
| **Python**           | Arka uç dili             |
| **Flask**            | Web framework            |
| **SQLite**           | Dosya tabanlı veritabanı |
| **Flask-SQLAlchemy** | ORM                      |
| **Bootstrap 5**      | UI tasarımı              |
| **Jinja2**           | Template motoru          |

---

# 🛠 Kurulum ve Çalıştırma Rehberi (Windows PowerShell)

Bu bölüm senin verdiğin içeriğin **düzenlenmiş ve profesyonelleştirilmiş** halidir.

---

## 1️⃣ PowerShell’i aç ve proje klasörüne git

```powershell
cd "C:\Users\Your_Project"
```

---

## 2️⃣ Sanal ortam oluştur

```powershell
py -3 -m venv venv
```

---

## 3️⃣ Sanal ortamı aktif et

```powershell
.\venv\Scripts\Activate.ps1
```

✔ Aktifleştikten sonra komut satırında `(venv)` görünür.

⚠ Eğer izin hatası alırsan:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Daha sonra sanal ortamı yeniden aktif et.

---

## 4️⃣ Flask’ı yükle

```powershell
pip install Flask
```

📌 Örnek `pip list` çıktısı:

```
Package      Version
------------ -------
blinker      1.9.0
click        8.3.1
colorama     0.4.6
Flask        3.1.2
itsdangerous 2.2.0
Jinja2       3.1.6
MarkupSafe   3.0.3
pip          25.2
Werkzeug     3.1.3
```

---

## 5️⃣ Flask uygulamasını çalıştır

```powershell
python app.py
```

Tarayıcıda açmak için:

```
http://127.0.0.1:5000/
```

---

## 6️⃣ Flask-SQLAlchemy yükle

```powershell
pip install Flask-SQLAlchemy
```

Bu adımlardan sonra proje tamamen hazır 🎉

---

# 🎯 Yapılabileceklere Örnek Geliştirmeler

Aşağıdaki ek özellikler proje üzerine kolayca eklenebilir:

### 🔹 Kullanıcı Girişi (Login/Register)

Görevler farklı kullanıcı hesapları ile kullanılabilir.

### 🔹 Log / Aktivite Kaydı

Her işlem otomatik olarak günlüğe işlenebilir.

### 🔹 Görev İstatistik Paneli

Grafikler ile:

* Günlük görev tamamlama sayısı
* Aktif görev süresi
* Duraklatılmış görevler
* En uzun / en kısa görev süresi

raporlanabilir.

### 🔹 Görevlerin PDF/CSV Olarak Dışa Aktarılması

Yönetim raporları için ideal.

### 🔹 Karanlık Tema

Bootstrap tema switch ile kolayca eklenebilir.

### 🔹 Görevlere Dosya Eklemek

Word/PDF/Resim yükleme.

---

# 🧪 Örnek Ekran Görünümü

(Buraya daha sonra ekran görüntüleri eklenecektir.)

---

# 🤝 Katkı

Pull request’ler ve öneriler her zaman açıktır.

---
