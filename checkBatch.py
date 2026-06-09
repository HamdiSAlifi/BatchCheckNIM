from pddiktipy import api
import time

# Partial match targets (lowercase)
TARGET_UNIVERSITY = "andalas"
TARGET_MAJOR = "informat"

def normalize(text):
    return text.lower().strip() if text else ""

def trunc(s, n):
    return s if len(s) <= n else s[:n-2] + ".."

def search_single(name, index, total):
    """Opens a fresh API connection per search to avoid hangs."""
    status = "❌ Not Found"
    actual_name = "-"
    university = "-"
    major = "-"
    name_corrected = False

    try:
        with api() as client:
            results = client.search_mahasiswa(name)

        if results and len(results) > 0:
            best = None
            for r in results:
                uni   = r.get('nama_pt', '')
                prodi = r.get('nama_prodi', '')
                if TARGET_UNIVERSITY in normalize(uni) and TARGET_MAJOR in normalize(prodi):
                    best = r
                    break

            if best:
                university  = best.get('nama_pt', 'Unknown')
                major       = best.get('nama_prodi', 'Unknown')
                actual_name = best.get('nama', name).title()

                if normalize(actual_name) != normalize(name):
                    status = "✅ Match ✏️ name diff"
                    name_corrected = True
                else:
                    status = "✅ Match"
            else:
                first = results[0]
                university  = first.get('nama_pt', 'Unknown')
                major       = first.get('nama_prodi', 'Unknown')
                actual_name = first.get('nama', name).title()

                uni_ok   = TARGET_UNIVERSITY in normalize(university)
                major_ok = TARGET_MAJOR in normalize(major)

                if uni_ok:
                    status = "⚠️  Andalas, wrong major"
                elif major_ok:
                    status = "⚠️  Informat, wrong uni"
                else:
                    status = "❌ Wrong uni/major"
        else:
            status = "❌ Not in DB"

    except Exception as e:
        status = "⚠️  API Error"
        university = str(e)[:20]

    label = f"[{index}/{total}]" if total > 0 else f"[{index}]"
    print(f"{label:<10} {trunc(name,30):<30} {status:<22} {trunc(actual_name,28):<28} {trunc(university,25):<25} {trunc(major,24)}")

    return {
        "searched": name,
        "actual_name": actual_name,
        "status": status,
        "university": university,
        "major": major,
        "name_corrected": name_corrected
    }

def print_header():
    print("=" * 110)
    print(f"{'No':<10} {'Searched Name':<30} {'Status':<22} {'Actual Name in DB':<28} {'University':<25} {'Major'}")
    print("=" * 110)

def print_summary(results_log):
    found = [r for r in results_log if "✅" in r["status"]]
    corrections = [r for r in results_log if r["name_corrected"]]

    print("=" * 110)
    print(f"\n📊 SUMMARY")
    print(f"   ✅  Full match (Andalas + Informatika) : {len(found)}")
    print(f"   ✏️   Name corrections found             : {len(corrections)}")
    print(f"   ❌  Not matched / not found            : {len(results_log) - len(found)}")
    print(f"   📋  Total searched                     : {len(results_log)}")

    if corrections:
        print(f"\n{'='*60}")
        print("✏️  NAME CORRECTIONS:")
        print(f"{'='*60}")
        for r in corrections:
            print(f"   Searched : {r['searched']}")
            print(f"   DB Name  : {r['actual_name']}")
            print()

def mode_batch(names):
    print(f"\n🔍 Batch mode — searching {len(names)} name(s)...\n")
    print_header()
    results_log = []
    for i, name in enumerate(names, 1):
        result = search_single(name.strip(), i, len(names))
        results_log.append(result)
        time.sleep(2)
    print_summary(results_log)

def mode_interactive():
    print("\n Interactive mode — type a name and press Enter to search.")
    print("   Comma-separated names are supported.")
    print("   Type 'done' or leave empty to finish.\n")
    print_header()

    results_log = []
    counter = 1

    while True:
        try:
            raw = input("🔎 Name: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not raw or raw.lower() in ("done", "exit", "quit", "q"):
            break

        names = [n.strip() for n in raw.split(",") if n.strip()]
        for name in names:
            print(f"    Searching...", end="\r")
            result = search_single(name, counter, 0)
            results_log.append(result)
            counter += 1
            time.sleep(2)

    if results_log:
        print_summary(results_log)
    else:
        print("\nNo names were searched.")

def mode_single(name):
    print(f"\n🔍 Searching: {name}")
    print("   ⏳ Please wait...")
    print_header()
    result = search_single(name, 1, 1)
    print_summary([result])

def main():
    print("╔════════════════════════════════════════════════════════╗")
    print("║  PDDIKTI Search — Universitas Andalas × Informatika   ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    print("Choose mode:")
    print("  [1] Interactive — type names one by one")
    print("  [2] Single      — search one name now")
    print()

    try:
        choice = input("Enter choice (1/2): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        return

    if choice == "1":
        mode_interactive()
    elif choice == "2":
        try:
            name = input("Enter name to search: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return
        if name:
            mode_single(name)
        else:
            print("No name entered.")
    else:
        print("Invalid choice. Defaulting to interactive mode.")
        mode_interactive()

if __name__ == "__main__":
    main()