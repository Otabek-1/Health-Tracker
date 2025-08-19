# Health Tracker Bot - Yangilangan Versiya

## O'zgarishlar va Yaxshilanishlar

### ✅ Hal qilingan muammolar:
- **Vaqt zonasi tuzatildi**: Endi GMT+5 (Toshkent vaqti) bo'yicha ishlaydi
- **Ma'lumot kiritish vaqti**: Soat 21:00 dan keyin mahalliy vaqt bo'yicha
- **Scheduler**: Eslatmalar ham mahalliy vaqt bo'yicha yuboriladi
- **Database**: SQLite ishonchli ishlaydi va ma'lumotlar saqlanadi

### 🆕 Qo'shilgan xususiyatlar:
- **AI tahlil**: So'nggi kunlar ma'lumotlari asosida tahlil
- **Korrelyatsiya analizi**: Uyqu, faollik, kayfiyat o'rtasidagi bog'liqlik
- **Shaxsiylashtirilgan maslahatlar**: Har bir user uchun individual tavsiyalar
- **Haftalik tendensiyalar**: 7 kunlik ma'lumotlar asosida tahlil
- **To'liq state management**: FSM bilan step-by-step ma'lumot kiritish

### 📋 Bot buyruqlari:
- `/start` - Ro'yxatdan o'tish
- `/today` - Kunlik ma'lumot kiritish (21:00 dan keyin)
- `/stats` - So'nggi 7 kunlik statistika
- `/help` - Yordam

### 🔧 Ishga tushirish:
```bash
pip install -r requirements.txt
python main.py
```

### 📊 Ma'lumotlar:
- **Uyqu vaqti**: Soat hisobida (0-24)
- **Jismoniy faollik**: Soat hisobida (0-24)
- **Agressiya**: Past/O'rtacha/Baland (1-3)
- **Kayfiyat**: 😡😐🙂😃🤩 (1-5)

### 🗃️ Database:
- SQLite (HealtTracker.db)
- Automatic table creation
- User va health_data jadvallari

### ⏰ Scheduler:
- Har kuni soat 21:00 da avtomatik eslatma
- Mahalliy vaqt zonasi bo'yicha
- Faqat ma'lumot kiritmagan userlar uchun

### 🏗️ Arxitektura:
- **main.py**: Asosiy ishga tushirish
- **bot.py**: Bot konfiguratsiyasi
- **handlers.py**: Xabar va buyruq handlerlari
- **database.py**: SQLite operatsiyalari
- **ml_analysis.py**: AI tahlil va maslahatlar
- **scheduler.py**: Kunlik eslatmalar
- **models.py**: Ma'lumot modellari
- **config.py**: Sozlamalar va konstantalar

### 🔑 Environment:
```
BOT_TOKEN=your_telegram_bot_token
```

Bot to'liq ishga tayyor va production uchun optimizatsiya qilingan!