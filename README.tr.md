# Sentinel Node

Sensör ve sinyal verilerini toplamak, işlemek ve paylaşmak için uç düğüm (edge node) yazılımı.

**Diğer diller:** [English](README.md)

---

## Genel Bakış

Sentinel Node, Atlas Defence ekosistemi içinde dağıtık cihazlarda çalışacak şekilde tasarlanmış hafif bir edge yazılımıdır. Sensörlerden ve sinyal kaynaklarından veri toplar, veriyi yerelde işler ve yapılandırılmış çıktıları diğer düğümlerle veya merkezi sistemlerle paylaşır.

Amaç; basit ve modüler bileşenlerle, merkeziyetsiz, ölçeklenebilir ve dayanıklı izleme ağları oluşturmaktır.

---

## Özellikler

- Çok kaynaklı veri toplama (RF, çevresel, ses, özel sensörler)
- Yerel işlem ve filtreleme
- Gerçek zamanlı olay (event) üretimi
- Hafif ve kaynak dostu
- Modüler eklenti (plugin) sistemi
- Düğümler arası güvenli veri iletimi
- Çevrimdışı / kesintili bağlantıda çalışabilme

---

## Mimari

```
[ Sensörler / Girdiler ]
(RF / Audio / Env / Özel)
↓
Veri Alma Katmanı
↓
İşleme Motoru
(Filtreleme / Tespit)
↓
Olay & Veri Katmanı
↓
Çıktı (API / Ağ / Depolama)
```

---

## Desteklenen Donanım

- Raspberry Pi (önerilir)
- Linux tabanlı edge cihazlar
- ESP32 (deneysel entegrasyon)
- SDR cihazları (RTL-SDR, HackRF)
- USB / GPIO sensörleri

---

## Hızlı Başlangıç

### Gereksinimler

- Linux (Ubuntu / Debian tercih edilir)
- Python 3.10+
- Opsiyonel: SDR sürücüleri, sensör kütüphaneleri

### Kurulum

```bash
git clone https://github.com/atlas-defence/sentinel-node.git
cd sentinel-node
pip install -r requirements.txt
```

### Çalıştırma

```bash
copy config.example.yaml config.yaml
python main.py --config config.yaml
```

---

## Yapılandırma

Yapılandırma basit JSON/YAML dosyaları ile yapılır:

```json
{
  "node_id": "node-001",
  "modules": ["rf", "audio"],
  "output": "local"
}
```

---

## Modüller

- `rf/` — RF sinyal alma ve işleme
- `audio/` — ses tabanlı tespit
- `env/` — çevresel sensörler
- `core/` — işleme motoru
- `network/` — düğümden düğüme iletişim

---

## API

Yapılandırmada etkinse (varsayılan), düğüm küçük bir HTTP API başlatır:

- `GET /health`
- `GET /events?limit=50`
- `POST /ingest` (düğümler arası event alımı; opsiyonel `X-Sentinel-Signature` HMAC)

---

## Notlar

- Bu repodaki yerleşik `rf`, `audio` ve `env` modülleri **çalışan yer tutuculardır** (sentetik örnekler üretir). İhtiyacınıza göre gerçek sensör/SDR entegrasyonlarıyla değiştirin.
- Harici eklenti eklemek için `modules` listesine `your_package.your_module:create` formatında değer ekleyin.

---

## Kullanım Senaryoları

- Dağıtık sensör ağları
- Sinyal izleme sistemleri
- Çevresel veri toplama
- Edge AI denemeleri
- Merkeziyetsiz güvenlik sistemleri

---

## Felsefe

Sentinel Node şu prensiplerle tasarlanmıştır:

- **Basit** — kurulumu ve anlaşılması kolay
- **Modüler** — özel sensörlerle genişletilebilir
- **Merkeziyetsiz** — tek hata noktası yok
- **Açık** — tamamen şeffaf ve geliştirilebilir

---

## Katkı

Katkılar memnuniyetle karşılanır. Modülleri iyileştirmek veya yeni entegrasyonlar eklemek için issue açabilir ya da pull request gönderebilirsiniz.

---

## Lisans

MIT Lisansı

