mesaj = "DTÖUserBot Yükləyici"
mesaj += "Telegram: @DTOUserBot"
mesaj += "Çıxan hər şeyə Y ardından enterləyin."
clear
echo $mesaj
echo "Python yüklənir"
apk add python3
clear
echo $mesaj
echo "TeleThon yüklənir"
pip3 install telethon
pip3 install bs4
pip3 install requests
clear
echo $mesaj
echo "Fayl yazılır"
curl "https://raw.githubusercontent.com/umudmmmdov1/DTOUserBot/master/dto.py" --output "dto.py"
echo $mesaj
echo "Qurulum hazırdır, İndi StringSessionu ala bilərsiz"
python3 dto.py
