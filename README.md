# HealthTracker - doimiy jismoniy va ruhiy holatni AI modellar orqali o'rganib boruvchi bot.

## Maqsad:
  1. **aiogram** bo'yicha o'rgangan ma'lumotlarni amalda sinash.
  2. **sklearn, ML modellar** bo'yicha o'rganganlarni amalda sinash.

## Bot va ishlashi haqida qisqacha:
  - `/start` command orqali bot ishga tushiriladi va shu jarayon o'zida user ro'yxatdan o'tadi.
  - Har kuni kunlik uyqu vaqti, jismoniy harakatlar umumiy vaqti, agressiya darajasi, kayfiyat user tomonidan botga yuboriladi (esidan chiqsa bot o'zi xabar yuboradi).
  - Berilgan ma'lumotlar asosida bot userga bugungi kuni haqida xulosa beradi. Misol uchun nega bugun kayfiyati past bo'lgani va h.k.
  - Va ertangi kun uchun ham maslahat va ma'lumotlar beradi, misol uchun: "Agar bugun ham shunday kam uxlasang ertaga kayfiyat bundan ham past bo'lishi mumkin." va h.k.
  - Agar shu joyigacha asabiylashmasdan yetib kelsam user uchun oxirgi 1hafta ma'lumotlari asosida grafik ham tashlab berish funksiyasini qo'shaman.

> Bu birinchi yasagan kichik AI modelim bo'ladi va buni kelajakda yana kuchaytirib AI Agent yasash niyatin ham bor (o'zi Agent uchun o'rganyabman).