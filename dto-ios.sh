mesaj = "DTÖUserBot Yükleyici"
mesaj += "Telegram: @DTOUserBot"
mesaj += "Çıxan her şeye Y ardından enterleyin."
clear
echo $mesaj
echo "Python yüklenir"
apk add python3
clear
echo $mesaj
echo "TeleThon yüklenir"
pip3 install telethon
pip3 install bs4
pip3 install requests
clear
echo $mesaj
echo "Fayl yazılır"
curl "https://raw.githubusercontent.com/umudmmmdov1/DTOUserBot/master/dto.py" --output "dto.py"
echo $mesaj
echo "Qurulum hazırdır, İndi StringSessionu ala bilersiz"
python3 dto.py
