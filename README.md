# Sudoku Üretici

Bu Python programı, rastgele Sudoku bulmacaları oluşturur ve çözümlerini kaydeder. Sudoku bulmacaları görsel olarak da oluşturulup, belirlenen bir klasöre kaydedilir.

## Gereksinimler

Bu programın çalışması için aşağıdaki Python kütüphaneleri gereklidir:

* numpy

* Pillow
  
* colorama

Bu kütüphaneleri yüklemek için aşağıdaki komutu çalıştırabilirsiniz:

`pip install numpy pillow colorama`

## Kullanım

1- Terminal veya komut istemcisinde aşağıdaki komutu çalıştırarak programı başlatın:

`python sudoku_generator.py`

2- Kaç adet Sudoku bulmacası üretmek istediğinizi girin.

3- Zorluk seviyesini belirleyin (17 ile 57 arasında bir değer).
* Bu değer tam dolu sudoku tahtasından kaç adet sayının kaldırılacağını belirler.

4- Program, oluşturulan Sudoku bulmacalarını Sudokular klasörüne, çözümlerini ise Sudoku Çözümleri klasörüne kaydedecektir.

## Program Özellikleri

* Program üretilen her bir sudokunun sadece bir çözümü olduğundan emin olur.
* Çözümü bozmadan kullanıcının istediği sayıda sayıyı tahtadan kaldırmak için tekrar tekrar deneme yapar.

# Lisans

Bu proje GNU GENERAL PUBLIC LICENSE ile lisanslanmıştır.
