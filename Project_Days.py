import os
import sys
import time
import random
import json

# =========================
# Project Days v1.7 - Revised
# Modern minimalis terminal style
# =========================

# ====== UTILITIES ======

def slow(text, delay=0.02):
    for c in str(text):
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def clear():
    os.system("clear" if os.name != "nt" else "cls")


class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


# ====== GLOBALS & DATA ======
SAVE_FOLDER = "saves"
if not os.path.exists(SAVE_FOLDER):
    os.mkdir(SAVE_FOLDER)

# Weapon & armor definitions (consistent names)
weapon_list = {
    "Tangan Kosong": {"type": "melee", "atk": 5},
    "Pisau": {"type": "melee", "atk": 8},
    "Palu": {"type": "melee", "atk": 12},
    "Tombak": {"type": "melee", "atk": 16},
    "Kampak": {"type": "melee", "atk": 20},
    "Pedang": {"type": "melee", "atk": 25},

    "Pistol": {"type": "gun", "ammo": "Ammo 9mm", "atk": 35, "scale": 0.05},
    "Shotgun": {"type": "gun", "ammo": "Ammo 12mm", "atk": 55, "scale": 0.05},
    "Sniper": {"type": "gun", "ammo": "Ammo 7.2mm", "atk": 95, "scale": 0.05},
    "Senapan Serbu": {"type": "gun", "ammo": "Ammo 7.2mm", "atk": 60, "scale": 0.05},
}

armor_list = {
    "Pakaian Lusuh": {"def": 5},
    "Kaos": {"def": 8},
    "Kaos Panjang": {"def": 10},
    "Sweater": {"def": 14},
    "Jaket": {"def": 20},
    "Rompi Lv1": {"def": 30},
    "Rompi Lv2": {"def": 40},
    "Rompi Lv3": {"def": 50},
}

# Zombie types (global)
zombie_types = {
    "Zombie": {"hp_mod": 1.0, "atk_mod": 1.0, "def_mod": 1.0, "dodge": 0},
    "Zombie Atlit": {"hp_mod": 0.7, "atk_mod": 0.8, "def_mod": 0.8, "dodge": 35},
    "Zombie Berotot": {"hp_mod": 1.35, "atk_mod": 1.3, "def_mod": 1.0, "dodge": 0},
    "Zombie Armored": {"hp_mod": 1.3, "atk_mod": 1.1, "def_mod": 1.4, "dodge": 0},
    "Zombie Mutant": {"hp_mod": 1.4, "atk_mod": 1.3, "def_mod": 1.25, "dodge": 15},
}

# Item effects for consumables
item_effects = {
    "Perban": {"type": "heal", "heal": 25},
    "Herbal": {"type": "heal", "heal": 15},
    "Painkiller": {"type": "heal", "heal": 35},
    "Medkit": {"type": "heal", "heal": 50},
    "Makanan": {"type": "heal_energy", "heal": 10, "energy": 30},
    "Minuman": {"type": "energy", "energy": 20},
}

# ====== SAVE / LOAD ======

def save_game(player):
    try:
        if not os.path.exists(SAVE_FOLDER):
            os.mkdir(SAVE_FOLDER)
        filename = os.path.join(SAVE_FOLDER, f"{player['name']}.json")
        with open(filename, "w") as f:
            json.dump(player, f, indent=4)
        slow(f"\n💾 Game berhasil disimpan: {filename}\n", 0.02)
        time.sleep(0.6)
    except Exception as e:
        slow(f"Gagal menyimpan game: {e}", 0.02)


def load_game_interactive():
    files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith('.json')]
    clear()
    if not files:
        slow("Tidak ada save yang ditemukan.", 0.02)
        time.sleep(1)
        return None

    print("Pilih file untuk dimuat:\n")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {f[:-5]}")
    print()
    try:
        num = int(input("Masukkan nomor: ").strip())
        if num < 1 or num > len(files):
            raise ValueError
        path = os.path.join(SAVE_FOLDER, files[num-1])
        with open(path, 'r') as f:
            data = json.load(f)
        slow(f"Memuat data {data.get('name','Unknown')}...", 0.02)
        time.sleep(0.8)
        return data
    except Exception:
        slow("Input tidak valid.", 0.02)
        time.sleep(1)
        return None


# ====== PLAYER CREATION & STATUS ======

def create_new_game():
    clear()
    slow("Memasuki dunia Project Days...\n", 0.03)
    time.sleep(0.6)
    slow("Tahun 2089... Dunia runtuh setelah wabah biologi.", 0.03)
    slow("Kau harus bertahan, mencari makanan, dan menghindari zombie.\n", 0.03)
    time.sleep(0.6)

    name = input("Masukkan nama karaktermu: ").strip().title()
    if not name:
        name = "Survivor"

    player = {
        "name": name,
        "level": 1,
        "exp": 0,
        "exp_to_next": 100,
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
            "Makanan": 1,
            "Pisau": 1,
        },
        "location": "Hutan Pinggiran"
    }

    save_game(player)
    slow(f"\nSelamat, {player['name']}! Karaktermu telah dibuat.", 0.02)
    time.sleep(0.8)
    return player


def check_level_up(player):
    while player.get('exp', 0) >= player.get('exp_to_next', 100):
        player['level'] += 1
        player['exp'] = player['exp'] - player['exp_to_next']
        player['exp_to_next'] = player.get('exp_to_next',100) + 50
        player['atk'] += 2
        player['def'] += 2
        player['def'] += 2
        player['max_hp'] += 10
        player['max_energy'] += 5
        player['hp'] = player['max_hp']
        player['energy'] = player['max_energy']
        slow(f"\n🎉 Naik level! Sekarang kamu level {player['level']}", 0.02)
        time.sleep(0.8)

# ====== UI: Title & Menus ======
def show_title():
    clear()
    print("=" * 60)
    print(" " * 18 + "PROJECT DAYS v1.7")
    print("=" * 60)
    print()
    print("1. New Game".ljust(30) + "2. Load Game")
    print("3. Exit")
    print()
    choice = input(" " * 70 + "Pilih: ").strip()

    if choice == "1":
        player = create_new_game()
        main_menu(player)
    elif choice == "2":
        player = load_game_interactive()
        if player:
            main_menu(player)
        else:
            show_title()
    elif choice == "3":
        slow("Keluar...", 0.02)
        sys.exit()
    else:
        slow("Input tidak valid.", 0.02)
        time.sleep(0.6)
        show_title()

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
            slow("Membuka inventory...", 0.02)
            inventory_menu(player)
        elif choice == "2":
            slow("Bersiap untuk menjelajah...", 0.02)
            explore_menu(player)
        elif choice == "3":
            slow("Mempersiapkan perjalanan...", 0.02)
            travel_menu(player)
        elif choice == "4":
            slow("Menuju toko terdekat...", 0.02)
            shop_menu(player)
        elif choice == "5":
            slow("Fitur chatting global masih dalam pengembangan...", 0.02)
            input("Tekan Enter untuk kembali...")
        elif choice == "6":
            save_game(player)
            slow("Sampai jumpa, survivor.", 0.02)
            time.sleep(0.6)
            clear()
            sys.exit()
        else:
            slow("Pilihan tidak valid.", 0.02)
            time.sleep(0.6)

# ====== INVENTORY SYSTEM ======
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
            slow("Pilihan tidak valid.", 0.02)
            time.sleep(0.6)

def lihat_deskripsi():
    clear()
    slow("Item yang ada didalam permainan:\n", 0.02)
    slow("🩹 Perban  — Mengembalikan 25 HP.", 0.02)
    slow("🥤 Minuman — Mengembalikan 20 Energy.", 0.02)
    slow("🍖 Makanan — Mengembalikan 30 Energy & 10 HP.", 0.02)
    slow("🌿 Herbal — Bahan ramuan, mengembalikan 15 HP.", 0.02)
    slow("🩹 Medkit  — Bahan ramuan, mengembalikan 50 HP.", 0.02)
    slow("🪵 Kayu, Batu, Daun — Bahan untuk crafting.", 0.02)
    input("Tekan Enter untuk kembali...")

def gunakan_item(player):
    global weapon_list, armor_list

    # Filter item valid (jumlah > 0)
    valid_items = {k: v for k, v in player["inventory"].items() if v > 0}

    if not valid_items:
        slow("Inventory kosong.", 0.02)
        time.sleep(1)
        return

    clear()
    print("Pilih item yang ingin digunakan:\n")

    items = list(valid_items.items())
    for i, (nama, jumlah) in enumerate(items, start=1):
        print(f"{i}. {nama} ({jumlah})")
    print()

    try:
        choice = int(input("Nomor item: ").strip())
        if choice < 1 or choice > len(items):
            raise ValueError
        item, jumlah = items[choice - 1]
    except ValueError:
        slow("Pilihan tidak valid.", 0.02)
        return

    # Efek item consumable
    if item in item_effects:
        effect = item_effects[item]
        if effect["type"] == "heal":
            player["hp"] = min(player["hp"] + effect["heal"], player["max_hp"])
            slow(f"Kamu menggunakan {item}. HP +{effect['heal']}", 0.02)
        elif effect["type"] == "energy":
            player["energy"] = min(player["energy"] + effect["energy"], player["max_energy"])
            slow(f"Kamu menggunakan {item}. Energy +{effect['energy']}", 0.02)
        elif effect["type"] == "heal_energy":
            player["hp"] = min(player["hp"] + effect["heal"], player["max_hp"])
            player["energy"] = min(player["energy"] + effect["energy"], player["max_energy"])
            slow(f"Kamu menggunakan {item}. HP +{effect['heal']} dan Energy +{effect['energy']}", 0.02)

    # Equip weapon/armor
    elif item in weapon_list:
        # jika gun, cek ammo
        wdata = weapon_list[item]
        if wdata.get("type") == "gun":
            ammo_t = wdata.get("ammo")
            if player["inventory"].get(ammo_t, 0) <= 0:
                slow(f"Kamu tidak punya peluru {ammo_t}! Tidak bisa equip {item}.", 0.02)
                return
        player["weapon"] = item
        slow(f"Kamu kini menggunakan senjata: {item}!", 0.02)

    elif item in armor_list:
        player["armor"] = item
        slow(f"Kamu kini memakai armor: {item}!", 0.02)

    else:
        slow("Item ini tidak bisa digunakan langsung.", 0.02)
        return

    # Kurangi jumlah item setelah digunakan (jika consumable atau bila equip consumes one)
    if item in player["inventory"]:
        player["inventory"][item] -= 1
        if player["inventory"][item] <= 0:
            del player["inventory"][item]

    time.sleep(0.6)

def buang_item(player):
    valid_items = {k: v for k, v in player["inventory"].items() if v > 0}
    if not valid_items:
        slow("Tidak ada item untuk dibuang.", 0.02)
        time.sleep(1)
        return

    clear()
    print("Pilih item yang ingin dibuang:\n")
    items = list(valid_items.items())
    for i, (item, jumlah) in enumerate(items, start=1):
        print(f"{i}. {item} ({jumlah})")
    print()
    try:
        choice = int(input("Nomor item: ").strip())
        item, jumlah = items[choice - 1]
        del player["inventory"][item]
        slow(f"{item} dibuang.", 0.02)
    except Exception:
        slow("Pilihan tidak valid.", 0.02)
    time.sleep(0.6)

def crafting_menu(player):
    clear()
    print("═" * 60)
    print("⚒️  MENU CRAFTING")
    print("═" * 60)
    print()
    print("1. Perban (Butuh: 2x Kain)")
    print("2. Tombak (Butuh: 1x Kayu + 1x Batu)")
    print("3. Kembali")
    print()
    choice = input("Pilih resep: ").strip()

    if choice == "1":
        if player["inventory"].get("Kain", 0) >= 2:
            player["inventory"]["Kain"] -= 2
            player["inventory"]["Perban"] = player["inventory"].get("Perban", 0) + 1
            slow("Kamu berhasil membuat 1x Perban.", 0.02)
        else:
            slow("Bahan tidak cukup.", 0.02)
    elif choice == "2":
        if player["inventory"].get("Kayu", 0) >= 1 and player["inventory"].get("Batu", 0) >= 1:
            player["inventory"]["Kayu"] -= 2
            player["inventory"]["Batu"] -= 1
            player["inventory"]["Tombak"] = player["inventory"].get("Tombak", 0) + 1
            slow("Kamu membuat 1x Tombak.", 0.02)
        else:
            slow("Bahan tidak cukup.", 0.02)
    elif choice == "3":
        return
    else:
        slow("Pilihan tidak valid.", 0.02)
    time.sleep(0.6)

# ====== TRAVEL & SHOP ======
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
        slow("Perjalanan dibatalkan.", 0.02)
        time.sleep(0.6)
        return

    kota_indonesia = [
        "Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Semarang", "Medan",
        "Palembang", "Makassar", "Denpasar", "Balikpapan", "Malang", "Pontianak",
        "Manado", "Padang", "Samarinda", "Banjarmasin", "Cirebon", "Tasikmalaya",
        "Solo", "Bogor", "Batam", "Pekanbaru", "Kupang", "Jayapura", "Mataram"
    ]

    tujuan = random.choice([k for k in kota_indonesia if k != player["location"]])
    biaya = random.randint(10, 30)
    if player["energy"] < biaya:
        slow("Energi kamu tidak cukup untuk melakukan perjalanan jauh.", 0.02)
        time.sleep(0.6)
        return

    slow(f"\nKamu memulai perjalanan meninggalkan {player['location']}...", 0.02)
    time.sleep(1.2)
    player["energy"] -= biaya
    player["location"] = tujuan
    slow(f"\nSetelah perjalanan panjang, kamu tiba di {tujuan}.", 0.02)
    time.sleep(0.6)

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
        slow("Marketplace masih dalam tahap pengembangan...", 0.02)
        time.sleep(0.6)
    elif pilihan == "3":
        return
    else:
        slow("Pilihan tidak valid.", 0.02)
        time.sleep(0.6)

def barter_shop(player):
    clear()
    slow(f"\nKamu memasuki kios barter di {player['location']}...\n", 0.02)
    time.sleep(0.6)

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
            slow("Kamu meninggalkan kios.", 0.02)
            time.sleep(0.6)
            return
        if not pilih.isdigit() or int(pilih) not in range(1, 6):
            slow("Pilihan tidak valid.", 0.02)
            continue

        item_toko = stok_pedagang[int(pilih) - 1]

        if not player["inventory"]:
            slow("Kamu tidak punya barang untuk ditukar!", 0.02)
            time.sleep(0.6)
            continue

        print("\nBarang kamu untuk barter:")
        for i, (item, jumlah) in enumerate(player["inventory"].items(), 1):
            print(f"{i}. {item} ({jumlah})")
        pilih_barter = input("Pilih barangmu untuk ditukar: ").strip()

        if not pilih_barter.isdigit() or int(pilih_barter) < 1 or int(pilih_barter) > len(player["inventory"]):
            slow("Pilihan tidak valid.", 0.02)
            continue

        item_player = list(player["inventory"].keys())[int(pilih_barter) - 1]

        if random.randint(1, 100) <= 70:
            del player["inventory"][item_player]
            player["inventory"][item_toko] = player["inventory"].get(item_toko, 0) + 1
            slow(f"Barter berhasil! {item_player} ditukar dengan {item_toko}.", 0.02)
        else:
            slow(f"Pedagang menolak menukar {item_player}.", 0.02)

        time.sleep(0.6)

# ====== EXPLORE & LOOT ======
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
            energi = 5
            chance_zombie = 25
            chance_item = 90
            reward_exp = 10
        elif choice == "2":
            lokasi = "Desa"
            energi = 10
            chance_zombie = 50
            chance_item = 80
            reward_exp = 20
        elif choice == "3":
            lokasi = "Kota"
            energi = 20
            chance_zombie = 80
            chance_item = 80
            reward_exp = 40
        elif choice == "4":
            return
        else:
            slow("Pilihan tidak valid.", 0.02)
            continue

        if player["energy"] < energi:
            slow("Energi tidak cukup untuk menjelajah ke sana.", 0.02)
            time.sleep(0.6)
            continue

        player["energy"] -= energi
        slow(f"\nMenjelajah ke {lokasi}...\n", 0.02)
        time.sleep(0.6)

        event_roll = random.randint(1, 100)
        if event_roll <= chance_item:
            dapat_item(player, lokasi)
        elif event_roll <= chance_item + chance_zombie:
            battle_zombie(player, lokasi, reward_exp)
        else:
            slow("Tidak terjadi apa-apa...", 0.02)
            time.sleep(0.6)

def dapat_item(player, lokasi):
    slow("Kamu menemukan sesuatu di sekitar...\n", 0.02)

    loot_table = {
        "Hutan": ["Kayu", "Batu", "Daun", "Makanan", "Minuman"],
        "Desa": ["Perban", "Kain", "Makanan", "Minuman", "Pisau"],
        "Kota": ["Perban", "Painkiller", "Makanan", "Minuman"]
    }

    if lokasi == "Kota":
        roll = random.randint(1, 100)
        if roll <= 35:
            item = random.choice(["Pistol", "Shotgun", "Sniper", "Senapan Serbu"])
        elif 21 <= roll <= 50:
            peluru_roll = random.randint(1, 100)
            if peluru_roll <= 50:
                item = "Ammo 9mm"
            elif peluru_roll <= 90:
                item = "Ammo 12mm"
            else:
                item = "Ammo 7.2mm"
        else:
            item = random.choice(loot_table[lokasi])
    else:
        item = random.choice(loot_table[lokasi])

    jumlah = random.randint(2, 5)
    player["inventory"][item] = player["inventory"].get(item, 0) + jumlah
    slow(f"Kamu mendapatkan {jumlah}x {item}!", 0.02)
    time.sleep(0.6)

# ====== BATTLE ZOMBIE ======
def battle_zombie(player, lokasi, reward_exp):
    global weapon_list, armor_list, zombie_types
    slow(f"Tiba-tiba... zombie muncul di {lokasi}!\n", 0.02)

    # Pilih tipe zombie
    zombie_type_name = random.choice(list(zombie_types.keys()))
    ztype = zombie_types[zombie_type_name]

    # Dasar status zombie
    base_hp = random.randint(30, 70)
    base_atk = random.randint(5, 15)
    base_def = random.randint(0, 10)

    zombie = {
        "name": zombie_type_name,
        "hp": int(base_hp * ztype["hp_mod"]),
        "atk": int(base_atk * ztype["atk_mod"]),
        "def": int(base_def * ztype["def_mod"]),
        "dodge": ztype["dodge"],
        "exp": reward_exp + random.randint(5, 15)
    }

    slow(f"Kamu bertemu dengan {zombie['name']}!\n", 0.03)
    slow(f"• HP: {zombie['hp']} | ATK: {zombie['atk']} | DEF: {zombie['def']} | DODGE: {zombie['dodge']}%\n", 0.02)
    time.sleep(0.8)

    # === LOOP PERTEMPURAN ===
    while player["HP"] > 0 and zombie["hp"] > 0:
        print("\n════════════════════════════════════════════════════════════")
        print(f"⚔️  {zombie['name']} — ❤️  {zombie['hp']}")
        print("════════════════════════════════════════════════════════════")
        print(f"🧍  {player['name']} — ❤️  {player['HP']} / 100")
        print("════════════════════════════════════════════════════════════")
        print("1. Serang")
        print("2. Gunakan Item")
        print("3. Kabur")
        print("════════════════════════════════════════════════════════════")

        action = input("Pilih aksi: ").strip()

        if action == "1":
            # Ambil data senjata
            weapon_name = player.get("Weapon", "Tangan Kosong")
            weapon_data = weapon_list.get(weapon_name, {"type": "melee", "atk": 5})

            base_atk = weapon_data["atk"]

            # Hitung bonus dari stat ATK
            atk_bonus = base_atk * (player["ATK"] * 0.02)
            total_damage = base_atk + atk_bonus

            # Jika senjata type gun
            if weapon_data.get("type") == "gun":
                ammo_type = weapon_data.get("ammo")
                if player["inventory"].get(ammo_type, 0) <= 0:
                    slow(f"Tidak ada peluru {ammo_type}! Serangan gagal!\n", 0.02)
                    total_damage = 0
                else:
                    player["inventory"][ammo_type] -= 1
                    slow(f"🔫 {weapon_name} digunakan! Peluru {ammo_type} tersisa {player['inventory'].get(ammo_type,0)}\n", 0.02)

            # Cek zombie dodge
            if random.randint(1, 100) <= zombie["dodge"]:
                slow(f"{zombie['name']} berhasil menghindar!\n", 0.03)
            else:
                dmg_after_def = max(1, int(total_damage - zombie["def"]))
                zombie["hp"] -= dmg_after_def
                slow(f"Kamu menyerang dan memberi {dmg_after_def} damage!\n", 0.02)

        elif action == "2":
            gunakan_item(player)
            continue

        elif action == "3":
            if random.random() < 0.5:
                slow("Kamu berhasil kabur!\n", 0.02)
                return
            else:
                slow("Gagal kabur!\n", 0.02)
        else:
            slow("Pilihan tidak valid.\n", 0.02)
            continue

        # === Serangan zombie balik ===
        if zombie["hp"] > 0:
            # Peluang dodge dari DEX
            if random.randint(1, 100) <= player["DEX"]:
                slow("Kamu berhasil menghindar dari serangan zombie!\n", 0.02)
            else:
                base_dmg_zombie = zombie["atk"]
                def_reduction = base_dmg_zombie * (player["DEF"] * 0.015)
                total_zombie_dmg = max(1, int(base_dmg_zombie - def_reduction))
                player["HP"] -= total_zombie_dmg
                slow(f"{zombie['name']} menyerangmu dan memberi {total_zombie_dmg} damage!\n", 0.03)

        # === Hasil Akhir ===
        if zombie["hp"] <= 0:
            slow(f"\n{zombie['name']} dikalahkan!\n", 0.03)
            gained_exp = zombie["exp"]
            player["EXP"] += gained_exp
            slow(f"Kamu mendapat {gained_exp} EXP!\n", 0.02)
            drop_item(player)

            # ===== LEVEL UP OTOMATIS =====
            if player["EXP"] >= 100:
                player["EXP"] -= 100
                player["Level"] += 1
                player["ATK"] += 2
                player["DEF"] += 1
                player["DEX"] += 1
                player["HP"] = 100
                player["ENERGY"] = 100
                slow(f"\nNaik Level! Sekarang kamu Level {player['Level']}!\n", 0.03)
                slow("Stat meningkat: +2 ATK, +1 DEF, +1 DEX\n", 0.02)
                time.sleep(1)

            time.sleep(0.6)
            return

        if player["HP"] <= 0:
            slow("\nKamu tumbang... Game Over!\n", 0.03)
            time.sleep(2)
            sys.exit()

# ====== DROP ITEM ======
def drop_item(player):
    # item drop sederhana, bisa dikustom per zombie jenis
    if random.randint(1, 100) <= 50:
        item = random.choice(["Ammo 9mm", "Perban", "Minuman"])
        jumlah = random.randint(2, 5)
        player["inventory"][item] = player["inventory"].get(item, 0) + jumlah
        slow(f"Zombie menjatuhkan {jumlah}x {item}!", 0.02)
        time.sleep(0.6)

# ====== MAIN ENTRY ======
if __name__ == "__main__":
    try:
        show_title()
    except KeyboardInterrupt:
        slow("\nPermainan dihentikan. Sampai jumpa!", 0.02)
