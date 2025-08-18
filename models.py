from sklearn.linear_model import LinearRegression

# X = [sleep_hours, action_hours]
X = []
y = []

# 0=yomon, 1=o'rta, 2=yaxshi
for sleep in range(1, 13):  # 1–12 soat uyqu
    action = 24 - sleep     # 1 soat uyqu → 23 soat harakat, 2→22, ...
    X.append([sleep, action])
    
    # Yaratish qoidasi:
    # kam uyqu + ko'p harakat → o'rta/yaxshi
    # ko'p uyqu + kam harakat → o'rta/yaxshi
    # o'rta uyqu + o'rta harakat → o'rta
    if sleep <= 4 and action >= 20:
        y.append(0)  # juda kam uyqu + ko'p harakat → yaxshi
    elif 5 <= sleep <= 8 and 12 <= action <= 20:
        y.append(1)  # normal uyqu + normal/ko'p harakat → o'rta
    else:
        y.append(2)  # ko'p uyqu + kam harakat → yaxshi


# Modelni fit qilish
model = LinearRegression()
model.fit(X, y)

class Analyzer:
    def __init__(self, telegram_id, sleep_time, action_time, agression, mood):
        self.telegram_id = telegram_id
        self.sleep_time = int(sleep_time)
        self.action_time = int(action_time)
        self.agression = agression
        self.mood = mood
        self.advices = []

    def analyze_energy(self):
        """Asosiy energy prediction"""
        prediction = model.predict([[self.sleep_time, self.action_time]])[0]
        return round(prediction, 2)  # qiymatni yaxlitlab qaytarish

    def get_conclusion(self):
        """Xulosa va maslahatlarni chiqarish"""
        pred = self.analyze_energy()
        
        # Mood kategoriyasini aniqlash
        if pred < 0.8:
            mood_text = "yomon"
            advice = "Ko‘proq uxlash va jismoniy harakatni oshiring."
        elif 0.8 <= pred < 1.5:
            mood_text = "o'rta"
            advice = "Uyqu va harakat balansini saqlashga harakat qiling."
        else:
            mood_text = "yaxshi"
            advice = "Davom eting! Siz yaxshi holatda ekansiz."
        
        # Agresiya bo‘yicha maslahat
        if self.agression in ["low","ag_low"]:
            ag_text = "Past"
        elif self.agression in ["normal","ag_normal"]:
            ag_text = "O'rtacha"
        else:
            ag_text = "Baland"

        # Kayfiyat emoji bo‘yicha tavsiyalar
        mood_dict = {
            "1":"😡 Juda yomon",
            "2":"😐 O'rtacha",
            "3":"🙂 Yaxshi",
            "4":"😃 Juda yaxshi",
            "5":"🤩 Ajoyib"
        }
        mood_desc = mood_dict.get(str(self.mood), "Noma'lum")
        
        # Maslahatlar
        advices = []
        
        # Uyqu bo‘yicha
        if self.sleep_time < 6:
            advices.append("Uyqu yetarli emas: ko‘proq dam olish va uxlashga harakat qiling.")
        elif 6 <= self.sleep_time <= 8:
            advices.append("Uyqu normal: shunday davom eting.")
        else:
            advices.append("Ko‘p uyqu: bu yaxshi, lekin kun davomida faollikni ham saqlang.")
        
        # Jismoniy harakat bo‘yicha
        if self.action_time < 3:
            advices.append("Jismoniy harakat yetarli emas: qisqa yurishlar yoki mashqlar qo‘shing.")
        elif 3 <= self.action_time <= 6:
            advices.append("Jismoniy faollik normal: shunday davom eting.")
        else:
            advices.append("Juda faol kun: tanaffuslar bilan energiyani saqlang.")
        
        # Agressiya bo‘yicha
        if ag_text == "Past":
            advices.append("Agressiya darajasi past: yaxshi holat, ijobiy kayfiyatni saqlang.")
        elif ag_text == "O'rtacha":
            advices.append("Agressiya darajasi o‘rtacha: stressni kamaytirish uchun qisqa mashqlar yoki meditatsiya qilishingiz mumkin.")
        else:
            advices.append("Agressiya darajasi baland: chuqur nafas olish va dam olishga harakat qiling.")
        
        # Kayfiyat bo‘yicha
        if mood_desc in ["😡 Juda yomon", "😐 O'rtacha"]:
            advices.append("Kayfiyatingiz past: sevimli mashg‘ulotlar bilan o‘zingizni ko‘tarishga harakat qiling.")
        else:
            advices.append("Kayfiyatingiz yaxshi: ijobiy kayfiyatni saqlang va boshqalarni ham rag‘batlantiring.")
        
        # Umumiy maslahat
        advices.append("Kunlik rejimingizni muvozanatda saqlang: uyqu, harakat va dam olish balansini kuzating.")
        
        # Maslahatlarni birlashtirish
        advices_text = "\n• ".join([""] + advices)  # • bilan chiroyli ro‘yxat
        
        # Yakuniy xulosa bilan birlashtirish
        result_text = (
            f"<b>Umumiy holat:\n</b>"
            f"Kunlik uyqu vaqti: {self.sleep_time} soat\n"
            f"Kunlik jismoniy harakat vaqti: {self.action_time} soat\n"
            f"Agressiya (asabiylik) darajasi: {ag_text}\n"
            f"Kayfiyat: {mood_desc}\n\n"
            f"<b>Ushbu maslahatlar sizga foydali bo'lishi mumkin:\n</b>•{advices_text}"
        )
        return result_text
        