# butuh --> pip install kazoo
from kazoo.client import KazooClient
from kazoo.recipe.lock import Lock
import threading, time

# def worker(worker_id):
#     zk = KazooClient(hosts='localhost:2181')
#     zk.start()
#     lock = Lock(zk, "/myapp/lock")
#     print(f"[Worker-{worker_id}] Mencoba acquire lock...")
#     with lock:
#         print(f"[Worker-{worker_id}] Lock diperoleh! Masuk CR.")
#         time.sleep(2)
#         print(f"[Worker-{worker_id}] Selesai, release lock.")
#     zk.stop()

#SIMULASI CRASH: Kita buat Worker ke-3 mengalami error di tengah CR
def worker(worker_id):
    zk = KazooClient(hosts='localhost:2181')
    zk.start()
    lock = Lock(zk, "/myapp/lock")
    
    try:
        print(f"[Worker-{worker_id}] Mencoba acquire lock...")
        with lock:
            print(f"[Worker-{worker_id}] Lock diperoleh! Masuk CR.")
            
            # SIMULASI CRASH: Jika ini Worker ke-3, kita buat dia error/mati
            if worker_id == 3:
                print(f"[Worker-{worker_id}] !!! CRASH TERJADI DI TENGAH CR !!!")
                raise Exception("Koneksi Putus / Daya Mati")
                
            time.sleep(2)
            print(f"[Worker-{worker_id}] Selesai, release lock.")
    except Exception as e:
        print(f"[Worker-{worker_id}] Keluar karena Error: {e}")
    finally:
        zk.stop()

threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print("Semua worker selesai!")

