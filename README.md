# Описание
Данный скрипт на питоне сгенерирует /etc/distcc/hosts, проверив что указанные в cluster.hosts узлы слушают порт 3632.
# Установка
Все команды выполняем от рута. Пути в инструкции подразумевают, что папка для скриптов в /root/src. Скрипт написан для linux. Для работы необходим python.
```
cd /root/src
git clone https://github.com/DimaKirk/distcc-gen-hosts.git
cd distcc-gen-hosts
crontab -l > tmp.cron
echo "*/5 * * * * /usr/bin/python /root/src/distcc-gen-hosts/distcc-genhosts.py" >> tmp.cron
echo "30 1 * * * cd /root/src/distcc-gen-hosts; git pull" >> tmp.cron
crontab tmp.cron
rm -f tmp.cron
```

Если ваш ip есть в cluster.hosts, то создайте файл exclude.hosts с ip адресами которые следует исключить из кластера. Разделителем служит перевод строки.

# Использование
```
python /root/src/distcc-gen-hosts/distcc-genhosts.py
```
Сгенерирует /etc/distcc/hosts для работы в plain mode. Для работы через pump:
```
python /root/src/distcc-gen-hosts/distcc-genhosts.py --pump
```
# компиляция с distcc

COMPILER='/root/src/distcc-gen-hosts/healdep.py distcc clang' CCOMPILER='/root/src/distcc-gen-hosts/healdep.py distcc clang++' make -j20

Для чего здесь /root/src/distcc-gen-hosts/healdep.py? При компиляции создаются неправильные .Po файлы. В них неверный путь и иногда при изменении заголовочного файла компилятор не понимает, что нужно пересобрать объект. healdep.py исправит пути и все будет хорошо.
