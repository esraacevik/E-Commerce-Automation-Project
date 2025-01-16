# Mağazalar için Ürün Fiyat Takibi ve Alısverisi Otomatiklestirme Projesi

Bu proje, inditex magazalardaki (şu anlık sadece zara için uygulanabilir.) hesabınıza giriş yaparak sepetinizde bulunan veya beğenilenler listenize
eklemiş olduğunuz ürünlerin fiyatlarını ve mevcut stok durumlarını takip eden,fiyat değişikliklerini kontrol eden bu verileri Excel
dosyasına kaydeden bir uygulamayı hayata geçirir. 
Beğeniler listenizde olan ürünleri fiyat değişikliği veya stok güncellemesi olması durumunda sepetinize otomatik olarak ekler.


## Özellikler
İki aşamalı bir uygulamadır.
İsterseniz hesabınıza giriş yapıp sepetinize mudahale edebilir isterseniz de giriş yapmadan daha öncesinde kaydettiğiniz bir excel dosyasını yükleyip
fiyat ve stok takibini kolayca yapabilirsiniz.
- **Excel Dosyası Yükleme**: (Var olan ürün ve fiyat bilgilerini Excel dosyasından yükleme). Bu aşama zorunlu değildir. Eğer giriş yapmadan uygulamayı kullanmak
-  isterseniz dosya yüklemelisiniz ancak hesabınıza giriş yaparsanız herhangi bir dosya eklemenize gerek yok. Giriş yaptığınız durumda
-  otomatik olarak sepetteki ve beğenilen listenizdeki veriler üzerinden işlemler yapılır.
- **Fiyat Takibi**: ZARA sepetinizdeki ürünlerin adı, fiyatı ve URL bilgilerini çekme.
- **Excel'e Kaydetme**: (Toplanan verileri Excel dosyası olarak dışa aktarma). Bu aşama zorunlu değildir. Bilgileri anlık olarak GUİ ekranında da görüntüleyebilirsiniz.
- **Kullanıcı Dostu Arayüz**: Tkinter tabanlı grafik arayüz.

## Gereksinimler
Bu projeyi çalıştırmak için aşağıdaki yazılım ve aracılar gereklidir:

- **Python 3.8 veya daha üstü**
- **Chrome Tarayıcısı ve ChromeDriver**: Seleniumun aktif olması için gereklidir.
- **Python Kütüphaneleri**:
  - pandas
  - tkinter
  - selenium

## Kurulum
Proje kurulumunu yapmak için aşağıdaki adımları takip edin:

1. Gerekli Python kütüphanelerini yükleyin:

3. ChromeDriver'ı indirin ve sisteminizde kurulu Chrome tarayıcısı ile uyumlu sürümünü kullanın:
    - [ChromeDriver İndir](https://developer.chrome.com/docs/chromedriver/downloads?hl=tr)
    - ChromeDriver'ı bir dizine kopyalayın ve PATH çevre değişkenine ekleyin.

4. Proje dosyasını indirip çalıştırın:

## Kullanım
1. Programı başlatın ve açılan arayüzde gerekli alanları doldurun.
2. E-posta ve şifre bilgilerinizi girerek bir mağaza seçin ve hesabınızla oturum açın.
3. Aşağıdaki işlemleri gerçekleştirebilirsiniz:
    - Hesabınıza giriş yaptığınızda sepetinizdeki ürünler anlık olarak excel dosyasına eklenir. O dosyayı kaydedip sonrasında fiyat verilerindeki farklılıkları
    - gör butonuna basarsanız fiyat değişikliği oldugu durumda size blgilendirme yapılır.
    - Yeni ürün fiyatlarını çekip listeleyin.
    - Tüm verileri Excel dosyası olarak dışa aktarabilirsiniz ancak bu bir zorunluluk değildir değişimleri anlık olarak panelde görebilirsiniz..
    - Hesabınıza giriş yapıp sepetinizdeki ürünler üzerinden işlemler yapın.
    - Beğeniler listenizdeki ürünlerden fiyat düşüşü olması durumunda sepetinize ekleyin.
-NOTLAR-
Bu projede sitenin artık izin vermemesinden dolayı hesaba giriş yapamıyorum. Hesaba giriş yapılamadığından dolayı sepetteki ürünler üzerinde işlemler
gerçekleştirilemiyor.Giriş yapıldığı durumda uygulama otomatik olarak sepete gidip sepet verilerimi anlık olarak karşılaştırıyor ve fiyat düşüşleri olduğunda ya da stok güncellendiğinde beğenilen
listemdeki ürünler otomatik olarak sepete ekleniyor.
Ancak şu anda sitenin güvenlik protokolünden dolayı hesaba giriş yapıldıktan kısa süre sonra siteden çıkış yapılıyor.
Ancak Giriş yapmadan da uygulama kullanılabilir. Bunun için tek yapmanız gereken bir excel dosyası yüklemek. Uygulama dosyadaki ürünleri aratacak ve stok- fiyat durumlarını takip edecektir.

Örneğin bu dosyadaki ürünleri deneyebilirsiniz.
[v5.xlsx](https://github.com/user-attachments/files/18443642/v5.xlsx)

Program çalıştığında panel şu şekilde görülür.
<img width="446" alt="Panelin Görünümü" src="https://github.com/user-attachments/assets/d831810b-db94-4aa9-8b15-00cac2590446" />
