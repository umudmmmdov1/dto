MESAJ="DTÖUserBot Yükləyici"
MESAJ+="\nTelegram: @DTOUserBot"
pkg upgrade
clear
echo -e $MESAJ
echo "Python yüklənir"
pkg install python -y
clear
echo -e $MESAJ
echo "TeleThon yüklənir"
pip install telethon
echo "Requests/BS4 yüklənir"
pip install requests
pip install bs4
clear
echo -e $MESAJ
echo "Fayl yazılır..."
curl "https://raw.githubusercontent.com/umudmmmdov1/DTOUserBot/master/dto.py" --output "dto.py"
clear
echo -e $MESAJ
echo "Qurulum hazırdır, İndi StringSessionu ala bilərsiz"
clear
python dto.py
