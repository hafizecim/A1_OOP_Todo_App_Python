Tabii! İşte senin kurulum adımlarını **Markdown formatında, düzenli ve okunabilir şekilde** hazırladım:

````markdown
# Flask Projesi Kurulum ve Çalıştırma Adımları

## 1️⃣ PowerShell’i aç ve proje klasörüne git

```powershell
cd "C:\Users\Your_Project"
````

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

* Başarılı olursa prompt’ta `(venv)` görünecek.

* Eğer güvenlik nedeniyle çalışmazsa, önce şu komutu çalıştır:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

sonra tekrar aktive et.

---

## 4️⃣ Flask’ı yükle

```powershell
pip install flask
```

* Yükleme sonrası `pip list` çıktısı örneği:

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

* Tarayıcıda açmak için: `http://127.0.0.1:5000`
* Artık Flask projesi çalışıyor ve sanal ortam aktif durumda.

```


