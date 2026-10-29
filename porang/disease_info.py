"""Basis pengetahuan penyakit daun porang untuk halaman hasil diagnosis."""

# Ikon memakai nama Material Symbols Outlined.
DISEASE_INFO = {
    "DAUN SEHAT": {
        "display_name": "Daun Sehat",
        "latin": "Amorphophallus muelleri - jaringan daun normal",
        "category": "Tidak Ada Patogen Terdeteksi",
        "short": "Tidak ditemukan indikasi penyakit pada helaian daun.",
        "impact_title": "Dampak terhadap Akumulasi Glukomanan:",
        "impact": (
            "Jaringan daun berada pada kondisi optimal. Proses fotosintesis berjalan "
            "maksimal sehingga sintesis glukomanan pada umbi porang dapat berlangsung "
            "tanpa hambatan. Pertahankan pola perawatan saat ini."
        ),
        "confidence_note": (
            "Tidak ditemukan titik lesi signifikan. Warna klorofil dan struktur "
            "helaian daun berada pada rentang normal."
        ),
        "metrics": [
            {"label": "Risiko Penularan", "value": "Rendah", "note": "Tidak Menular", "tone": "optimal"},
            {"label": "Organ Terdampak", "value": "Tidak Ada", "note": "Jaringan Utuh", "tone": "optimal"},
            {"label": "Potensi Defisit Umbi", "value": "0%", "note": "Bobot Panen Optimal", "tone": "optimal"},
        ],
        "symptoms": [
            {
                "icon": "bubble_chart",
                "title": "Tanda Morfologi Daun",
                "text": (
                    "Helaian daun berwarna hijau merata, permukaan licin, dan tidak "
                    "ditemukan bercak nekrotik maupun halo klorotik. Tulang daun tampak "
                    "tegak dan jaringan tetap elastis."
                ),
                "note": "Pola Diagnostik: Normal Foliage Pattern",
            },
            {
                "icon": "water_drop",
                "title": "Keseimbangan Air & Nutrisi",
                "text": (
                    "Turgor sel terjaga dengan baik. Tidak ada indikasi kekurangan "
                    "unsur hara makro maupun mikro yang tampak dari warna daun."
                ),
                "note": "Status: Kondisi Fisiologis Baik",
            },
            {
                "icon": "eco",
                "title": "Aktivitas Fotosintesis",
                "text": (
                    "Luas daun efektif untuk menangkap cahaya berada pada tingkat "
                    "maksimal. Ini mendukung translokasi karbohidrat menuju umbi."
                ),
                "note": "Estimasi: Efisiensi Fotosintesis Optimal",
            },
        ],
        "recommendations": [
            {
                "tag": "Perawatan Rutin",
                "tone": "primary",
                "icon": "science",
                "title": "Pemupukan Berimbang",
                "text": (
                    "Aplikasikan pupuk kandang matang dan NPK berimbang secara berkala "
                    "untuk menjaga vigor tanaman pada fase vegetatif."
                ),
                "details": [
                    {"label": "Dosis Anjuran:", "value": "NPK 15-15-15, 10 gr/tanaman"},
                    {"label": "Waktu Aplikasi:", "value": "Setiap 30 hari"},
                    {"label": "Interval:", "value": "Sesuai fase vegetatif"},
                ],
                "footnote": "*Hindari pemupukan berlebih saat curah hujan tinggi.",
            },
            {
                "tag": "Organik Berkelanjutan",
                "tone": "secondary",
                "icon": "eco",
                "title": "Pupuk Organik & Mulsa",
                "text": (
                    "Tambahkan kompos atau pupuk organik matang di sekitar perakaran "
                    "untuk menjaga struktur tanah dan kelembapan mikro."
                ),
                "details": [
                    {"label": "Bahan:", "value": "Kompos matang / pupuk kandang"},
                    {"label": "Aplikasi Tanah:", "value": "2-3 kg per rumpun"},
                    {"label": "Fungsi:", "value": "Menjaga kesuburan tanah"},
                ],
                "footnote": "*Pastikan bahan organik benar-benar matang agar tidak memicu jamur.",
            },
            {
                "tag": "Monitoring",
                "tone": "neutral",
                "icon": "yard",
                "title": "Pemantauan Berkala",
                "text": (
                    "Lakukan inspeksi mingguan pada permukaan atas dan bawah daun, "
                    "terutama setelah hujan berkepanjangan."
                ),
                "details": [
                    {"label": "Frekuensi:", "value": "1-2 kali per minggu"},
                    {"label": "Fokus:", "value": "Bercak baru & perubahan warna"},
                    {"label": "Tindakan:", "value": "Catat temuan lapangan"},
                ],
                "footnote": "*Deteksi dini mempercepat penanganan dan menekan kerugian.",
            },
        ],
        "prevention": [
            {
                "icon": "grid_goldenratio",
                "title": "Jarak Tanam Ideal",
                "text": (
                    "Pertahankan jarak tanam 50 cm x 60 cm agar sirkulasi udara tetap "
                    "baik dan kelembapan tajuk tidak berlebihan."
                ),
            },
            {
                "icon": "water_drop",
                "title": "Drainase Guludan",
                "text": (
                    "Pastikan parit dan guludan mampu mengalirkan air dengan lancar "
                    "sehingga tidak ada genangan di sekitar perakaran."
                ),
            },
            {
                "icon": "sunny",
                "title": "Naungan Terkontrol",
                "text": (
                    "Atur intensitas naungan pada kisaran 40%-50% agar tanaman "
                    "mendapat cahaya cukup tanpa stres panas berlebih."
                ),
            },
        ],
    },
    "HAWAR DAUN": {
        "display_name": "Hawar Daun",
        "latin": "Phytophthora sp. / Xanthomonas sp.",
        "category": "Klasifikasi Patogen Terdeteksi",
        "short": "Terdeteksi gejala hawar daun yang menyerang jaringan hijau.",
        "impact_title": "Dampak terhadap Akumulasi Glukomanan:",
        "impact": (
            "Hawar daun merusak jaringan fotosintesis aktif dan mempercepat layu "
            "helaian. Jika tidak segera ditangani, <strong>efisiensi fotosintesis "
            "dapat turun hingga -30%</strong> sehingga pembentukan glukomanan pada "
            "umbi terhambat secara signifikan."
        ),
        "confidence_note": (
            "Model mendeteksi pola bercak basah dan nekrosis pada area daun yang "
            "konsisten dengan gejala hawar."
        ),
        "metrics": [
            {"label": "Kecepatan Penularan", "value": "Cepat", "note": "Air & Tanah", "tone": "critical"},
            {"label": "Organ Terdampak", "value": "Daun & Tangkai", "note": "Helaian & Petiola", "tone": "moderate"},
            {"label": "Potensi Defisit Umbi", "value": "20% - 40%", "note": "Bobot Panen Akhir", "tone": "critical"},
        ],
        "symptoms": [
            {
                "icon": "bubble_chart",
                "title": "Bercak Basah Membesar",
                "text": (
                    "Muncul bercak kebasahan tidak beraturan yang cepat melebar. "
                    "Jaringan di dalam bercak berubah cokelat gelap dan terasa lunak."
                ),
                "note": "Pola Diagnostik: Water-Soaked Lesion",
            },
            {
                "icon": "dew_point",
                "title": "Faktor Pemicu Utama",
                "text": (
                    "Kelembapan tinggi (<strong>RH &gt; 85%</strong>), drainase buruk, "
                    "dan genangan air di sekitar perakaran mempercepat infeksi."
                ),
                "note": "Mikroklimat lembap mempercepat penyebaran patogen.",
                "note_tone": "moderate",
            },
            {
                "icon": "air",
                "title": "Pola Penyebaran",
                "text": (
                    "Patogen menyebar melalui percikan air hujan, air irigasi, dan "
                    "tanah yang terkontaminasi. Alat pertanian juga dapat menjadi "
                    "vektor transmisi antar guludan."
                ),
                "note": "Vektor Primer: Air & Tanah Terkontaminasi",
            },
        ],
        "recommendations": [
            {
                "tag": "Opsi Cepat / Kimia",
                "tone": "primary",
                "icon": "science",
                "title": "Fungisida Sistemik Presisi",
                "text": (
                    "Gunakan fungisida berbahan aktif <strong>Mankozeb 80%</strong> atau "
                    "<strong>Dimetomorf 50%</strong> untuk menekan pertumbuhan patogen."
                ),
                "details": [
                    {"label": "Dosis Anjuran:", "value": "1.5 - 2.0 gram/Liter air"},
                    {"label": "Waktu Semprot:", "value": "06:30 - 08:30 WIB"},
                    {"label": "Interval:", "value": "Ulangi tiap 7 hari (maks 3x)"},
                ],
                "footnote": "*Semprot merata pada permukaan atas dan bawah daun.",
            },
            {
                "tag": "Organik Berkelanjutan",
                "tone": "secondary",
                "icon": "eco",
                "title": "Agens Hayati Tanah",
                "text": (
                    "Aplikasikan <strong>Trichoderma harzianum</strong> pada pangkal "
                    "tanaman untuk menekan patogen tular tanah secara alami."
                ),
                "details": [
                    {"label": "Agens Hayati:", "value": "Trichoderma harzianum"},
                    {"label": "Aplikasi Tanah:", "value": "20 gr/tanaman"},
                    {"label": "Fungsi:", "value": "Kompetitor alami patogen"},
                ],
                "footnote": "*Aman terhadap struktur mikroba tanah dan residu umbi.",
            },
            {
                "tag": "Manajemen Lahan",
                "tone": "neutral",
                "icon": "yard",
                "title": "Sanitasi & Drainase",
                "text": (
                    "Pangkas dan musnahkan daun bergejala, lalu perbaiki saluran "
                    "drainase agar tidak ada genangan di sekitar perakaran."
                ),
                "details": [
                    {"label": "Tindakan:", "value": "Pangkas daun bergejala"},
                    {"label": "Drainase:", "value": "Tinggikan guludan 30-40 cm"},
                    {"label": "Isolasi Fisik:", "value": "Bakar / kubur di luar kebun"},
                ],
                "footnote": "*Jangan meninggalkan sisa tanaman sakit di area kebun.",
            },
        ],
        "prevention": [
            {
                "icon": "grid_goldenratio",
                "title": "Jarak Tanam Ideal",
                "text": (
                    "Gunakan jarak tanam 50 cm x 60 cm atau 60 cm x 80 cm agar "
                    "sirkulasi udara baik dan kelembapan tajuk menurun."
                ),
            },
            {
                "icon": "water_drop",
                "title": "Drainase Parit & Guludan",
                "text": (
                    "Tinggikan guludan tanam dan buat parit gravitasi untuk mencegah "
                    "air menggenang di sekitar pangkal umbi."
                ),
            },
            {
                "icon": "sunny",
                "title": "Intensitas Naungan",
                "text": (
                    "Pangkas cabang penaung secara teratur agar sinar matahari "
                    "tersaring tetap pada kisaran 40%-50%."
                ),
            },
        ],
    },
    "KARAT BERCAK": {
        "display_name": "Bercak Daun (Karat)",
        "latin": "Cercospora amorphophalli / Cercospora sp.",
        "category": "Klasifikasi Patogen Terdeteksi",
        "short": "Terdeteksi lesi bercak konsentris dengan halo klorotik.",
        "impact_title": "Dampak terhadap Akumulasi Glukomanan:",
        "impact": (
            "Penyakit merusak klorofil daun utama, memicu penuaan dini dan "
            "<strong>degradasi efisiensi fotosintesis sebesar -15%</strong> jika tidak "
            "segera diintervensi. Hal ini berpotensi menghambat sintesis glukomanan "
            "pada umbi porang fase vegetatif II."
        ),
        "confidence_note": (
            "Model mengenali pola lesi konsentris khas Cercosporiose pada daun porang."
        ),
        "metrics": [
            {"label": "Kecepatan Penularan", "value": "Cepat", "note": "Spora Angin & Hujan", "tone": "critical"},
            {"label": "Organ Terdampak", "value": "Daun & Tangkai", "note": "Helaian & Petiola", "tone": "moderate"},
            {"label": "Potensi Defisit Umbi", "value": "12% - 25%", "note": "Bobot Panen Akhir", "tone": "moderate"},
        ],
        "symptoms": [
            {
                "icon": "bubble_chart",
                "title": "Tanda Morfologi Daun",
                "text": (
                    "Lesi nekrotik berbentuk melingkar hingga agak bersudut. Pusat "
                    "bercak berwarna abu-abu kecokelatan kering, dikelilingi "
                    "<strong>halo klorotik kuning keemasan</strong> yang tegas."
                ),
                "note": "Pola Diagnostik: Frogeye Leaf Spot Pattern",
            },
            {
                "icon": "dew_point",
                "title": "Faktor Pemicu Utama",
                "text": (
                    "Kelembapan udara mikro tinggi (<strong>RH &gt; 85%</strong>), "
                    "curah hujan deras berkepanjangan, naungan terlalu rapat, serta "
                    "drainase guludan yang jenuh air."
                ),
                "note": "Mikroklimat saat ini ideal untuk spora patogen.",
                "note_tone": "moderate",
            },
            {
                "icon": "air",
                "title": "Pola Penyebaran Spora",
                "text": (
                    "Konidia jamur <em>Cercospora sp.</em> terbawa angin basah dan "
                    "percikan air hujan. Alat pangkas atau pakaian pekerja yang "
                    "terkontaminasi juga mempercepat transmisi."
                ),
                "note": "Vektor Primer: Angin Laminar & Cipratan Air Hujan",
            },
        ],
        "recommendations": [
            {
                "tag": "Opsi Cepat / Kimia",
                "tone": "primary",
                "icon": "science",
                "title": "Fungisida Kimia Presisi",
                "text": (
                    "Gunakan fungisida sistemik berbahan aktif "
                    "<strong>Difenokonazol 250 g/L</strong> atau fungisida kontak "
                    "<strong>Mankozeb 80%</strong>."
                ),
                "details": [
                    {"label": "Dosis Anjuran:", "value": "1.5 - 2.0 gram/Liter air"},
                    {"label": "Waktu Semprot:", "value": "06:30 - 08:30 WIB"},
                    {"label": "Interval:", "value": "Ulangi tiap 7 hari (maks 3x)"},
                ],
                "footnote": "*Semprot merata sebelum stomata menutup pada pagi hari.",
            },
            {
                "tag": "Organik Berkelanjutan",
                "tone": "secondary",
                "icon": "eco",
                "title": "Biopestisida & Musuh Alami",
                "text": (
                    "Semprotkan ekstrak daun mimba (<em>Azadirachta indica</em>) "
                    "konsentrasi 15% untuk menekan perkecambahan spora."
                ),
                "details": [
                    {"label": "Agens Hayati:", "value": "Trichoderma harzianum"},
                    {"label": "Aplikasi Tanah:", "value": "20 gr/tanaman"},
                    {"label": "Fungsi:", "value": "Kompetitor alami jamur"},
                ],
                "footnote": "*Aman terhadap mikroba tanah dan residu umbi siap ekspor.",
            },
            {
                "tag": "Manajemen Lahan",
                "tone": "neutral",
                "icon": "yard",
                "title": "Sanitasi & Perawatan Tanah",
                "text": (
                    "Lakukan pengapuran ringan dengan <strong>Kapur Dolomit</strong> "
                    "untuk menetralkan pH tanah masam (target pH 6.2 - 6.8)."
                ),
                "details": [
                    {"label": "Dolomit:", "value": "50 - 80 gr per rumpun"},
                    {"label": "Abu Sekam Padi:", "value": "Tabur tipis di bedengan"},
                    {"label": "Isolasi Fisik:", "value": "Pangkas daun lesi > 50%"},
                ],
                "footnote": "*Bakar atau kubur daun rontok di luar area kebun porang.",
            },
        ],
        "prevention": [
            {
                "icon": "grid_goldenratio",
                "title": "Penataan Jarak Tanam",
                "text": (
                    "Terapkan jarak tanam 50 cm x 60 cm atau 60 cm x 80 cm agar "
                    "sirkulasi angin baik dan embun tidak mengendap di tajuk."
                ),
            },
            {
                "icon": "water_drop",
                "title": "Drainase Parit & Guludan",
                "text": (
                    "Tinggikan guludan 30-40 cm dan buat parit pembuangan air untuk "
                    "mencegah genangan di pangkal umbi dan petiola."
                ),
            },
            {
                "icon": "sunny",
                "title": "Intensitas Naungan Terkontrol",
                "text": (
                    "Pangkas cabang pohon penaung agar intensitas cahaya tersaring "
                    "tetap 40%-50%. Cahaya cukup menekan pembentukan spora."
                ),
            },
        ],
    },
}


def get_info(name):
    """Ambil info penyakit berdasarkan nama kelas; fallback ke entri pertama."""
    if name in DISEASE_INFO:
        return DISEASE_INFO[name]
    upper = (name or "").upper()
    for key in DISEASE_INFO:
        if key in upper or upper in key:
            return DISEASE_INFO[key]
    return DISEASE_INFO["KARAT BERCAK"]
