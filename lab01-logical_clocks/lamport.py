# Import modul yang diperlukan
import threading, queue, time, random 

# Definisikan kelas Process yang mewakili setiap proses dalam sistem
class Process(threading.Thread): 
    def __init__(self, pid, peers): #pid: ID proses, peers: dict yang berisi referensi ke proses lain
        super().__init__(daemon=True) # Inisialisasi thread sebagai daemon agar program bisa keluar meskipun thread masih berjalan
        self.pid = pid # Definisikan ID proses
        self.clock = 0 # Inisialisasi clock Lamport
        self.inbox = queue.Queue() # Antrian untuk menerima pesan dari proses lain
        self.peers = peers # dict: pid -> Process

    def send(self, target_pid, message): # Fungsi untuk mengirim pesan ke proses lain
        self.clock += 1
        ts = self.clock
        print(f" [{self.pid}|t={ts}] SEND '{message}' → {target_pid}")
        self.peers[target_pid].inbox.put((ts, self.pid, message))

    def receive(self): # Fungsi untuk menerima pesan dari proses lain
        ts, sender, msg = self.inbox.get()
        self.clock = max(self.clock, ts) + 1
        print(f" [{self.pid}|t={self.clock}] RECV '{msg}' ← {sender}")

    def local_event(self, name): # Fungsi untuk mencatat event  
        self.clock += 1
        print(f" [{self.pid}|t={self.clock}] EVENT '{name}'")

    def run(self): # Fungsi utama yang dijalankan saat thread dimulai
        time.sleep(random.uniform(0, 0.2))
        if self.pid == "P1":
            self.local_event("start")
            self.send("P2", "hello")
            self.receive() # will get from P2
        elif self.pid == "P2":
            self.receive() # dari P1
            self.local_event("process")
            self.send("P1", "ack")
            self.send("P3", "data")
        elif self.pid == "P3":
            self.receive() # dari P2
            self.local_event("process")
            self.send("P4", "this one is for you")
            self.receive() # dari P4
        elif self.pid == "P4":
            self.receive() # dari P3
            self.local_event("done")
            self.send("P3", "i got it")

processes = {} # Dictionary untuk menyimpan referensi ke semua proses, dengan key sebagai pid dan value sebagai instance Process
for pid in ["P1", "P2", "P3", "P4"]:
    processes[pid] = Process(pid, processes)

print("=== Jalankan simulasi Lamport Clock ===")
for p in processes.values(): p.start()
for p in processes.values(): p.join(timeout=3)
print("=== Selesai ===")