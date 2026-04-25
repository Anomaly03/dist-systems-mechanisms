import threading, time
from kazoo.client import KazooClient

def manual_worker(worker_id):
    zk = KazooClient(hosts='127.0.0.1:2181')
    zk.start()

    # 1.Membuat folder untuk lock (jika belum ada)
    path_induk = "/mylock"
    zk.ensure_path(path_induk)

    # 2. Buat Ephemeral Sequential Node (Antrean)
    my_path = zk.create(f"{path_induk}/node-", ephemeral=True, sequence=True)
    my_node_name = my_path.split("/")[-1] # Ambil nama filenya saja

    print(f"[Worker-{worker_id}] Masuk antrean dengan nomor: {my_node_name}")

    while True:
        # 3. Cek semua anak di path_induk, urutkan berdasarkan nomor urut
        children = zk.get_children(path_induk)
        # Mengurutkan berdasarkan nomor urut (asumsi format node-0000000001, node-0000000002, dst)
        sorted_children = sorted(children)

        # 4. Syarat untuk masuk CR: jika node kita yang paling kecil, berarti kita dapat lock
        if my_node_name == sorted_children[0]:
            print(f" >>> [Worker-{worker_id}] MENANG! (Node: {my_node_name}) Masuk CR...")
            time.sleep(2) # Simulasi kerja
            print(f" <<< [Worker-{worker_id}] SELESAI. Melepas lock.")
            break
        else:
            # 5. Jika belum dapat lock, tunggu sebentar dan cek lagi (polling sederhana)
            time.sleep(0.5)

    # 6. Setelah selesai, hapus node kita untuk memberi kesempatan ke worker berikutnya
    zk.delete(my_path)
    zk.stop()

threads = [threading.Thread(target=manual_worker, args=(i,)) for i in range(5)]
for t in threads: t.start()
for t in threads: t.join()