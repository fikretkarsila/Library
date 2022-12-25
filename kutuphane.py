#---------- Kütüphaneler ----------------#
from os import path,mkdir
from re import search
from hashlib import md5
import sys
import sqlite3
from time import sleep
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, qApp
from kutuphane_main import Ui_MainWindow
from login_panel import Ui_Form
from kayit_ol import Ui_Form_2
from sifre_unuttum import Ui_Form_3
from kullanici_bilgi import Ui_Form_4
# ---------------------------------------------------------------------------------------#

try:
    def uygulamayi_kapat():  # Burası tamamlandı.

        kapat = QMessageBox()

        kapat.setWindowTitle("Çıkış")
        kapat.setText("Uygulama kapatılsın mı ?")
        kapat.setIcon(QMessageBox.Warning)
        kapat.setWindowIcon(QIcon("Resimler/warning.png"))

        kapat.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        kapat.setDefaultButton(QMessageBox.Cancel)

        buton_x = kapat.button(QMessageBox.Yes)
        buton_x.setText("Evet")

        buton_y = kapat.button(QMessageBox.No)
        buton_y.setText("Hayır")

        kapat.exec_()

        if kapat.clickedButton() == buton_x:

            sleep(0.5)
            qApp.quit()

    if not path.exists("Database"):
        mkdir("Database")

    def tamam(baslik, icerik, isaret, resim_yol):
        tamam = QMessageBox()
        tamam.setWindowIcon(QIcon(resim_yol))
        tamam.setWindowTitle(baslik)
        tamam.setText(icerik)
        tamam.setIcon(isaret)
        tamam.setStandardButtons(QMessageBox.Yes)
        tamam.setDefaultButton(QMessageBox.Cancel)

        buton_tamam = tamam.button(QMessageBox.Yes)
        buton_tamam.setText("Tamam")

        tamam.exec_()

    def veri_sifrele(metin):
        
        return md5(metin.encode('utf-8')).hexdigest()
    #----------------------------------------------------------------------#

    class Anasayfa(QMainWindow):
        def __init__(self):
            super(Anasayfa,self).__init__()

            self.ui = Ui_Form()
            self.ui.setupUi(self)

            self.setFixedSize(424,589)
            self.setWindowTitle("Giriş Ekran") # Pencereye başlık ekledik
            self.setWindowIcon(QIcon("Resimler/user.png")) #Pencereye icon ekledik 

            #---------------------- Butona tıklandığında -------------------#
            self.ui.giris_yap.clicked.connect(self.kontrol_et)
            self.ui.sifre_unuttum.clicked.connect(self.sifre_sifirlama)
            self.ui.hesap_ac.clicked.connect(self.yeni_kayit)
            #---------------------------------------------------------------#

        def kutuphane(self,konum):

            def baglanti_2(konum):  # Burası tamamlandı.

                if not path.exists("Database"):
                    mkdir("Database")

                self.aktif_kullanici = konum.replace('.db','')

                self.baglanti = sqlite3.connect(f"Database/{konum}")
                self.cursor = self.baglanti.cursor()

                kitaplik = 'CREATE TABLE IF NOT EXISTS kitaplik(kitap_id INTEGER NOT NULL UNIQUE,kitap_okundumu INTEGER NOT NULL,kitap_adi TEXT NOT NULL,yazar_adi TEXT NOT NULL,yayinevi_id INTEGER,kitap_tur_id INTEGER,sayfa_sayisi INTEGER NOT NULL,basim_yili INTEGER NOT NULL,detay TEXT,FOREIGN KEY("kitap_tur_id") REFERENCES "kitap_turleri"("kitap_tur_id"),FOREIGN KEY("yayinevi_id") REFERENCES "yayin_evleri"("yayinevi_id") PRIMARY KEY("kitap_id" AUTOINCREMENT))'
                self.cursor.execute(kitaplik)
                self.baglanti.commit()

                yayin_evleri = 'CREATE TABLE IF NOT EXISTS yayin_evleri(yayinevi_id	INTEGER NOT NULL UNIQUE,yayinevi_adi TEXT NOT NULL,PRIMARY KEY("yayinevi_id" AUTOINCREMENT))'
                self.cursor.execute(yayin_evleri)
                self.baglanti.commit()

                kitap_turleri = 'CREATE TABLE IF NOT EXISTS kitap_turleri(kitap_tur_id INTEGER NOT NULL UNIQUE,tur_adi	TEXT NOT NULL,PRIMARY KEY("kitap_tur_id" AUTOINCREMENT))'
                self.cursor.execute(kitap_turleri)
                self.baglanti.commit()

                kutuphanem.kitap_tablo.setColumnWidth(0, 70)
                kutuphanem.kitap_tablo.setColumnWidth(1, 150)
                kutuphanem.kitap_tablo.setColumnWidth(2, 150)
                kutuphanem.kitap_tablo.setColumnWidth(3, 150)
                kutuphanem.kitap_tablo.setColumnWidth(4, 180)
                kutuphanem.kitap_tablo.setColumnWidth(5, 150)
                kutuphanem.kitap_tablo.setColumnWidth(6, 150)
                kutuphanem.kitap_tablo.setColumnWidth(7, 150)
            
            def kullanici():

                if not path.exists("Database"):
                    mkdir("Database")

                self.pencere_kutuphane.close()

                sleep(0.5)
                
                self.baglanti = sqlite3.connect("Database/b52332518761b3165c9b9f9c36f936a1.db")
                self.cursor = self.baglanti.cursor()

                self.show()
            
            def kullanici_bilgi():

                self.pencere_bilgi = QMainWindow()
                
                kullanici_sayfa = Ui_Form_4()
                kullanici_sayfa.setupUi(self.pencere_bilgi)

                self.pencere_bilgi.setFixedSize(441,437)

                self.pencere_bilgi.setWindowTitle("Kullanıcı Bilgi")
                self.pencere_bilgi.setWindowIcon(QIcon("Resimler/user.png"))

                sorgu = "SELECT SUM(sayfa_sayisi) FROM kitaplik WHERE kitap_okundumu = 0"
                self.cursor.execute(sorgu)
                sayfa_sayisi = str(self.cursor.fetchall()[0][0])

                sorgu_2 = "SELECT kitap_id FROM kitaplik WHERE kitap_okundumu = ?"
                self.cursor.execute(sorgu_2,(0,))
                okunan_kitap_sayisi = str(len(self.cursor.fetchall()))

                sorgu_3 = "SELECT kitap_id FROM kitaplik WHERE kitap_okundumu = ?"
                self.cursor.execute(sorgu_3,(1,))
                okunmayan_kitap_sayisi = str(len(self.cursor.fetchall()))

                if sayfa_sayisi == "None":
                    sayfa_sayisi = "0"

                kullanici_sayfa.ad.setText(self.kullanici_ad)
                kullanici_sayfa.soyad.setText(self.kullanici_soyad)
                kullanici_sayfa.kullanici_adi_aktif.setText(self.kullanici_adi)
                kullanici_sayfa.okunan_kitap_sayisi.setText(okunan_kitap_sayisi)
                kullanici_sayfa.okunmayan_kitap_sayisi.setText(okunmayan_kitap_sayisi)
                kullanici_sayfa.okunan_sayfa_sayisi.setText(sayfa_sayisi)

                self.pencere_bilgi.show()

            def kontrol():
                try:

                    sorgu = "SELECT * FROM kitaplik"
                    self.cursor.execute(sorgu)
                    kitap_listesi = self.cursor.fetchall()

                    if len(kitap_listesi) == 0:

                        yayin_evi_sorgu = "DELETE FROM yayin_evleri"
                        self.cursor.execute(yayin_evi_sorgu)
                        self.baglanti.commit()

                        kitap_turleri_sorgu = "DELETE FROM kitap_turleri"
                        self.cursor.execute(kitap_turleri_sorgu)
                        self.baglanti.commit()

                except Exception as ex:
                    print(f"Hata Mesajı : {ex}")
                except:
                    pass
            
            def okunacak_kitaplar_listesi():  # Burası tamamlandı.
                try:
                    kutuphanem.kitap_tablo.clearContents()  # Tabloyu temizledik.

                    sleep(0.5)

                    sorgu = "SELECT kitap_id,kitap_adi,yazar_adi,yayin_evleri.yayinevi_adi,kitap_turleri.tur_adi,sayfa_sayisi,basim_yili,detay from kitaplik INNER JOIN kitap_turleri ON kitaplik.kitap_tur_id = kitap_turleri.kitap_tur_id INNER JOIN yayin_evleri ON kitaplik.yayinevi_id = yayin_evleri.yayinevi_id Where kitap_okundumu = 1"
                    self.cursor.execute(sorgu)
                    okunacak_kitaplar = self.cursor.fetchall()

                    if len(okunacak_kitaplar) == 0:

                        tamam("Bilgi", "Okuyacak kitabınız yok.", QMessageBox.Information, "Resimler/information.png")
                    else:

                        rowIndex = 0
                        kutuphanem.kitap_tablo.setRowCount(0)

                        for yazdir in okunacak_kitaplar:
                            rowCount = kutuphanem.kitap_tablo.rowCount()  # Kaç tane eleman ekli onu söylüyor.
                            kutuphanem.kitap_tablo.insertRow(rowCount)  # Burayada rowCount indexli yere eleman ekledik.

                            kutuphanem.kitap_tablo.setItem(rowIndex, 0, QTableWidgetItem(str(yazdir[0])))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 1, QTableWidgetItem(yazdir[1]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 2, QTableWidgetItem(yazdir[2]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 3, QTableWidgetItem(yazdir[3]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 4, QTableWidgetItem(yazdir[4]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 5, QTableWidgetItem(str(yazdir[5])))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 6, QTableWidgetItem(str(yazdir[6])))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 7, QTableWidgetItem(yazdir[7]))

                            rowIndex += 1
                except Exception as ex:
                    print(f"Hata mesajı : {ex}")
                except:
                    pass

            def uygulamayi_kapat():  # Burası tamamlandı.

                kapat = QMessageBox()

                kapat.setWindowTitle("Çıkış")
                kapat.setText("Uygulama kapatılsın mı ?")
                kapat.setIcon(QMessageBox.Warning)
                kapat.setWindowIcon(QIcon("Resimler/warning.png"))

                kapat.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                kapat.setDefaultButton(QMessageBox.Cancel)

                buton_x = kapat.button(QMessageBox.Yes)
                buton_x.setText("Evet")

                buton_y = kapat.button(QMessageBox.No)
                buton_y.setText("Hayır")

                kapat.exec_()

                if kapat.clickedButton() == buton_x:
                    
                    self.baglanti.close()
                    sleep(0.5)
                    qApp.quit()

            def kitaplari_listele():  # Burası tamamlandı.

                try:

                    kutuphanem.kitap_tablo.clearContents()  # Tablo içeriğini temizledik.
                    # ---------------------------------------------------------------------------------------#
                    sorgula = "SELECT kitap_id,kitap_adi,yazar_adi,yayin_evleri.yayinevi_adi,kitap_turleri.tur_adi,sayfa_sayisi,basim_yili,detay from kitaplik INNER JOIN kitap_turleri ON kitaplik.kitap_tur_id = kitap_turleri.kitap_tur_id INNER JOIN yayin_evleri ON kitaplik.yayinevi_id = yayin_evleri.yayinevi_id"

                    self.cursor.execute(sorgula)
                    kitaplik_listesi = self.cursor.fetchall()
                    rowIndex = 0

                    sleep(0.2)

                    if len(kitaplik_listesi) == 0:

                        tamam("Bilgi", "Kütüphanenizde hiç kitap bulunmuyor.", QMessageBox.Information,
                            "Resimler/information.png")
                    else:

                        kutuphanem.kitap_tablo.setRowCount(0)

                        for yazdir in kitaplik_listesi:
                            rowCount = kutuphanem.kitap_tablo.rowCount()  # Kaç tane eleman ekli onu söylüyor.

                            kutuphanem.kitap_tablo.insertRow(rowCount)  # Burayada rowCount indexli yere eleman ekledik.

                            kutuphanem.kitap_tablo.setItem(rowIndex, 0, QTableWidgetItem(str(yazdir[0])))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 1, QTableWidgetItem(yazdir[1]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 2, QTableWidgetItem(yazdir[2]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 3, QTableWidgetItem(yazdir[3]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 4, QTableWidgetItem(yazdir[4]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 5, QTableWidgetItem(str(yazdir[5])))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 6, QTableWidgetItem(str(yazdir[6])))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 7, QTableWidgetItem(yazdir[7]))

                            rowIndex += 1

                except Exception as ex:
                    print(f"Hata mesajı : {ex}")
                except:
                    pass

            def kitap_sil_veri():  # Temiz

                try:

                    sil_kitap = kutuphanem.sil_kitap.text().strip().title()

                    # ---------------------------------------------------------------------------------------#
                    #yazılacak_bak
                    #----------------------------------------------------------------------------------------#

                    if kutuphanem.arama_id_text_2 == "Yayınevi":
                        yayin_evi_tutucu = sil_kitap
                        sorgu = "SELECT yayinevi_id FROM yayin_evleri WHERE yayinevi_adi = ?"
                        self.cursor.execute(sorgu,(sil_kitap,))
                        sorgu_sonuc = self.cursor.fetchall()

                        if len(sorgu_sonuc) == 0:
                            raise SyntaxError(tamam("Uyarı", "Yayınevine ait böyle bir kitap bulunamadı", QMessageBox.Warning, "Resimler/warning.png"))
                        else:

                            sorgu_2 = "SELECT yayinevi_id FROM kitaplik WHERE yayinevi_id = ?"
                            self.cursor.execute(sorgu_2,(sorgu_sonuc[0][0],))
                            sorgu_sonuc_2 = self.cursor.fetchall()

                            if len(sorgu_sonuc_2) == 0:
                                raise SyntaxError(tamam("Uyarı", "Yayınevine ait böyle bir kitap bulunamadı", QMessageBox.Warning,"Resimler/warning.png"))
                            else:
                                sil_kitap = str(sorgu_sonuc_2[0][0])

                    elif kutuphanem.arama_id_text_2 == "Tür":

                        kitap_turu_tutucu = sil_kitap
                        sorgu = "SELECT kitap_tur_id FROM kitap_turleri WHERE tur_adi = ?"
                        self.cursor.execute(sorgu,(sil_kitap,))
                        sorgu_sonuc = self.cursor.fetchall()

                        if len(sorgu_sonuc) == 0:
                            raise SyntaxError(
                                tamam("Uyarı", "Kitap türüne ait böyle bir kitap bulunamadı", QMessageBox.Warning,
                                    "Resimler/warning.png"))
                        else:
                            sorgu_2 = "SELECT kitap_tur_id FROM kitaplik WHERE kitap_tur_id = ?"
                            self.cursor.execute(sorgu_2,(sorgu_sonuc[0][0],))
                            sorgu_sonuc_2 = self.cursor.fetchall()

                            if len(sorgu_sonuc_2) == 0:
                                raise SyntaxError(
                                    tamam("Uyarı", "Yayınevine ait böyle bir kitap bulunamadı", QMessageBox.Warning,
                                        "Resimler/warning.png"))
                            else:
                                sil_kitap = str(sorgu_sonuc_2[0][0])
                    else:

                        sorgu = f"SELECT * FROM kitaplik WHERE {kutuphanem.arama_id_bilgi_2} = ?"
                        self.cursor.execute(sorgu, (sil_kitap,))
                        bulunan_kitaplar = self.cursor.fetchall()

                        if len(bulunan_kitaplar) == 0:

                            raise SyntaxError(tamam("Uyarı", "Böyle bir kitap bulunamadı.", QMessageBox.Warning, "Resimler/warning.png"))
                    # ---------------------------------------------------------------------------------------#
                    if len(sil_kitap) == 0:
                        tamam("Uyarı", "Boş alan bırakmayınız.", QMessageBox.Warning, "Resimler/warning.png")

                    else:
                        # ---------------------------------------------------------------------------------------#
                        if kutuphanem.arama_id_text_2 == "Id":
                            uyari_mesaji = f"{sil_kitap} numaralı Id'ye sahip kitabı silmek istediğinize emin misiniz ?"
                        elif kutuphanem.arama_id_text_2 == "Kitap Adı":
                            uyari_mesaji = f"{sil_kitap} adına sahip tüm kitaplar silinecektir emin misiniz ?"
                        elif kutuphanem.arama_id_text_2 == "Yazar Adı":
                            uyari_mesaji = f"{sil_kitap} yazar adına sahip tüm kitaplar silinecektir emin misiniz ?"
                        elif kutuphanem.arama_id_text_2 == "Yayınevi":
                            uyari_mesaji = f"{yayin_evi_tutucu} yayınevine sahip tüm kitaplar silinecektir emin misiniz ?"
                        elif kutuphanem.arama_id_text_2 == "Tür":
                            uyari_mesaji = f"{kitap_turu_tutucu} kitap türüne sahip tüm kitaplar silinecektir emin misiniz ?"
                        elif kutuphanem.arama_id_text_2 == "Basım Yılı":
                            uyari_mesaji = f"{sil_kitap} basım yılına sahip tüm kitaplar silinecektir emin misiniz ?"

                        kapat = QMessageBox()

                        kapat.setWindowTitle("Uyarı")
                        kapat.setText(uyari_mesaji)
                        kapat.setIcon(QMessageBox.Warning)
                        kapat.setWindowIcon(QIcon("Resimler/warning.png"))

                        kapat.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        kapat.setDefaultButton(QMessageBox.No)

                        buton_x = kapat.button(QMessageBox.Yes)
                        buton_x.setText("Evet")

                        buton_y = kapat.button(QMessageBox.No)
                        buton_y.setText("Hayır")

                        kapat.exec_()
                        # ---------------------------------------------------------------------------------------#
                        if kapat.clickedButton() == buton_x:
                            sleep(0.2)

                            sorgu = f"DELETE FROM kitaplik WHERE {kutuphanem.arama_id_bilgi_2} = ?"

                            self.cursor.execute(sorgu, (sil_kitap,))
                            self.baglanti.commit()

                            if kutuphanem.arama_id_text_2 == "Yayınevi":

                                sorgu_3 = "DELETE FROM yayin_evleri WHERE yayinevi_id = ?"
                                self.cursor.execute(sorgu_3, (sil_kitap,))
                                self.baglanti.commit()

                            elif kutuphanem.arama_id_text_2 == "Tür":
                                sorgu_3 = "DELETE FROM kitap_turleri WHERE kitap_tur_id = ?"
                                self.cursor.execute(sorgu_3, (sil_kitap,))
                                self.baglanti.commit()

                            tamam("Bilgi", "Silme işlemi başarılı.", QMessageBox.Information, "Resimler/information.png")

                            kutuphanem.sil_kitap.clear()  # LineEdit temizledik
                            kutuphanem.kitap_id_2.setChecked(True)
                            kutuphanem.arama_id_bilgi_2 = "kitap_id"
                            kutuphanem.arama_id_text_2 = "Id"

                            kitaplari_listele()
                # ---------------------------------------------------------------------------------------#
                except Exception as ex:
                    print(f"Hata mesajı : {ex}")
                except:
                    pass

            def kitap_ekle_veri():  # Burası Tamamlandı

                try:

                    # ---------------------------------------------------------------------------------------#
                    kitap_adi = kutuphanem.ekle_kitap_adi.text().strip().title()
                    yazar_adi = kutuphanem.ekle_yazar_adi.text().strip().title()
                    yayinevi = kutuphanem.ekle_yayinevi_id.text().strip().title()
                    kitap_turu = kutuphanem.ekle_kitap_tur_id.text().strip().title()
                    sayfa_sayisi = kutuphanem.ekle_sayfa_sayisi.text().strip()
                    basim_yili = kutuphanem.ekle_basim_yili.text().strip()
                    detay = kutuphanem.ekle_detay.text().strip()
                    # ---------------------------------------------------------------------------------------#
                    if len(kitap_adi) == 0 and len(yazar_adi) == 0 and len(yayinevi) == 0 and len(kitap_turu) == 0 and len(
                            sayfa_sayisi) == 0 and len(basim_yili) == 0:
                        raise SyntaxError(
                            tamam("Uyarı", "Boş alan bırakmayınız.", QMessageBox.Warning, "Resimler/warning.png"))

                    elif len(kitap_adi) == 0:
                        raise SyntaxError(
                            tamam("Uyarı", "Kitap adı boş bırakılamaz.", QMessageBox.Warning, "Resimler/warning.png"))

                    elif len(yazar_adi) == 0:
                        raise SyntaxError(
                            tamam("Uyarı", "Yazar adı boş bırakılamaz", QMessageBox.Warning, "Resimler/warning.png"))

                    elif len(yayinevi) == 0:
                        raise SyntaxError(
                            tamam("Uyarı", "Yayinevi boş bırakılamaz.", QMessageBox.Warning, "Resimler/warning.png"))

                    elif len(kitap_turu) == 0:
                        raise SyntaxError(
                            tamam("Uyarı", "Kitap türü boş bırakılamaz.", QMessageBox.Warning, "Resimler/warning.png"))

                    elif len(sayfa_sayisi) == 0:
                        raise SyntaxError(
                            tamam("Uyarı", "Sayfa sayısı boş bırakılamaz.", QMessageBox.Warning, "Resimler/warning.png"))

                    elif len(basim_yili) == 0:
                        raise SyntaxError(
                            tamam("Uyarı", "Basım yılı boş bırakılamaz.", QMessageBox.Warning, "Resimler/warning.png"))

                    else:

                        if search("[0-9]", yazar_adi):
                            raise SyntaxError(tamam("Uyarı", "Yazar adının içinde rakam bulunamaz.", QMessageBox.Warning,
                                                    "Resimler/warning.png"))

                        elif search("[0-9]", kitap_turu):
                            raise SyntaxError(tamam("Uyarı", "Kitap türünün içinde rakam bulunamaz.", QMessageBox.Warning,
                                                    "Resimler/warning.png"))

                        elif search("[a-z]", sayfa_sayisi) or search("[A-Z]", sayfa_sayisi):
                            raise SyntaxError(
                                tamam("Uyarı", "Sayfa sayısına sadece rakam girebilirsiniz.", QMessageBox.Warning,
                                    "Resimler/warning.png"))

                        elif search("[a-z]", basim_yili) or search("[A-Z]", basim_yili):
                            raise SyntaxError(
                                tamam("Uyarı", "Basım yılına sadece rakam girebilirsiniz.", QMessageBox.Warning,
                                    "Resimler/warning.png"))

                    # ---------------------------------------------------------------------------------------#

                    sorgu_kitap_var_mi = "SELECT kitap_id FROM kitaplik INNER JOIN yayin_evleri ON kitaplik.yayinevi_id = yayin_evleri.yayinevi_id INNER JOIN kitap_turleri ON kitaplik.kitap_tur_id = kitap_turleri.kitap_tur_id WHERE kitap_adi = ? and yazar_adi = ? and yayin_evleri.yayinevi_adi = ? and kitap_turleri.tur_adi = ? and sayfa_sayisi = ? and basim_yili = ?"
                    self.cursor.execute(sorgu_kitap_var_mi,(kitap_adi,yazar_adi,yayinevi,kitap_turu,int(sayfa_sayisi),int(basim_yili)))
                    var_mi = self.cursor.fetchall()

                    if len(var_mi) == 0:

                        sorgu = "INSERT INTO kitaplik(kitap_okundumu,kitap_adi,yazar_adi,yayinevi_id,kitap_tur_id,sayfa_sayisi,basim_yili,detay) Values(?,?,?,?,?,?,?,?)"
                        self.cursor.execute(sorgu, (kutuphanem.kitap_okudu_mu, kitap_adi, yazar_adi, 'NULL', 'NULL', sayfa_sayisi, basim_yili, detay))
                        self.baglanti.commit()

                        sorgu_yayin_evi = "SELECT yayinevi_id FROM yayin_evleri WHERE yayinevi_adi = ?"
                        self.cursor.execute(sorgu_yayin_evi,(yayinevi,))
                        yayinevi_var_mi = self.cursor.fetchall()

                        sorgu_ogren = "SELECT kitap_id FROM kitaplik WHERE kitap_adi = ? and yazar_adi = ? and sayfa_sayisi = ? and basim_yili = ?"
                        self.cursor.execute(sorgu_ogren,(kitap_adi,yazar_adi,sayfa_sayisi,basim_yili))
                        rowId_si = self.cursor.fetchall()[0][0]

                        if len(yayinevi_var_mi) != 0:
                            sorgu_guncelle = "UPDATE kitaplik SET yayinevi_id = ? WHERE kitap_id = ?"
                            c = int(yayinevi_var_mi[0][0])
                            self.cursor.execute(sorgu_guncelle, (c, rowId_si))
                            self.baglanti.commit()
                        else:

                            sorgu_sayi = "SELECT yayinevi_id FROM yayin_evleri ORDER BY yayinevi_id DESC"
                            self.cursor.execute(sorgu_sayi)
                            sayisi = self.cursor.fetchall()

                            if len(sayisi) == 0:
                                sayisi = [(0,)]

                            sorgu_ekle = "INSERT INTO yayin_evleri VALUES(?,?)"
                            self.cursor.execute(sorgu_ekle,(sayisi[0][0] + 1,yayinevi))
                            self.baglanti.commit()

                            sorgu_yayinevi_id_ekle = "UPDATE kitaplik SET yayinevi_id = ? WHERE kitap_id = ?"
                            self.cursor.execute(sorgu_yayinevi_id_ekle, (sayisi[0][0] + 1,rowId_si))
                            self.baglanti.commit()

                        sorgu_kitap_turu = "SELECT kitap_tur_id FROM kitap_turleri WHERE tur_adi = ?"
                        self.cursor.execute(sorgu_kitap_turu,(kitap_turu,))
                        kitap_turu_var_mi = self.cursor.fetchall()

                        if len(kitap_turu_var_mi) != 0:
                            sorgu_guncelle_2 = "UPDATE kitaplik SET kitap_tur_id = ? WHERE kitap_id = ?"
                            self.cursor.execute(sorgu_guncelle_2,(kitap_turu_var_mi[0][0],rowId_si))
                            self.baglanti.commit()
                        else:

                            sorgu_sayi = "SELECT kitap_tur_id FROM kitap_turleri ORDER BY kitap_tur_id DESC"
                            self.cursor.execute(sorgu_sayi)
                            sayisi = self.cursor.fetchall()

                            if len(sayisi) == 0:
                                sayisi = [(0,)]

                            sorgu_ekle_2 = "INSERT INTO kitap_turleri VALUES(?,?)"
                            hm = sayisi[0][0] + 1
                            self.cursor.execute(sorgu_ekle_2,(hm, kitap_turu))
                            self.baglanti.commit()

                            sorgu_kitap_turu_ekle = "UPDATE kitaplik SET kitap_tur_id = ? WHERE kitap_id = ?"

                            self.cursor.execute(sorgu_kitap_turu_ekle, (hm,rowId_si))
                            self.baglanti.commit()

                        sleep(0.5)
                        tamam("Bilgi", f"{kitap_adi} adlı kitap başarıyla eklendi.", QMessageBox.Information,
                            "Resimler/information.png")
                        # ---------------------------------------------------------------------------------------#
                        kutuphanem.ekle_kitap_adi.clear()  # LineEdit temizledik.
                        kutuphanem.ekle_yazar_adi.clear()  # LineEdit temizledik.
                        kutuphanem.ekle_yayinevi_id.clear()  # LineEdit temizledik.
                        kutuphanem.ekle_kitap_tur_id.clear()  # LineEdit temizledik.
                        kutuphanem.ekle_sayfa_sayisi.clear()  # LineEdit temizledik.
                        kutuphanem.ekle_basim_yili.clear()  # LineEdit temizledik.
                        kutuphanem.ekle_detay.clear()  # LineEdit temizledik.
                        kutuphanem.okundu.setChecked(True)
                        kutuphanem.kitap_okudu_mu = 0

                        kitaplari_listele()  # Kitap listesini yeniledik.
                        # -------------------------------------------------------------------------------#
                    else:
                        tamam("Uyarı","Böyle bir kitap zaten var.",QMessageBox.Warning,"Resimler/warning.png")
                except Exception as ex:
                    print(f"Hata mesajı : {ex}")
                except:
                    pass
            
            # --------------------------------------------------------------------------------#
            def veritabani_yazi():  # Yorumsuz
                rb = kutuphanem.formLayout.sender()

                if rb.isChecked():
                    kutuphanem.arama_id_bilgi_1 = rb.objectName().rstrip()
                    kutuphanem.arama_id_text_1 = rb.text().strip()

            def veritabani_yazi_2():  # Yorumsuz
                rb = kutuphanem.formLayout.sender()

                if rb.isChecked():
                    kutuphanem.arama_id_bilgi_2 = rb.objectName().rstrip("_2")
                    kutuphanem.arama_id_text_2 = rb.text().strip()

            def veritabani_yazi_3():  # Yorumsuz
                rb = kutuphanem.formLayout.sender()

                if rb.isChecked():
                    kutuphanem.arama_id_bilgi_3 = rb.objectName().rstrip("_3").lstrip("_4")
                    kutuphanem.arama_id_text_3 = rb.text().strip()
                    kutuphanem.yeni_deger.setEnabled(True)

            def veritabani_yazi_4():  # Yorumsuz
                rb = kutuphanem.groupBox_ekle.sender()

                if rb.isChecked():
                    kutuphanem.kitap_okudu_mu = 0

            def veritabani_yazi_5():  # Yorumsuz
                rb = kutuphanem.groupBox_ekle.sender()

                if rb.isChecked():
                    kutuphanem.kitap_okudu_mu = 1
            
            def veritabani_yazi_6():  # Yorumsuz
                rb = kutuphanem.formLayout.sender()

                if rb.isChecked():
                    kutuphanem.arama_id_bilgi_3 = "kitap_okundumu"
                    kutuphanem.kitap_id = 0

                    kutuphanem.yeni_deger.setEnabled(False)
                    kutuphanem.yeni_deger.clear()

            def veritabani_yazi_7():  # Yorumsuz
                rb = kutuphanem.formLayout.sender()

                if rb.isChecked():
                    kutuphanem.arama_id_bilgi_3 = "kitap_okundumu"
                    kutuphanem.kitap_id = 1

                    kutuphanem.yeni_deger.setEnabled(False)
                    kutuphanem.yeni_deger.clear()
            #----------------------------------------------------------------------------------#
            def kitap_sorgula_veri():  # Temiz

                try:

                    kitap_ara = kutuphanem.kitap_ara.text().strip()

                    if kitap_ara[0] == "i":
                        kitap_ara = "İ" + kitap_ara[2:]

                    elif kitap_ara[0] == "ı":
                        kitap_ara = "I" + kitap_ara[2:]

                    else:
                        kitap_ara = kitap_ara.title()
                        print(kitap_ara)

                    if len(kitap_ara) == 0:
                        raise Exception("bos")

                    # ---------------------------------------------------------------------------------------#
                    kutuphanem.kitap_tablo.clearContents()  # Tabloyu temizledik

                    if kutuphanem.arama_id_text_1 == "Yayınevi":

                        sorgu = f"SELECT yayinevi_id FROM yayin_evleri WHERE yayinevi_adi LIKE '%{kitap_ara}%'"
                        self.cursor.execute(sorgu)
                        yayinevi_kontrol = self.cursor.fetchall()

                        if len(yayinevi_kontrol) == 0:
                            raise SyntaxError(tamam("Uyarı", "Böyle bir yayınevi bulunamadı.", QMessageBox.Warning,"Resimler/warning.png"))
                        else:
                            yayinevi_idler = []
                            for x in yayinevi_kontrol:
                                yayinevi_idler.append(x[0])

                            sorgu = f"SELECT yayinevi_id FROM kitaplik WHERE yayinevi_id = {yayinevi_idler[0]}"
                            yayinevi_idler.pop(0)

                            for sorgu_ekle in yayinevi_idler:
                                sorgu += f' or yayinevi_id = {sorgu_ekle}'

                            self.cursor.execute(sorgu)
                            bulunan_id_kitaplar = self.cursor.fetchall()

                            bulunan_id_kitaplar = list(set(bulunan_id_kitaplar))

                            bulunan_id_kitaplar_2 = []
                            for x in bulunan_id_kitaplar:
                                bulunan_id_kitaplar_2.append(x[0])

                            if len(bulunan_id_kitaplar) == 0:
                                raise SyntaxError(tamam("Uyarı","Bu yayinevine ait kitap bulunamadı.",QMessageBox.Warning,"Resimler/warning.png"))
                            else:
                                sorgu = f'SELECT kitap_id,kitap_adi,yazar_adi,yayin_evleri.yayinevi_adi,kitap_turleri.tur_adi,sayfa_sayisi,basim_yili,detay FROM kitaplik INNER JOIN yayin_evleri ON kitaplik.yayinevi_id = yayin_evleri.yayinevi_id INNER JOIN kitap_turleri ON kitaplik.kitap_tur_id = kitap_turleri.kitap_tur_id WHERE kitaplik.yayinevi_id = {bulunan_id_kitaplar_2[0]}'
                                bulunan_id_kitaplar_2.pop(0)

                                for sorgu_ekle_2 in bulunan_id_kitaplar_2:
                                    sorgu += f" or kitaplik.yayinevi_id = {sorgu_ekle_2}"

                                self.cursor.execute(sorgu)
                                bulunan_kitaplar = self.cursor.fetchall()

                    elif kutuphanem.arama_id_text_1 == "Tür":

                        sorgu = f"SELECT kitap_tur_id FROM kitap_turleri WHERE tur_adi LIKE '%{kitap_ara}%'"
                        self.cursor.execute(sorgu)
                        kitap_tur_kontrol = self.cursor.fetchall()

                        if len(kitap_tur_kontrol) == 0:
                            raise SyntaxError(tamam("Uyarı", "Böyle bir kitap türü bulunamadı.", QMessageBox.Warning, "Resimler/warning.png"))
                        else:

                            kitap_tur_idler = []
                            for x in kitap_tur_kontrol:
                                kitap_tur_idler.append(x[0])

                            sorgu = f"SELECT kitap_tur_id FROM kitaplik WHERE kitap_tur_id = {kitap_tur_idler[0]}"
                            kitap_tur_idler.pop(0)

                            for sorgu_ekle in kitap_tur_idler:
                                sorgu += f' or kitap_tur_id = {sorgu_ekle}'

                            self.cursor.execute(sorgu)
                            bulunan_id_kitaplar = self.cursor.fetchall()

                            bulunan_id_kitaplar = list(set(bulunan_id_kitaplar))

                            bulunan_id_kitaplar_2 = []
                            for x in bulunan_id_kitaplar:
                                bulunan_id_kitaplar_2.append(x[0])

                            if len(bulunan_id_kitaplar) == 0:
                                raise SyntaxError(tamam("Uyarı","Bu kitap türüne ait kitap bulunamadı.",QMessageBox.Warning,"Resimler/warning.png"))
                            else:
                                sorgu = f'SELECT kitap_id,kitap_adi,yazar_adi,yayin_evleri.yayinevi_adi,kitap_turleri.tur_adi,sayfa_sayisi,basim_yili,detay FROM kitaplik INNER JOIN yayin_evleri ON kitaplik.yayinevi_id = yayin_evleri.yayinevi_id INNER JOIN kitap_turleri ON kitaplik.kitap_tur_id = kitap_turleri.kitap_tur_id WHERE kitaplik.kitap_tur_id = {bulunan_id_kitaplar_2[0]}'
                                bulunan_id_kitaplar_2.pop(0)

                                for sorgu_ekle_2 in bulunan_id_kitaplar_2:
                                    sorgu += f" or kitaplik.kitap_tur_id = {sorgu_ekle_2}"

                                self.cursor.execute(sorgu)
                                bulunan_kitaplar = self.cursor.fetchall()
                    else:

                        sorgu = f"SELECT kitap_id,kitap_adi,yazar_adi,yayin_evleri.yayinevi_adi,kitap_turleri.tur_adi,sayfa_sayisi,basim_yili,detay FROM kitaplik INNER JOIN yayin_evleri ON kitaplik.yayinevi_id = yayin_evleri.yayinevi_id INNER JOIN kitap_turleri ON kitaplik.kitap_tur_id = kitap_turleri.kitap_tur_id WHERE kitaplik.{kutuphanem.arama_id_bilgi_1} LIKE '{kitap_ara}%'"
                        self.cursor.execute(sorgu)
                        bulunan_kitaplar = self.cursor.fetchall()
                    # ---------------------------------------------------------------------------------------#
                    if len(bulunan_kitaplar) == 0:

                        tamam("Uyarı", "Böyle bir kitap bulunamadı.", QMessageBox.Warning, "Resimler/warning.png")
                    else:

                        tamam("Bilgi", f"{kutuphanem.arama_id_text_1} aramasında {len(bulunan_kitaplar)} kitap bulundu.",
                            QMessageBox.Information, "Resimler/information.png")

                        rowIndex = 0

                        kutuphanem.kitap_tablo.setRowCount(0)

                        for yazdir in bulunan_kitaplar:
                            rowCount = kutuphanem.kitap_tablo.rowCount()  # Kaç tane eleman ekli onu söylüyor.
                            kutuphanem.kitap_tablo.insertRow(rowCount)  # Burayada rowCount indexli yere eleman ekledik.

                            kutuphanem.kitap_tablo.setItem(rowIndex, 0, QTableWidgetItem(str(yazdir[0])))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 1, QTableWidgetItem(yazdir[1]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 2, QTableWidgetItem(yazdir[2]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 3, QTableWidgetItem(yazdir[3]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 4, QTableWidgetItem(yazdir[4]))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 5, QTableWidgetItem(str(yazdir[5])))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 6, QTableWidgetItem(str(yazdir[6])))
                            kutuphanem.kitap_tablo.setItem(rowIndex, 7, QTableWidgetItem(yazdir[7]))

                            rowIndex += 1
                        # ---------------------------------------------------------------------------------------#
                        kutuphanem.kitap_ara.clear()  # LineEdit temizledik
                        kutuphanem.kitap_id.setChecked(True)
                        kutuphanem.arama_id_bilgi_1 = "kitap_id"
                        kutuphanem.arama_id_text_1 = "Id"
                # ---------------------------------------------------------------------------------------#
                except Exception as ex:

                    if str(ex) == "bos":
                        tamam("Uyarı", "Boş alan bırakmayınız.", QMessageBox.Warning, "Resimler/warning.png")
            
            def kitap_guncelle_veri():  # Temiz
                try:

                    # -------------------------------------------------#
                    kapat = QMessageBox()

                    kapat.setWindowTitle("Uyarı")
                    kapat.setText("Güncellemek istediğinize emin misiniz ?")
                    kapat.setIcon(QMessageBox.Question)
                    kapat.setWindowIcon(QIcon("Resimler/question.png"))

                    kapat.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    kapat.setDefaultButton(QMessageBox.Cancel)

                    buton_x = kapat.button(QMessageBox.Yes)
                    buton_x.setText("Evet")

                    buton_y = kapat.button(QMessageBox.No)
                    buton_y.setText("Hayır")

                    # ------------------------------------------------#
                    id_bilgi = kutuphanem.degistir_bilgi.text().strip()

                    if kutuphanem.arama_id_bilgi_3 == "detay":
                        yeni_deger = kutuphanem.yeni_deger.text().strip()
                    else:
                        yeni_deger = kutuphanem.yeni_deger.text().strip().title()
                    # ------------------------------------------------#

                    if len(id_bilgi) == 0:
                        raise SyntaxError(
                            tamam("Uyarı", "Boş alan bırakmayınız.", QMessageBox.Warning, "Resimler/warning.png"))

                    elif search("[a-z]", id_bilgi) or search("[A-Z]", id_bilgi):

                        raise SyntaxError(tamam("Uyarı", "Id bilgisine sadece sayı girebilirsiniz.", QMessageBox.Warning,"Resimler/warning.png"))

                    if kutuphanem.arama_id_bilgi_3 == "kitap_id":

                        if len(yeni_deger) == 0:
                            raise SyntaxError(
                                tamam("Uyarı", "Yeni değer boş bırakılamaz.", QMessageBox.Warning, "Resimler/warning.png"))

                        elif search("[a-z]", yeni_deger) or search("[A-Z]", yeni_deger):

                            raise SyntaxError(tamam("Uyarı", "Id bilgisine harf giremezsiniz.", QMessageBox.Warning,
                                                    "Resimler/warning.png"))

                        sorgu = "SELECT * FROM kitaplik WHERE kitap_id = ?"
                        self.cursor.execute(sorgu,(id_bilgi,))
                        kitap_var_mi = self.cursor.fetchall()

                        if len(kitap_var_mi) == 0:
                            raise SyntaxError(tamam("Uyarı", "Bu Id'ye sahip bir kitap bulunamadı.", QMessageBox.Warning,
                                                    "Resimler/warning.png"))

                        sorgu = f"Select * from kitaplik Where kitap_id = {yeni_deger}"

                        self.cursor.execute(sorgu)
                        liste = self.cursor.fetchall()

                        if len(liste) != 0:
                            raise SyntaxError(
                                tamam("Uyarı", "Böyle bir id numarası zaten var tekrar deneyiniz.", QMessageBox.Warning,
                                    "Resimler/warning.png"))

                    elif (len(yeni_deger) == 0 or len(id_bilgi) == 0) and kutuphanem.arama_id_bilgi_3 != "kitap_okundumu":  # Sorgula bakılacak
                        raise SyntaxError(
                            tamam("Uyarı", "Boş alan bırakmayınız.", QMessageBox.Warning,
                                "Resimler/warning.png"))

                    elif kutuphanem.arama_id_bilgi_3 == "sayfa_sayisi":

                        if search("[a-z]", yeni_deger) or search("[A-Z]", yeni_deger):
                            raise SyntaxError(tamam("Uyarı", "Sayfa sayısına sadece rakam girebilirsiniz.", QMessageBox.Warning,
                                                    "Resimler/warning.png"))

                    elif kutuphanem.arama_id_bilgi_3 == "basim_yili":

                        if search("[a-z]", yeni_deger) or search("[A-Z]", yeni_deger):
                            raise SyntaxError(tamam("Uyarı", "Basım yılına sadece rakam girebilirsiniz.", QMessageBox.Warning,
                                                    "Resimler/warning.png"))

                    elif kutuphanem.arama_id_bilgi_3 == "yazar_adi":

                        if search("[0-9]", yeni_deger):
                            raise SyntaxError(tamam("Uyarı", "Yazar adının içinde rakam bulunamaz.", QMessageBox.Warning,
                                                    "Resimler/warning.png"))

                    elif kutuphanem.arama_id_text_3 == "Tür":

                        if search("[0-9]", yeni_deger):
                            raise SyntaxError(tamam("Uyarı", "Kitap türünün içinde rakam bulunamaz.", QMessageBox.Warning,
                                                    "Resimler/warning.png"))  # KİTAP TÜRÜNÜ BURADAN DEVAM EDEBİLİRSİN BAK SADECE
                    # -------------------------------------------------------------------------------------------------------------------------------#

                    sorgu = f"SELECT * FROM kitaplik WHERE kitap_id = {id_bilgi}"
                    self.cursor.execute(sorgu)
                    kitap_var_mi = self.cursor.fetchall()

                    if len(kitap_var_mi) == 0:
                        raise SyntaxError(tamam("Uyarı", "Bu Id'ye sahip bir kitap bulunamadı.", QMessageBox.Warning,
                                                "Resimler/warning.png"))

                    kapat.exec_()

                    if kutuphanem.arama_id_bilgi_3 == "kitap_okundumu" and kapat.clickedButton() == buton_x:

                        sleep(0.5)

                        sorgu = f"UPDATE kitaplik SET {kutuphanem.arama_id_bilgi_3} = ? WHERE kitap_id = ?"

                        self.cursor.execute(sorgu, (kutuphanem.kitap_id, id_bilgi))
                        self.baglanti.commit()

                        tamam("Bilgi", f"Güncelleme işlemi tamamlandı.", QMessageBox.Information,
                            "Resimler/information.png")

                        kutuphanem.degistir_bilgi.clear()
                        kutuphanem._4kitap_id_3.setChecked(True)

                        kutuphanem.arama_id_bilgi_3 = "kitap_id"
                        kutuphanem.arama_id_text_3 = "Id"

                        okunacak_kitaplar_listesi()

                    elif (kutuphanem.arama_id_text_3 == "Yayınevi") and kapat.clickedButton() == buton_x:

                        sorgu_yayinevi_var_mi = "SELECT yayinevi_id FROM yayin_evleri WHERE yayinevi_adi = ?"
                        self.cursor.execute(sorgu_yayinevi_var_mi,(yeni_deger,))
                        control_yayinevi = self.cursor.fetchall()

                        if len(control_yayinevi) == 0:

                            sorgu_kac_yayievi_var = "SELECT yayinevi_id FROM yayin_evleri ORDER BY yayinevi_id DESC"
                            self.cursor.execute(sorgu_kac_yayievi_var)
                            yayinevi_sayisi = self.cursor.fetchall()

                            if len(yayinevi_sayisi) == 0:
                                yayinevi_sayisi = 1
                            else:
                                yayinevi_sayisi = yayinevi_sayisi[0][0] + 1

                            sorgu_yayinevi_ekle = "INSERT INTO yayin_evleri(yayinevi_id,yayinevi_adi) VALUES (?,?)"
                            self.cursor.execute(sorgu_yayinevi_ekle,(yayinevi_sayisi,yeni_deger))
                            self.baglanti.commit()

                            sorgu_yayinevi_guncelle = "UPDATE kitaplik SET yayinevi_id = ? WHERE kitap_id = ?"
                            self.cursor.execute(sorgu_yayinevi_guncelle,(yayinevi_sayisi,id_bilgi))
                            self.baglanti.commit()
                        else:

                            sorgu_yayinevi_guncelle = "UPDATE kitaplik SET yayinevi_id = ? WHERE kitap_id = ?"
                            self.cursor.execute(sorgu_yayinevi_guncelle, (control_yayinevi[0][0], id_bilgi))
                            self.baglanti.commit()

                        kutuphanem.degistir_bilgi.clear()
                        kutuphanem.yeni_deger.clear()
                        kutuphanem._4kitap_id_3.setChecked(True)

                        kutuphanem.arama_id_bilgi_3 = "kitap_id"
                        kutuphanem.arama_id_text_3 = "Id"

                        tamam("Bilgi", f"Güncelleme işlemi tamamlandı.", QMessageBox.Information,
                            "Resimler/information.png")

                        kitaplari_listele()

                    elif kutuphanem.arama_id_text_3 == "Tür" and kapat.clickedButton() == buton_x:

                        sorgu_kitap_turleri_var_mi = "SELECT kitap_tur_id FROM kitap_turleri WHERE tur_adi = ?"
                        self.cursor.execute(sorgu_kitap_turleri_var_mi,(yeni_deger,))
                        control_kitap_turleri = self.cursor.fetchall()

                        if len(control_kitap_turleri) == 0:

                            sorgu_kac_kitap_turleri_var = "SELECT kitap_tur_id FROM kitap_turleri ORDER BY kitap_tur_id DESC"
                            self.cursor.execute(sorgu_kac_kitap_turleri_var)
                            kitap_turleri_sayisi = self.cursor.fetchall()

                            if len(kitap_turleri_sayisi) == 0:
                                kitap_turleri_sayisi = 1
                            else:
                                kitap_turleri_sayisi = kitap_turleri_sayisi[0][0] + 1

                            sorgu_kitap_turleri_ekle = "INSERT INTO kitap_turleri(kitap_tur_id,tur_adi) VALUES (?,?)"
                            self.cursor.execute(sorgu_kitap_turleri_ekle, (kitap_turleri_sayisi,yeni_deger))
                            self.baglanti.commit()

                            sorgu_kitap_turleri_guncelle = "UPDATE kitaplik SET kitap_tur_id = ? WHERE kitap_id = ?"
                            self.cursor.execute(sorgu_kitap_turleri_guncelle, (kitap_turleri_sayisi, id_bilgi))
                            self.baglanti.commit()
                        else:

                            sorgu_kitap_turleri_guncelle = "UPDATE kitaplik SET kitap_tur_id = ? WHERE kitap_id = ?"
                            self.cursor.execute(sorgu_kitap_turleri_guncelle, (control_kitap_turleri[0][0], id_bilgi))
                            self.baglanti.commit()

                        kutuphanem.degistir_bilgi.clear()
                        kutuphanem.yeni_deger.clear()
                        kutuphanem._4kitap_id_3.setChecked(True)

                        kutuphanem.arama_id_bilgi_3 = "kitap_id"
                        kutuphanem.arama_id_text_3 = "Id"

                        tamam("Bilgi", f"Güncelleme işlemi tamamlandı.", QMessageBox.Information,
                            "Resimler/information.png")

                        kitaplari_listele()

                    elif kapat.clickedButton() == buton_x:

                        sleep(0.5)

                        sorgu = f"UPDATE kitaplik SET {kutuphanem.arama_id_bilgi_3} = ? WHERE kitap_id = ?"

                        self.cursor.execute(sorgu, (yeni_deger, id_bilgi))
                        self.baglanti.commit()

                        kutuphanem.degistir_bilgi.clear()
                        kutuphanem.yeni_deger.clear()
                        kutuphanem._4kitap_id_3.setChecked(True)

                        kutuphanem.arama_id_bilgi_3 = "kitap_id"
                        kutuphanem.arama_id_text_3 = "Id"

                        tamam("Bilgi", f"Güncelleme işlemi tamamlandı.", QMessageBox.Information,
                            "Resimler/information.png")

                        kitaplari_listele()

                except Exception as ex:
                    print(f"Hata mesajı : {ex}")
                except:
                    pass

            #----------------------------------------------------------------------------------#
            self.pencere_kutuphane = QMainWindow()

            kutuphanem = Ui_MainWindow()
            kutuphanem.setupUi(self.pencere_kutuphane)
            
            baglanti_2(konum)

            self.pencere_kutuphane.setWindowTitle("Kütüphanem")  # Pencereye başlık ekledik
            self.pencere_kutuphane.setWindowIcon(QIcon("Resimler/bookcase.png"))  # Uygulamaya icon ekledik

            kontrol()

            kutuphanem.kitap_id.setChecked(True)
            kutuphanem.kitap_id_2.setChecked(True)
            kutuphanem._4kitap_id_3.setChecked(True)
            kutuphanem.okundu.setChecked(True)

            kutuphanem.arama_id_bilgi_1 = "kitap_id"
            kutuphanem.arama_id_text_1 = "Id"
            kutuphanem.arama_id_bilgi_2 = "kitap_id"
            kutuphanem.arama_id_text_2 = "Id"
            kutuphanem.arama_id_bilgi_3 = "kitap_id"
            kutuphanem.arama_id_text_3 = "Id"

            kutuphanem.kitap_okudu_mu = 0

            # -Butonlara-tıklandığında--------------------------------------#
            kutuphanem.exit.clicked.connect(uygulamayi_kapat)
            kutuphanem.kitap_listele.clicked.connect(kitaplari_listele)
            kutuphanem.kitap_ekle.clicked.connect(kitap_ekle_veri)
            kutuphanem.kitap_sorgula.clicked.connect(kitap_sorgula_veri)
            kutuphanem.kitap_sil.clicked.connect(kitap_sil_veri)
            kutuphanem.kitap_guncelle.clicked.connect(kitap_guncelle_veri)
            kutuphanem.okunacak_kitaplar.clicked.connect(okunacak_kitaplar_listesi)
            kutuphanem.kullanici_degistir.clicked.connect(kullanici)
            kutuphanem.kullanici_bilgi.clicked.connect(kullanici_bilgi)
            #---------------------------------------------------------------#
            # -Radio-butona-tıklandığı-zaman-----------------------------#
            kutuphanem.kitap_id.toggled.connect(veritabani_yazi)
            kutuphanem.kitap_adi.toggled.connect(veritabani_yazi)
            kutuphanem.yazar_adi.toggled.connect(veritabani_yazi)
            kutuphanem.yayinevi_id.toggled.connect(veritabani_yazi)
            kutuphanem.kitap_tur_id.toggled.connect(veritabani_yazi)
            kutuphanem.basim_yili.toggled.connect(veritabani_yazi)

            kutuphanem.kitap_id_2.toggled.connect(veritabani_yazi_2)
            kutuphanem.kitap_adi_2.toggled.connect(veritabani_yazi_2)
            kutuphanem.yazar_adi_2.toggled.connect(veritabani_yazi_2)
            kutuphanem.yayinevi_id_2.toggled.connect(veritabani_yazi_2)
            kutuphanem.kitap_tur_id_2.toggled.connect(veritabani_yazi_2)
            kutuphanem.basim_yili_2.toggled.connect(veritabani_yazi_2)

            kutuphanem._4kitap_id_3.toggled.connect(veritabani_yazi_3)
            kutuphanem.kitap_adi_3.toggled.connect(veritabani_yazi_3)
            kutuphanem.yazar_adi_3.toggled.connect(veritabani_yazi_3)
            kutuphanem.yayinevi_id_3.toggled.connect(veritabani_yazi_3)
            kutuphanem.kitap_tur_id_3.toggled.connect(veritabani_yazi_3)
            kutuphanem.sayfa_sayisi_3.toggled.connect(veritabani_yazi_3)
            kutuphanem.basim_yili_3.toggled.connect(veritabani_yazi_3)
            kutuphanem.detay_3.toggled.connect(veritabani_yazi_3)
            kutuphanem.okundu_3.toggled.connect(veritabani_yazi_6)
            kutuphanem.okunmadi_3.toggled.connect(veritabani_yazi_7)

            #------------------------------------------------------------#
            kutuphanem.okundu.toggled.connect(veritabani_yazi_4)
            kutuphanem.okunmadi.toggled.connect(veritabani_yazi_5)
            # -----------------------------------------------------------#
            self.pencere_kutuphane.setMinimumSize(1571,800)
            sleep(0.5)
            self.pencere_kutuphane.show()
        #------------------------------------ Veri tabanı bağlantısı sağlandı.
        def baglanti(self):

            if not path.exists("Database"):
                mkdir("Database")

            self.baglanti = sqlite3.connect("Database/b52332518761b3165c9b9f9c36f936a1.db")
            self.cursor = self.baglanti.cursor()

            sorgu = 'CREATE TABLE IF NOT EXISTS tum_kullanicilar(kullanici_id INTEGER NOT NULL UNIQUE,tc_no TEXT NOT NULL UNIQUE,kullanici_adi TEXT NOT NULL UNIQUE,kullanici_ad TEXT NOT NULL,kullanici_soyad TEXT NOT NULL,sifre TEXT NOT NULL,PRIMARY KEY("kullanici_id" AUTOINCREMENT))'
            self.cursor.execute(sorgu)
            self.baglanti.commit()
        #----------------------------------------------------------------------#
        def kontrol_et(self):

            try:
                sorgu = "SELECT kullanici_adi,sifre FROM tum_kullanicilar"
                self.cursor.execute(sorgu)
                kullanici_bilgileri = self.cursor.fetchall()

                if len(kullanici_bilgileri) == 0:
                    raise SyntaxError(tamam("Uyarı","Kayıtlı kullanıcı bulunamadı lütfen yeni kayıt oluşturunuz.",QMessageBox.Warning,"Resimler/warning.png"))
                else:
                    kullanici_adi = veri_sifrele(self.ui.kullanici_adi.text().strip())
                    sifre = veri_sifrele(self.ui.sifre.text().strip())

                    if len(kullanici_adi) == 0 or len(sifre) == 0:
                        raise SyntaxError(tamam("Uyarı","Boş alan bırakmayınız.",QMessageBox.Warning,"Resimler/warning.png"))
                    else:

                        kontrol = False

                        for kullanici in kullanici_bilgileri:

                            if kullanici[0] == kullanici_adi and kullanici[1] == sifre:
                                kontrol = True

                        if kontrol:
                            
                            self.hide()

                            sorgu_bilgiler = "SELECT kullanici_ad,kullanici_soyad FROM tum_kullanicilar WHERE kullanici_adi = ? and sifre = ?"
                            self.cursor.execute(sorgu_bilgiler,(kullanici_adi,sifre))
                            kullanici_blg = self.cursor.fetchone()

                            self.kullanici_ad = kullanici_blg[0]
                            self.kullanici_soyad = kullanici_blg[1]
                            self.kullanici_adi = self.ui.kullanici_adi.text().strip()
                        
                            self.kutuphane(f"{kullanici_adi}.db")

                            self.ui.kullanici_adi.clear()
                            self.ui.sifre.clear()
                        else:

                            raise SyntaxError(tamam("Uyarı","Kullanıcı adı ve/veya şifre yanlış.",QMessageBox.Warning,"Resimler/warning.png"))

            except Exception as ex:
                print(f"Hata mesajı : {ex}")
            except:
                pass
        #-----------------------------------------------------------------------------------#
        def sifre_sifirlama(self):

            def sayfa_geri_don():

                self.pencere_sifre_unuttum.close()
                self.show()

            def kaydet_kontrol():

                try:

                    tc_no = sifre_unuttum_sayfasi.tc_no.text().strip()
                    kullanici_adi = sifre_unuttum_sayfasi.kullanici_adi.text().strip()
                    sifre = sifre_unuttum_sayfasi.yeni_sifre.text().strip()
                    sifre_tekrari = sifre_unuttum_sayfasi.yeni_sifre_tekrari.text().strip()

                    if len(tc_no) == 0:
                        sifre_unuttum_sayfasi.hata_mesaji.setText("TC Kimlik numarası boş bırakılamaz.")
                        sifre_unuttum_sayfasi.tc_kontrol.setText("*")
                        raise SyntaxError()

                    elif len(kullanici_adi) == 0:
                        sifre_unuttum_sayfasi.hata_mesaji.setText("Kullanıcı adı boş bırakılamaz.")
                        sifre_unuttum_sayfasi.kullanici_adi_kontrol.setText("*")
                        raise SyntaxError()

                    elif len(sifre) == 0:
                        sifre_unuttum_sayfasi.hata_mesaji.setText("Şifre boş bırakılamaz.")
                        sifre_unuttum_sayfasi.sifre_kontrol.setText("*")
                        raise SyntaxError()

                    elif len(sifre_tekrari) == 0:
                        sifre_unuttum_sayfasi.hata_mesaji.setText("Şifre tekarı boş bırakılamaz.")
                        sifre_unuttum_sayfasi.sifre_tekrari_kontrol.setText("*")
                        raise SyntaxError()
                    else:

                        sifre_unuttum_sayfasi.hata_mesaji.clear()
                        sifre_unuttum_sayfasi.tc_kontrol.clear()
                        sifre_unuttum_sayfasi.kullanici_adi_kontrol.clear()
                        sifre_unuttum_sayfasi.sifre_kontrol.clear()
                        sifre_unuttum_sayfasi.sifre_tekrari_kontrol.clear()
                    
                    if search("[a-z]",tc_no) or search("[A-Z]",tc_no):
                        sifre_unuttum_sayfasi.hata_mesaji.setText("TC Kimlik numarasında harf olamaz.")
                        sifre_unuttum_sayfasi.tc_kontrol.setText("*")
                        raise SyntaxError()

                    elif search(" ",tc_no):
                        sifre_unuttum_sayfasi.hata_mesaji.setText("TC Kimlik numarasında boşluk karakteri girilemez.")
                        sifre_unuttum_sayfasi.tc_kontrol.setText("*")
                        raise SyntaxError()

                    elif not (len(tc_no) == 11):
                        sifre_unuttum_sayfasi.hata_mesaji.setText("TC Kimlik numarası 11 karakterli olmalıdır.")
                        sifre_unuttum_sayfasi.tc_kontrol.setText("*")
                        raise SyntaxError()

                    elif search(" ",kullanici_adi):
                        sifre_unuttum_sayfasi.hata_mesaji.setText("Kullanıcı adına boşluk karakteri girilemez.")
                        sifre_unuttum_sayfasi.kullanici_adi_kontrol.setText("*")
                        raise SyntaxError()

                    elif search(" ",sifre):
                        sifre_unuttum_sayfasi.hata_mesaji.setText("Şifreye boşluk karakteri girilemez.")
                        sifre_unuttum_sayfasi.sifre_kontrol.setText("*")
                        raise SyntaxError()

                    elif len(sifre) < 8:
                        sifre_unuttum_sayfasi.hata_mesaji.setText("Şifre en az 8 karakterli olmalıdır.")
                        sifre_unuttum_sayfasi.sifre_kontrol.setText("*")
                        raise SyntaxError()

                    elif not (sifre == sifre_tekrari):

                        sifre_unuttum_sayfasi.hata_mesaji.setText("Şifreler uyuşmuyor.")
                        sifre_unuttum_sayfasi.sifre_kontrol.setText("*")
                        sifre_unuttum_sayfasi.sifre_tekrari_kontrol.setText("*")
                        raise SyntaxError()
                    else:

                        sifre_unuttum_sayfasi.hata_mesaji.clear()
                        sifre_unuttum_sayfasi.tc_kontrol.clear()
                        sifre_unuttum_sayfasi.kullanici_adi_kontrol.clear()
                        sifre_unuttum_sayfasi.sifre_kontrol.clear()
                        sifre_unuttum_sayfasi.sifre_tekrari_kontrol.clear()

                    sorgu = "SELECT kullanici_id,sifre FROM tum_kullanicilar WHERE tc_no = ? and kullanici_adi = ?"
                    self.cursor.execute(sorgu,(veri_sifrele(tc_no),veri_sifrele(kullanici_adi)))
                    kullanici_bilgi = self.cursor.fetchall()

                    if len(kullanici_bilgi) == 0:

                        sifre_unuttum_sayfasi.hata_mesaji.setText("TC Kimlik numarası ve/veya kullanıcı adı uyuşmuyor.")
                        sifre_unuttum_sayfasi.tc_kontrol.setText("*")
                        sifre_unuttum_sayfasi.kullanici_adi_kontrol.setText("*")
                    else:
                        sleep(0.5)

                        sifre_unuttum_sayfasi.hata_mesaji.clear()
                        sifre_unuttum_sayfasi.tc_kontrol.clear()
                        sifre_unuttum_sayfasi.kullanici_adi_kontrol.clear()

                        sorgu_guncelle = f"UPDATE tum_kullanicilar SET sifre = '{veri_sifrele(sifre)}' WHERE kullanici_id = ?"
                        self.cursor.execute(sorgu_guncelle,(kullanici_bilgi[0][0],))
                        self.baglanti.commit()

                        tamam("Bilgi","Şifre başarıyla değiştirildi.",QMessageBox.Information,"Resimler/information.png")

                        self.pencere_sifre_unuttum.close()
                        self.show()

                except Exception as ex:
                    print(f"Hata mesajı : {ex}")
                except:
                    pass
            
            self.pencere_sifre_unuttum = QMainWindow()

            sifre_unuttum_sayfasi = Ui_Form_3()
            sifre_unuttum_sayfasi.setupUi(self.pencere_sifre_unuttum)

            self.pencere_sifre_unuttum.setFixedSize(441,581)

            self.pencere_sifre_unuttum.setWindowTitle("Şifre Yenile")
            self.pencere_sifre_unuttum.setWindowIcon(QIcon("Resimler/user.png"))

            sifre_unuttum_sayfasi.kaydet.clicked.connect(kaydet_kontrol)
            sifre_unuttum_sayfasi.geri_don.clicked.connect(sayfa_geri_don)

            self.ui.kullanici_adi.clear()
            self.ui.sifre.clear()

            self.hide()
            self.pencere_sifre_unuttum.show()
        #-----------------------------------------------------------------------------------#
        def yeni_kayit(self):

            self.ui.kullanici_adi.clear()
            self.ui.sifre.clear()
            #------------------------------------- Kayıt kontrol edildi..
            def kontrol_et():
                try:
                    tc_no = kayit_sayfasi.tc_no.text().strip()
                    ad = kayit_sayfasi.ad.text().strip().title()
                    soyad = kayit_sayfasi.soyad.text().strip().title()
                    kullanici_adi = kayit_sayfasi.yeni_kullanici_adi.text().strip()
                    sifre = kayit_sayfasi.yeni_sifre.text().strip()
                    sifre_tekrari = kayit_sayfasi.yeni_sifre_tekrari.text().strip()

                    if len(tc_no) == 0:
                        kayit_sayfasi.hata_mesaji.setText("TC Kimlik numarası boş bırakılamaz.")
                        kayit_sayfasi.tc_kontrol.setText("*")
                        raise SyntaxError()
                    
                    elif len(ad) == 0:
                        kayit_sayfasi.hata_mesaji.setText("Ad boş bırakılamaz.")
                        kayit_sayfasi.ad_kontrol.setText("*")
                        raise SyntaxError()

                    elif len(soyad) == 0:
                        kayit_sayfasi.hata_mesaji.setText("Soyad boş bırakılamaz.")
                        kayit_sayfasi.soyad_kontrol.setText("*")
                        raise SyntaxError()

                    elif len(kullanici_adi) == 0:
                        kayit_sayfasi.hata_mesaji.setText("Kullanıcı adı boş bırakılamaz.")
                        kayit_sayfasi.kullanici_adi_kontrol.setText("*")
                        raise SyntaxError()

                    elif len(sifre) == 0:
                        kayit_sayfasi.hata_mesaji.setText("Şifre boş bırakılamaz.")
                        kayit_sayfasi.sifre_kontrol.setText("*")
                        raise SyntaxError()

                    elif len(sifre_tekrari) == 0:
                        kayit_sayfasi.hata_mesaji.setText("Şifre tekarı boş bırakılamaz.")
                        kayit_sayfasi.sifre_tekrari_kontrol.setText("*")
                        raise SyntaxError()
                    else:

                        kayit_sayfasi.hata_mesaji.clear()
                        kayit_sayfasi.tc_kontrol.clear()
                        kayit_sayfasi.ad_kontrol.clear()
                        kayit_sayfasi.soyad_kontrol.clear()
                        kayit_sayfasi.kullanici_adi_kontrol.clear()
                        kayit_sayfasi.sifre_kontrol.clear()
                        kayit_sayfasi.sifre_tekrari_kontrol.clear()

                    if search("[a-z]",tc_no) or search("[A-Z]",tc_no):
                        kayit_sayfasi.hata_mesaji.setText("TC Kimlik numarasında harf olamaz.")
                        kayit_sayfasi.tc_kontrol.setText("*")
                        raise SyntaxError()

                    elif search(" ",tc_no):
                        kayit_sayfasi.hata_mesaji.setText("TC Kimlik numarasında boşluk karakteri girilemez.")
                        kayit_sayfasi.tc_kontrol.setText("*")
                        raise SyntaxError()

                    elif not (len(tc_no) == 11):
                        kayit_sayfasi.hata_mesaji.setText("TC Kimlik numarası 11 karakterli olmalıdır.")
                        kayit_sayfasi.tc_kontrol.setText("*")
                        raise SyntaxError()

                    elif search("[0-9]",ad):
                        kayit_sayfasi.hata_mesaji.setText("Ad içinde rakam bulunamaz.")
                        kayit_sayfasi.ad_kontrol.setText("*")
                        raise SyntaxError()

                    elif search("[0-9]",soyad):
                        kayit_sayfasi.hata_mesaji.setText("Soyad içinde rakam bulunamaz.")
                        kayit_sayfasi.soyad_kontrol.setText("*")
                        raise SyntaxError()

                    elif search(" ",kullanici_adi):
                        kayit_sayfasi.hata_mesaji.setText("Kullanıcı adına boşluk karakteri girilemez.")
                        kayit_sayfasi.kullanici_adi_kontrol.setText("*")
                        raise SyntaxError()

                    elif search(" ",sifre):
                        kayit_sayfasi.hata_mesaji.setText("Şifreye boşluk karakteri girilemez.")
                        kayit_sayfasi.sifre_kontrol.setText("*")
                        raise SyntaxError()

                    elif len(sifre) < 8:
                        kayit_sayfasi.hata_mesaji.setText("Şifre en az 8 karakterli olmalıdır.")
                        kayit_sayfasi.sifre_kontrol.setText("*")
                        raise SyntaxError()

                    elif not (sifre == sifre_tekrari):

                        kayit_sayfasi.hata_mesaji.setText("Şifreler uyuşmuyor.")
                        kayit_sayfasi.sifre_kontrol.setText("*")
                        kayit_sayfasi.sifre_tekrari_kontrol.setText("*")
                        raise SyntaxError()
                    else:

                        kayit_sayfasi.hata_mesaji.clear()
                        kayit_sayfasi.tc_kontrol.clear()
                        kayit_sayfasi.kullanici_adi_kontrol.clear()
                        kayit_sayfasi.sifre_kontrol.clear()
                        kayit_sayfasi.sifre_tekrari_kontrol.clear()

                    sorgu = "SELECT kullanici_adi FROM tum_kullanicilar WHERE kullanici_adi = ?"
                    self.cursor.execute(sorgu,(kullanici_adi,))
                    kullanici_var_mi = self.cursor.fetchall()

                    sorgu_2 = "SELECT tc_no FROM tum_kullanicilar WHERE tc_no = ?"
                    self.cursor.execute(sorgu_2,(tc_no,))
                    tc_no_var_mi = self.cursor.fetchall()

                    if len(tc_no_var_mi) != 0:
                        
                        kayit_sayfasi.tc_kontrol.setText("*")
                        kayit_sayfasi.hata_mesaji.setText("TC kimlik numarası ile zaten kayıt var.")
                        raise SyntaxError()

                    if len(kullanici_var_mi) == 0:

                        sorgu = "INSERT INTO tum_kullanicilar(tc_no,kullanici_adi,kullanici_ad,kullanici_soyad,sifre) VALUES (?,?,?,?,?)"
                        self.cursor.execute(sorgu,(veri_sifrele(tc_no),veri_sifrele(kullanici_adi),ad,soyad,veri_sifrele(sifre)))
                        self.baglanti.commit()

                        tamam("Bilgi","Yeni kayıt oluşturuldu.",QMessageBox.Information,"Resimler/information.png")

                        self.pencere.close()
                        self.show()
                    else:

                        kayit_sayfasi.kullanici_adi_kontrol.setText("*")
                        kayit_sayfasi.hata_mesaji.setText("Böyle bir kullanıcı zaten var.")
                        raise SyntaxError()

                except Exception as ex:
                    print(f"Hata mesajı : {ex}")
                except:
                    pass
            #---------------------------------------------------------------------------------------------------#
            #-------------------------- Geri dön butonu kodları
            def sayfa_geri_don():

                self.pencere.close()
                self.show()
            #--------------------------------------------------#

            self.pencere = QMainWindow()

            kayit_sayfasi = Ui_Form_2()
            kayit_sayfasi.setupUi(self.pencere)

            self.pencere.setFixedSize(461, 651)
            self.pencere.setWindowTitle("Kayıt Ekran") # Pencereye başlık ekledik
            self.pencere.setWindowIcon(QIcon("Resimler/user.png")) #Pencereye icon ekledik

            self.hide()
            self.pencere.show()

            kayit_sayfasi.kayit_ol.clicked.connect(kontrol_et)
            kayit_sayfasi.geri_don.clicked.connect(sayfa_geri_don)
        
    # ------------------------------------------------------------------------------------------------------------#
    application = QApplication(sys.argv)
    window = Anasayfa()
    window.baglanti()
    window.show()
    sys.exit(application.exec_())

except Exception as ex:
    print(f"Hata mesajı : {ex}")
except:
    pass