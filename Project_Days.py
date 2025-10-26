import os, sys, time, random, json

# ====== UTILITAS DASAR ======
def slow(text, delay=0.03):
    """Efek teks berjalan lambat"""
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear():
    """Membersihkan layar"""
    os.system("clear" if os.name != "nt" else "cls")

# ====== WARNA (opsional, bisa diubah nanti) ======
class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"

# ===== DATA SAVE =====
SAVE_FOLDER = "saves"
if not os.path.exists(SAVE_FOLDER):
    os.mkdir(SAVE_FOLDER)

def save_game(player):
    """Menyimpan data player ke file JSON"""
    file_path = os.path.join(SAVE_FOLDER, f"{player['name']}.json")
    with open(file_path, "w") as f:
        json.dump(player, f)
    slow(f"Progress {player['name']} berhasil disimpan!", 0.03)
    time.sleep(1)

def load_game():
    """Memuat data player dari file JSON"""
    files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".json")]
    if not files:
        slow("Tidak ada file save ditemukan.", 0.03)
        time.sleep(1)
        return None

    print("\nDaftar Save:")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {f[:-5]}")  # tanpa .json
    choice = input("Pilih nomor save: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(files):
        file_path = os.path.join(SAVE_FOLDER, files[int(choice) - 1])
        with open(file_path, "r") as f:
            player = json.load(f)
        slow(f"Data {player['name']} berhasil dimuat!", 0.03)
        time.sleep(1)
        return player
    else:
        slow("Pilihan tidak valid!", 0.03)
        time.sleep(1)
        return None

# ====== MENU AWAL ======
def show_title():
    clear()
    print("=" * 60)
    print(" " * 18 + "PROJECT DAYS v1.0")
    print("=" * 60)
    print()
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    print()
    choice = input("Pilih: ").strip()

    if choice == "1":
        player = create_new_game()
        main_menu(player)
    elif choice == "2":
        player = load_game()
        if player:
            main_menu(player)
        else:
            slow("Gagal memuat data game!", 0.03)
            time.sleep(1)
            show_title()
    elif choice == "3":
        slow("Keluar dari Project Days...", 0.03)
        sys.exit()
    else:
        slow("Input tidak valid.", 0.03)
        time.sleep(1)
        show_title()

def load_game():
    """Memuat data karakter dari folder saves"""
    files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".json")]
    clear()
    if not files:
        slow("Tidak ada file save ditemukan.", 0.03)
        time.sleep(1)
        show_title()
        return None

    print("Pilih file untuk dimuat:\n")
    for i, f in enumerate(files, start=1):
        name = f.replace(".json", "")
        print(f"{i}. {name}")

    print()
    try:
        num = int(input("Masukkan nomor: ").strip())
        if num < 1 or num > len(files):
            raise ValueError
        file_path = os.path.join(SAVE_FOLDER, files[num - 1])
        with open(file_path, "r") as f:
            data = json.load(f)
        slow(f"Memuat data {data['name']}...\n", 0.03)
        time.sleep(1)
        return data
    except:
        slow("Input tidak valid.", 0.03)
        time.sleep(1)
        show_title()
        return None

def create_new_game():
    clear()
    slow("Memasuki dunia Project Days...\n", 0.03)
    time.sleep(1)
    clear()
    slow("Tahun 2030...", 0.04)
    slow("Dunia telah hancur akibat penyebaran senjata biologis mematikan.", 0.04)
    slow("Hanya segelintir manusia yang berhasil bertahan hidup.", 0.04)
    slow("Sebagian lainnya... berubah menjadi makhluk haus darah — zombie.", 0.04)
    slow("\nKau adalah salah satu yang masih hidup.", 0.04)
    slow("Setiap hari hanyalah perjuangan untuk bertahan hidup.\n", 0.04)
    time.sleep(1)

    name = input("Masukkan nama karaktermu: ").strip().title()
    if not name:
        name = "Survivor"

    slow(f"\nSelamat datang, {name}...", 0.03)
    slow("Kau kini melangkah ke dunia kehancuran yang tak kenal ampun.\n", 0.03)
    time.sleep(1)

    # Inisialisasi data karakter
    player_data = {
        "name": name,
        "level": 1,
        "exp": 0,
        "hp": 100,
        "max_hp": 100,
        "energy": 100,
        "max_energy": 100,
        "atk": 10,
        "def": 5,
        "dex": 3,
        "weapon": "Tangan Kosong",
        "armor": "Pakaian Lusuh",
        "inventory": {
            "Perban": 2,
            "Minuman": 2,
            "Makanan": 1
        },
        "location": "Hutan Pinggiran",
        "exp_to_next": 100
    }

    # Simpan otomatis karakter baru
    save_path = os.path.join(SAVE_FOLDER, f"{name}.json")
    with open(save_path, "w") as f:
        json.dump(player_data, f, indent=4)

    slow("\nKarakter berhasil dibuat!", 0.03)
    time.sleep(1)
    return player_data

def tampil_status(player):
    clear()
    print("═" * 60)
    print()
    print(f"🧍  Nama   : {player['name']}")
    print()
    print(f"🔰 Level  : {player['level']}  | EXP: {player['exp']}/{player['exp_to_next']}")
    print()
    print(f"❤️  HP     : {player['hp']}/{player['max_hp']}  | ⚡ Energy: {player['energy']}/{player['max_energy']}")
    print()
    print(f"🗡️  ATK    : {player['atk']}  | 🛡️ DEF: {player['def']}  | 🎯 DEX: {player['dex']}")
    print()
    print(f"⚙️  Weapon : {player['weapon']}")
    print(f"🧥 Armor  : {player['armor']}")
    print()
    print("═" * 60)
    print()

def main_menu(player):
    while True:
        tampil_status(player)
        print("1. Inventory")
        print("2. Explore")
        print("3. Travel")
        print("4. Toko")
        print("5. Chatting (coming soon)")
        print("6. Exit (Save & Quit)")
        print()
        print("═" * 60)
        choice = input("Pilih menu: ").strip()

        if choice == "1":
            slow("Membuka inventory...\n", 0.03)
            inventory_menu(player)
        elif choice == "2":
            slow("Bersiap untuk menjelajah...\n", 0.03)
            explore_menu(player)
        elif choice == "3":
            slow("Mempersiapkan perjalanan...\n", 0.03)
            travel_menu(player)
        elif choice == "4":
            slow("Menuju toko terdekat...\n", 0.03)
            shop_menu(player)
        elif choice == "5":
            slow("Fitur chatting global masih dalam tahap pengembangan.\n", 0.03)
            input("Tekan Enter untuk kembali...")
        elif choice == "6":
            save_game(player)
            slow("\nSampai jumpa lagi di dunia yang hancur ini...", 0.03)
            time.sleep(1)
            clear()
            exit()
        else:
            slow("Pilihan tidak valid.\n", 0.03)
            time.sleep(1)

def inventory_menu(player):
    while True:
        clear()
        print("═" * 60)
        print(f"📦 INVENTORY — {player['name']}")
        print("═" * 60)
        print()

        if not player["inventory"]:
            print("Inventory kosong.\n")
        else:
            for i, (item, jumlah) in enumerate(player["inventory"].items(), start=1):
                print(f"{i}. {item} ({jumlah})")
        print()
        print("1. Lihat deskripsi item")
        print("2. Gunakan item")
        print("3. Buang item")
        print("4. Crafting")
        print("5. Kembali")
        print()
        choice = input("Pilih: ").strip()

        if choice == "1":
            lihat_deskripsi()
        elif choice == "2":
            gunakan_item(player)
        elif choice == "3":
            buang_item(player)
        elif choice == "4":
            crafting_menu(player)
        elif choice == "5":
            return
        else:
            slow("Pilihan tidak valid.", 0.03)
            time.sleep(1)

def lihat_deskripsi():
    clear()
    slow("Beberapa contoh item:\n", 0.03)
    slow("🩹 Perban  — Mengembalikan 20 HP.", 0.02)
    slow("🥤 Minuman — Mengembalikan 20 Energy.", 0.02)
    slow("🍖 Makanan — Mengembalikan 30 Energy & 10 HP.", 0.02)
    slow("🪵 Kayu, Batu, Daun — Bahan untuk crafting.\n", 0.02)
    input("Tekan Enter untuk kembali...")

def gunakan_item(player):
    if not player["inventory"]:
        slow("Inventory kosong.", 0.03)
        time.sleep(1)
        return

    clear()
    print("Pilih item yang ingin digunakan:\n")
    items = list(player["inventory"].items())
    for i, (item, jumlah) in enumerate(items, start=1):
        print(f"{i}. {item} ({jumlah})")
    print()
    try:
        choice = int(input("Nomor item: ").strip())
        item, jumlah = items[choice - 1]
    except:
        slow("Pilihan tidak valid.", 0.03)
        return

    # Efek item
    if item == "Perban":
        heal = 20
        player["hp"] = min(player["hp"] + heal, player["max_hp"])
        slow(f"HP bertambah {heal}.", 0.03)
    elif item == "Minuman":
        regen = 20
        player["energy"] = min(player["energy"] + regen, player["max_energy"])
        slow(f"Energy bertambah {regen}.", 0.03)
    elif item == "Makanan":
        player["hp"] = min(player["hp"] + 10, player["max_hp"])
        player["energy"] = min(player["energy"] + 30, player["max_energy"])
        slow("Kau makan dengan lahap dan merasa lebih segar.", 0.03)
    else:
        slow("Item ini tidak bisa digunakan langsung.", 0.03)
        return

    # Kurangi jumlah
    player["inventory"][item] -= 1
    if player["inventory"][item] <= 0:
        del player["inventory"][item]
    time.sleep(1)

def buang_item(player):
    if not player["inventory"]:
        slow("Tidak ada item untuk dibuang.", 0.03)
        time.sleep(1)
        return

    clear()
    print("Pilih item yang ingin dibuang:\n")
    items = list(player["inventory"].items())
    for i, (item, jumlah) in enumerate(items, start=1):
        print(f"{i}. {item} ({jumlah})")
    print()
    try:
        choice = int(input("Nomor item: ").strip())
        item, jumlah = items[choice - 1]
        del player["inventory"][item]
        slow(f"{item} dibuang.", 0.03)
    except:
        slow("Pilihan tidak valid.", 0.03)
    time.sleep(1)

def crafting_menu(player):
    clear()
    print("═" * 60)
    print("⚒️  MENU CRAFTING")
    print("═" * 60)
    print()
    print("1. Perban (Butuh: 2x Kain)")
    print("2. Kayu Tajam (Butuh: 2x Kayu + 1x Batu)")
    print("3. Kembali")
    print()
    choice = input("Pilih resep: ").strip()

    if choice == "1":
        if player["inventory"].get("Kain", 0) >= 2:
            player["inventory"]["Kain"] -= 2
            player["inventory"]["Perban"] = player["inventory"].get("Perban", 0) + 1
            slow("Kamu berhasil membuat 1x Perban.", 0.03)
        else:
            slow("Bahan tidak cukup.", 0.03)
    elif choice == "2":
        if player["inventory"].get("Kayu", 0) >= 2 and player["inventory"].get("Batu", 0) >= 1:
            player["inventory"]["Kayu"] -= 2
            player["inventory"]["Batu"] -= 1
            player["inventory"]["Kayu Tajam"] = player["inventory"].get("Kayu Tajam", 0) + 1
            slow("Kamu membuat 1x Kayu Tajam.", 0.03)
        else:
            slow("Bahan tidak cukup.", 0.03)
    elif choice == "3":
        return
    else:
        slow("Pilihan tidak valid.", 0.03)
    time.sleep(1)

def explore_menu(player):
    while True:
        clear()
        print("═" * 60)
        print("🌍  EXPLORE MENU")
        print("═" * 60)
        print("1. Hutan")
        print("2. Desa")
        print("3. Kota")
        print("4. Kembali")
        print("═" * 60)
        choice = input("Pilih lokasi: ").strip()

        if choice == "1":
            lokasi = "Hutan"
            energi = 15
            chance_zombie = 30
            chance_item = 80
            reward_exp = 10
        elif choice == "2":
            lokasi = "Desa"
            energi = 25
            chance_zombie = 70
            chance_item = 80
            reward_exp = 20
        elif choice == "3":
            lokasi = "Kota"
            energi = 50
            chance_zombie = 90
            chance_item = 80
            reward_exp = 40
        elif choice == "4":
            return
        else:
            slow("Pilihan tidak valid.", 0.03)
            continue

        if player["energy"] < energi:
            slow("Energi tidak cukup untuk menjelajah ke sana.", 0.03)
            time.sleep(1)
            continue

        player["energy"] -= energi
        slow(f"\nMenjelajah ke {lokasi}...\n", 0.03)
        time.sleep(1)

        # Random event: item atau musuh
        event_roll = random.randint(1, 100)
        if event_roll <= chance_item:
            dapat_item(player, lokasi)
        elif event_roll <= chance_item + chance_zombie:
            battle_zombie(player, lokasi, reward_exp)
        else:
            slow("Tidak terjadi apa-apa... hanya keheningan yang mencekam.", 0.03)
            time.sleep(1)

def dapat_item(player, lokasi):
    slow("Kamu menemukan sesuatu di sekitar...\n", 0.03)
    loot_table = {
        "Hutan": ["Kayu", "Batu", "Daun", "Makanan", "Minuman"],
        "Desa": ["Perban", "Kain", "Makanan", "Minuman", "Pisau"],
        "Kota": ["Perban", "Ammo 9mm", "Ammo 12mm", "Ammo 7.2mm", "Pistol", "Shotgun", "Sniper", "Senapan Serbu", "Obat-obatan"]
    }

    item = random.choice(loot_table[lokasi])
    jumlah = random.randint(1, 3)
    player["inventory"][item] = player["inventory"].get(item, 0) + jumlah
    slow(f"Kamu mendapatkan {jumlah}x {item}!", 0.03)
    time.sleep(1)

def battle_zombie(player, lokasi, reward_exp):
    slow(f"Tiba-tiba... zombie muncul di {lokasi}!\n", 0.03)
    zombie = {
        "name": random.choice(["Zombie Lapar", "Zombie Busuk", "Zombie Cepat"]),
        "hp": random.randint(30, 70),
        "atk": random.randint(5, 15),
        "exp": reward_exp + random.randint(5, 15)
    }
    time.sleep(1)

    while zombie["hp"] > 0 and player["hp"] > 0:
        clear()
        print("═" * 60)
        print(f"⚔️  {zombie['name']}")
        print(f"❤️  HP: {zombie['hp']}")
        print("═" * 60)
        print(f"🧍  {player['name']} — HP: {player['hp']} / {player['max_hp']}")
        print("═" * 60)
        print("1. Serang")
        print("2. Gunakan Item")
        print("3. Kabur")
        print("═" * 60)
        action = input("Pilih aksi: ").strip()

        if action == "1":
            dmg = random.randint(player["atk"] - 3, player["atk"] + 3)
            zombie["hp"] -= dmg
            slow(f"Kamu menyerang dan memberi {dmg} damage!", 0.03)
        elif action == "2":
            gunakan_item(player)
            continue
        elif action == "3":
            if random.randint(1, 100) <= 50:
                slow("Kamu berhasil kabur!", 0.03)
                return
            else:
                slow("Zombie menghadang! Kamu gagal kabur!", 0.03)
        else:
            slow("Pilihan tidak valid.", 0.03)
            continue

        if zombie["hp"] <= 0:
            slow(f"\nZombie berhasil dikalahkan!", 0.03)
            player["exp"] += zombie["exp"]
            drop_item(player)
            check_level_up(player)
            time.sleep(1)
            return

        # Serangan balik zombie
        dmg_z = random.randint(zombie["atk"] - 2, zombie["atk"] + 2)
        dmg_z = max(1, dmg_z - player["def"] // 3)
        player["hp"] -= dmg_z
        slow(f"Zombie menyerang! Kamu menerima {dmg_z} damage!\n", 0.03)

        if player["hp"] <= 0:
            slow("Kamu tumbang... Dunia ini terlalu keras bagimu.", 0.04)
            time.sleep(2)
            sys.exit()

def drop_item(player):
    if random.randint(1, 100) <= 50:
        item = random.choice(["Ammo 9mm", "Perban", "Minuman"])
        jumlah = random.randint(1, 2)
        player["inventory"][item] = player["inventory"].get(item, 0) + jumlah
        slow(f"Zombie menjatuhkan {jumlah}x {item}!", 0.03)
        time.sleep(1)

def check_level_up(player):
    if player["exp"] >= player["exp_to_next"]:
        player["level"] += 1
        player["exp"] = 0
        player["exp_to_next"] += 50
        player["atk"] += 2
        player["def"] += 2
        player["max_hp"] += 10
        player["max_energy"] += 5
        player["hp"] = player["max_hp"]
        player["energy"] = player["max_energy"]
        slow(f"\nNaik level! Sekarang kamu level {player['level']}!", 0.03)
        time.sleep(1)

def travel_menu(player):
    clear()
    print("═" * 60)
    print("🚗  TRAVEL MENU")
    print("═" * 60)
    print(f"📍 Lokasi saat ini : {player['location']}")
    print(f"⚡ Energi         : {player['energy']}/{player['max_energy']}")
    print("═" * 60)

    konfirmasi = input("Ingin melakukan perjalanan ke kota lain? (y/n): ").strip().lower()
    if konfirmasi != "y":
        slow("Perjalanan dibatalkan.", 0.03)
        time.sleep(1)
        return

    kota_indonesia = [
        "Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Semarang", "Medan",
        "Palembang", "Makassar", "Denpasar", "Balikpapan", "Malang", "Pontianak",
        "Manado", "Padang", "Samarinda", "Banjarmasin", "Cirebon", "Tasikmalaya",
        "Solo", "Bogor", "Batam", "Pekanbaru", "Kupang", "Jayapura", "Mataram"
    ]

    # Tentukan kota tujuan secara acak tapi tidak sama dengan kota saat ini
    tujuan = random.choice([k for k in kota_indonesia if k != player["location"]])
    biaya = random.randint(30, 60)

    if player["energy"] < biaya:
        slow("Energi kamu tidak cukup untuk melakukan perjalanan jauh.", 0.03)
        time.sleep(1)
        return

    slow(f"\nKamu memulai perjalanan jauh meninggalkan {player['location']}...", 0.03)
    time.sleep(2)
    player["energy"] -= biaya
    player["location"] = tujuan
    slow(f"\nSetelah menempuh perjalanan panjang, kamu tiba di {tujuan}.", 0.03)
    time.sleep(1)

def shop_menu(player):
    clear()
    print("═" * 60)
    print(f"🏪  TOKO - {player['location']}")
    print("═" * 60)
    print("1. Kios (Barter)")
    print("2. Marketplace (coming soon)")
    print("3. Kembali")
    print("═" * 60)

    pilihan = input("Pilih menu: ").strip()
    if pilihan == "1":
        barter_shop(player)
    elif pilihan == "2":
        slow("Marketplace masih dalam tahap pengembangan...", 0.03)
        time.sleep(1)
    elif pilihan == "3":
        return
    else:
        slow("Pilihan tidak valid.", 0.03)
        time.sleep(1)

def barter_shop(player):
    clear()
    slow(f"\nKamu memasuki kios barter di {player['location']}...\n", 0.03)
    time.sleep(1)

    # Barang tergantung kota (dalam kelompok tipe wilayah)
    kota_pesisir = ["Surabaya", "Makassar", "Denpasar", "Balikpapan", "Manado", "Batam", "Padang"]
    kota_gunung = ["Bandung", "Malang", "Bogor", "Tasikmalaya", "Solo"]
    kota_besar  = ["Jakarta", "Yogyakarta", "Semarang", "Medan", "Palembang", "Samarinda"]

    if player["location"] in kota_pesisir:
        stok_pedagang = ["Ikan Kering", "Air Laut", "Obat Luka", "Kayu", "Pisau"]
    elif player["location"] in kota_gunung:
        stok_pedagang = ["Kayu", "Batu", "Daun Herbal", "Obat", "Tombak"]
    elif player["location"] in kota_besar:
        stok_pedagang = ["Ammo 9mm", "Makanan Kaleng", "Perban", "Minuman", "Kain"]
    else:
        stok_pedagang = ["Kain", "Obat", "Batu", "Kayu", "Minuman"]

    while True:
        clear()
        print("═" * 60)
        print(f"🤝  KIOS BARTER — {player['location']}")
        print("═" * 60)
        for i, item in enumerate(stok_pedagang, 1):
            print(f"{i}. {item}")
        print("6. Kembali")
        print("═" * 60)

        print("Inventory kamu:")
        if player["inventory"]:
            for k, v in player["inventory"].items():
                print(f"- {k} ({v})")
        else:
            print("❌ Kamu tidak punya item apapun.")
        print("═" * 60)

        pilih = input("Pilih item dari pedagang (1-5): ").strip()
        if pilih == "6":
            slow("Kamu meninggalkan kios.", 0.03)
            time.sleep(1)
            return
        if not pilih.isdigit() or int(pilih) not in range(1, 6):
            slow("Pilihan tidak valid.", 0.03)
            continue

        item_toko = stok_pedagang[int(pilih) - 1]

        if not player["inventory"]:
            slow("Kamu tidak punya barang untuk ditukar!", 0.03)
            time.sleep(1)
            continue

        print("\nBarang kamu untuk barter:")
        for i, (item, jumlah) in enumerate(player["inventory"].items(), 1):
            print(f"{i}. {item} ({jumlah})")
        pilih_barter = input("Pilih barangmu untuk ditukar: ").strip()

        if not pilih_barter.isdigit() or int(pilih_barter) < 1 or int(pilih_barter) > len(player["inventory"]):
            slow("Pilihan tidak valid.", 0.03)
            continue

        item_player = list(player["inventory"].keys())[int(pilih_barter) - 1]

        # 70% kemungkinan barter berhasil
        if random.randint(1, 100) <= 70:
            del player["inventory"][item_player]
            player["inventory"][item_toko] = player["inventory"].get(item_toko, 0) + 1
            slow(f"Barter berhasil! {item_player} ditukar dengan {item_toko}.", 0.03)
        else:
            slow(f"Pedagang menolak menukar {item_player}.", 0.03)

        time.sleep(1)
        lanjut = input("\nIngin barter lagi? (y/n): ").strip().lower()
        if lanjut != "y":
            break

# Auto-repair save
def auto_repair_saves():
    """
    Memeriksa folder save dan memperbaiki file rusak, kosong, atau duplikat.
    - Menghapus file yang bukan .json
    - Menghapus file kosong (ukuran 0 byte)
    - Memperbaiki format JSON yang error
    """
    repaired = 0
    removed = 0

    # Pastikan folder save ada
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        return

    for filename in os.listdir(SAVE_FOLDER):
        filepath = os.path.join(SAVE_FOLDER, filename)

        # Hapus file non-json
        if not filename.endswith(".json"):
            os.remove(filepath)
            removed += 1
            continue

        # Hapus file kosong
        if os.path.getsize(filepath) == 0:
            os.remove(filepath)
            removed += 1
            continue

        # Periksa validitas JSON
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            # Pastikan minimal punya key penting
            required_keys = ["name", "level", "hp", "exp", "energy"]
            if not all(key in data for key in required_keys):
                os.remove(filepath)
                removed += 1
        except Exception:
            # Kalau file JSON rusak, hapus saja
            os.remove(filepath)
            removed += 1

    if removed > 0 or repaired > 0:
        slow(f"\n🧩 Sistem perbaikan save: {removed} file rusak dihapus.\n", 0.02)
        time.sleep(1)

# Skrip Wajib paling akhir
if __name__ == "__main__":
    auto_repair_saves()
    clear()
    slow("Memulai Project Days...\n", 0.04)
    time.sleep(1)
    show_title()
