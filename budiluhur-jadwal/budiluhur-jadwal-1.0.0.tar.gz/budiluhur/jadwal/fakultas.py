import requests
from budiluhur import URL_DEPAN
from budiluhur import SELECT_TAG_NAME
from budiluhur import URL_POST
from bs4 import BeautifulSoup as bsoup
import json
from Levenshtein import distance

class Jadwal(object):

    dosen = ""
    matakuliah = ""
    kelompok = ""
    ruang = ""
    mulai = ""
    selesai = ""
    keterangan = ""

    data_json = ""

    STATUS_DOSEN_TIDAK_HADIR = "DOSEN TIDAK HADIR"
    STATUS_DOSEN_PENGGANTI = "PENGGANTI"
    STATUS_DOSEN_HADIR = ""

    def __init__(self, fakultas):
        # set nilai fakultas.
        self.__fakultas = fakultas
        # set data post yang akan dikirim ke server.
        self.__data_post = {SELECT_TAG_NAME:self.__fakultas}
        # ambil data mentah berupa data jadwal
        self.__jadwal_html_tabel = requests.post(URL_POST, self.__data_post).text
        self.__soup = bsoup(self.__jadwal_html_tabel, 'html.parser')
        self.__data = []
        self.__init_data()

    def __init_data(self):
        # ambil semua data jadwal berdasarkan tag td
        # lalu buang nilai "kembali" dari data yang sudah di dapat
        # dengan mengambil bagian data mulai dari index 1 sampai -2. soalnya
        # nilai pada index 1 dan index -2 adalah td yang memiliki nilai anchor "kembali".
        data = [str(i.text.replace('\xa0','')) for i in self.__soup.findAll("td")[1:-2]]
        # ambil semua data header berdasarkan tag th. data ini sebagai indikasi segmentasi
        # untuk pemotongan data jadwal dalam n (atau 8) bagian.
        head = [str(i.text.replace('\xa0','')) for i in self.__soup.findAll("th")]

        # mendapatkan jumlah pemotongan dari panjang head mula-mula
        # semua data jadwal terbagi menjadi 8 segmentasi.
        potongan = len(head)
        # memotong data-data jadwal berdasarkan jumlah segmentasinya.
        # dalam kasus ini gue motong semua data list jadwal
        # berdasarkan 8 segment. misalnya :
        # [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        # jadi :
        # [
        #    [1,2,3,4,5,6,7,8],
        #    [9,10,11,12,13,14,15,16]
        # ]
        result = [data[i:i+potongan] for i in range(0, len(data), potongan)]
        # setiap segment yang udah dipotong bakal di zip jadi kesatuan
        # dictinary lalu hasil dari zip tersebut akan di muat kedalam
        # wadah list dari self.__data.
        for list_result in result:
            self.__data.append(dict(zip(head, list_result)))

    def get_all(self):
        return self.__data

    def to_json(self):
        return json.dumps(self.__data)

    def get_from_dosen(self, nama_dosen):
        cari = []
        for i in self.__data:
            if i['Nama Dosen'].upper().replace(' ','').strip() in nama_dosen.upper().replace(' ','').strip():
                cari.append(i)
        if not cari:
            cari = [
                {
                    'result': False
                }
            ]

        self.data_json = json.dumps(cari)
        return cari


    def get_from_ruangan(self, ruangan=''):
        cari = []
        for i in self.__data:
            if  ruangan.upper() in i['Ruang'].upper():
                cari.append(i)

        if not cari:
            cari = [
                {
                    'result': False
                }
            ]
        self.data_json = json.dumps(cari)
        return cari


    def filter_kehadiran(self, keterangan="DOSEN TIDAK HADIR"):
        cari = []
        for i in self.__data:
            if 'Keterangan' in i.keys():
                if distance(keterangan.upper(), i['Keterangan']) < len(keterangan):
                    cari.append(i)
                    # print(distance(keterangan.upper(), i['Keterangan']))

        if not cari:
            cari = [
                {
                    'result': False,
                    'keterangan': 'Tidak Ada Data Yang Dimaksud',
                }
            ]

        self.data_json = json.dumps(cari)
        return cari





class Fakultas(object):
    kode_fakultas = ""
    nama_fakultas = ""
    jadwal = None

    def __init__(self):
        # ambil data html dengan get dari requests
        r = requests.get(URL_DEPAN)
        # masukan data html yang udah diambil requests
        # kedalam variabel __html. nilainya dirubah ke dalam format
        # string dengan str.
        self.__html = str(r.text)
        # sekarang waktunya mengambil nilai-nilai pada inputan select
        # pilih fakultas dengan menggunakan beautifulsoup.
        # formatnya seperti : 'nilai':'nama fakultas'
        # dari pilihan select option html.
        soup = bsoup(self.__html, 'html.parser')
        # perlu kita ketahui, kalau nilai soup.namaelement
        # adalah objek dari class bs.Element.Tag.
        # berikut ini kita akan mencari semua element yang
        # bertipe tag option. keluaran berupa list yang
        # isinya tag object option.
        select_tag = soup.findAll("option")
        # mengambil nilai dan text dari semua tag option yang di dapat
        # lalu mengubahnya ke dalam bentuk dictionary.
        self.__semua_fakultas = dict([(i['value'], i.text) for i in select_tag])

    def get_fakultas(self, kode_fakultas, jadwal=False):
        # set kode fakultas
        self.kode_fakultas = kode_fakultas
        self.__jadwal()
        self.nama_fakultas = self.__semua_fakultas['{}'.format(kode_fakultas)]
        # set nama fakultas
        if not jadwal:
            return {self.kode_fakultas:self.nama_fakultas}
        else:
            return self



    def get_all(self):
        return self.__semua_fakultas

    def get_kode_fakultas(self):
        return tuple(self.__semua_fakultas.keys())

    def get_nilai_fakultas(self):
        return tuple(self.__semua_fakultas.values())

    def to_json(self):
        return json.dumps(self.__semua_fakultas)

    def __str__(self):
        return self.nama_fakultas

    def __jadwal(self):
        if self.kode_fakultas:
            self.jadwal = Jadwal(self.kode_fakultas)
        else:
            raise Exception('Kode fakultas harus di inisialisasi')
