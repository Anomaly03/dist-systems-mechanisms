import etcd3, threading, time

# def watch_key(etcd_client, key):
#     """Watch sebuah key dan print setiap perubahan."""
#     print(f"Watching key: {key}")
#     events_iterator, cancel = etcd_client.watch(key)
#     for event in events_iterator:
#         print(f" Event: {type(event).__name__} | "
#               f"key={event.key.decode()} | "
#               f"value={event.value.decode() if event.value else 'deleted'}")

# # Inisialisasi client harus di luar fungsi agar terbaca global
# etcd = etcd3.client(host='localhost', port=2379)

# # Start watcher in background
# watcher_thread = threading.Thread(
#     target=watch_key, args=(etcd, b'/config/threshold'), daemon=True
# )
# watcher_thread.start()

# # Simulate config updates
# time.sleep(0.5)
# for i in range(5):
#     value = f"threshold={80 + i}"
#     etcd.put('/config/threshold', value)
#     print(f"Updated: {value}")
#     time.sleep(1)

# Versi dengan 2 Watcher paralel
def watch_key(etcd_client, key):
    """Watch sebuah key dan print setiap perubahan."""
    print(f"[*] Started Watcher for key: {key}")
    # events_iterator adalah stream yang akan terus terbuka
    events_iterator, cancel = etcd_client.watch(key)
    for event in events_iterator:
        print(f"\n[ALERT] Event on {key.decode()}: {event.value.decode() if event.value else 'deleted'}")

# 1. Inisialisasi client
etcd = etcd3.client(host='localhost', port=2379)

# 2. Start Watcher pertama (/config/threshold)
threading.Thread(
    target=watch_key, args=(etcd, b'/config/threshold'), daemon=True
).start()

# 3. Tambahkan Watcher kedua secara paralel (/config/timeout)
threading.Thread(
    target=watch_key, args=(etcd, b'/config/timeout'), daemon=True
).start()

# 4. Simulasi update kedua key secara bergantian
time.sleep(1)
print("\n--- Memulai Simulasi Update ---")

for i in range(3):
    # Update threshold
    val_threshold = f"threshold={80 + i}"
    etcd.put('/config/threshold', val_threshold)
    print(f"Sent: {val_threshold}")
    
    # Update timeout
    val_timeout = f"timeout={10 + i}s"
    etcd.put('/config/timeout', val_timeout)
    print(f"Sent: {val_timeout}")
    
    time.sleep(1.5)