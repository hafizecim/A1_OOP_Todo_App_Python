# Flask Projesi — Kurulum ve Çalıştırma Rehberi

Aşağıdaki adımlar, Flask tabanlı bir projenin Windows PowerShell üzerinde doğru şekilde kurulmasını ve çalıştırılmasını sağlar.

---

## 1️⃣ PowerShell’i aç ve proje klasörüne git

```powershell
cd "C:\Users\Your_Project"

```
## 2️⃣ Sanal ortam oluştur

```powershell
py -3 -m venv venv
```

---

## 3️⃣ Sanal ortamı aktif et

```powershell
.\venv\Scripts\Activate.ps1
```

✔ Aktif olursa komut satırının başında `(venv)` görünür.

⚠ Eğer izin hatası alırsan:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Ardından sanal ortamı tekrar aktif et.

---

## 4️⃣ Flask’ı yükle

```powershell
pip install Flask
```

📌 Kurulum sonrası örnek `pip list` çıktısı:

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

🌐 Tarayıcıda görüntülemek için:
`http://127.0.0.1:5000/`

---

## 6️⃣ Flask-SQLAlchemy yükle

Veritabanı işlemleri için gerekli olan SQLAlchemy eklentisini yükleyin:

```powershell
pip install Flask-SQLAlchemy
```

---

Bu adımları tamamladıktan sonra proje tamamen çalışmaya hazırdır.

```

---


```
