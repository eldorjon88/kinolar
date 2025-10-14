Filmlane/
├── app/                          # FastAPI backend
│   ├── db/                      # Database konfiguratsiyasi
│   │   └── database.py          # SQLAlchemy sozlamalari
│   ├── models/                  # Database modellari
│   │   ├── movie.py             # Film va janr modellari
│   │   ├── anime.py             # Anime va seria modellari
│   │   └── serial.py            # Serial va epizod modellari
│   ├── routers/                 # API yo'naltiruvchilari
│   │   ├── movies.py            # Film API endpointlari
│   │   ├── anime.py             # Anime API endpointlari
│   │   ├── serial.py            # Serial API endpointlari
│   │   ├── anime_seria.py       # Anime seriyalari API
│   │   ├── seral_seria.py       # Serial epizodlari API
│   │   ├── ganres.py            # Janrlar API
│   │   └── mix.py               # Aralash kontent API
│   ├── schemas/                 # Pydantic sxemalari
│   │   ├── movies.py            # Film sxemalari
│   │   ├── animes.py            # Anime sxemalari
│   │   ├── serials.py           # Serial sxemalari
│   │   └── ganres.py            # Janr sxemalari
│   ├── services/                # Biznes logikasi
│   │   └── mix.py               # Aralash kontent xizmatlari
│   └── main.py                  # FastAPI ilovasi
├── frontend/                    # Frontend fayllari
│   ├── assets/                  # Statik resurslar
│   │   ├── css/
│   │   │   └── style.css        # Asosiy CSS fayli
│   │   ├── js/
│   │   │   └── script.js        # JavaScript fayllari
│   │   └── images/              # Rasmlar
│   ├── index.html               # Asosiy sahifa
│   ├── movies.html              # Filmlar sahifasi
│   ├── movie-details.html       # Film tafsilotlari
│   ├── anime-details.html       # Anime tafsilotlari
│   ├── serial-details.html      # Serial tafsilotlari
│   ├── index1.html              # Film admin paneli
│   ├── index2.html              # Anime yaratish formasi
│   ├── index3.html              # Anime admin paneli
│   └── index4.html              # Serial admin paneli
├── media/                       # Yuklangan fayllari
│   ├── images/                  # Rasm fayllari
│   ├── movies/                  # Film fayllari
│   ├── anime_serias/            # Anime seriya fayllari
│   └── serial_serias/           # Serial epizod fayllari
├── requirements.txt             # Python bog'liqliklar
├── .env                         # Muhit o'zgaruvchilari
├── .gitignore                   # Git ignore fayli
├── restar.py                    # Database qayta tiklash
└── README.md                    # Bu fayl