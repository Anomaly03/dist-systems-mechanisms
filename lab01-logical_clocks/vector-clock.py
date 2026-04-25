# Hasil mofikasi dari lamport.py untuk implementasi vector clock yang menggunakan array/dictionary untuk mencatat waktu setiap node, bukan hanya satu angka.
import threading, queue, time, random

class Process(threading.Thread):
    def __init__(self, pid, all_pids, peers):
        super().__init__(daemon=True)
        self.pid = pid
        # Vector Clock: mencatat waktu setiap node
        self.clock = {p: 0 for p in all_pids} 
        self.inbox = queue.Queue()
        self.peers = peers

    def send(self, target_pid, message):
        self.clock[self.pid] += 1 # Increment clock sendiri
        ts = dict(self.clock) # Kirim salinan vector saat ini
        print(f" [{self.pid}|t={ts}] SEND '{message}' → {target_pid}")
        self.peers[target_pid].inbox.put((ts, self.pid, message))

    def receive(self):
        ts, sender, msg = self.inbox.get()
        # Merge: ambil nilai maksimal untuk setiap elemen
        for p in self.clock:
            self.clock[p] = max(self.clock[p], ts[p])
        self.clock[self.pid] += 1 # Increment clock sendiri setelah merge
        print(f" [{self.pid}|t={self.clock}] RECV '{msg}' ← {sender}")

    def local_event(self, name):
        self.clock[self.pid] += 1
        print(f" [{self.pid}|t={self.clock}] EVENT '{name}'")

    def run(self):
        # Jalankan logika alur pesan yang sama
        if self.pid == "P1":
            self.local_event("start")
            self.send("P2", "hello")
            self.receive()
        elif self.pid == "P2":
            self.receive()
            self.local_event("process")
            self.send("P1", "ack")
            self.send("P3", "data")
        elif self.pid == "P3":
            self.receive()
            self.local_event("process")
            self.send("P4", "msg")
            self.receive()
        elif self.pid == "P4":
            self.receive()
            self.local_event("done")
            self.send("P3", "i got it")

pids = ["P1", "P2", "P3", "P4"]
processes = {}
for pid in pids:
    processes[pid] = Process(pid, pids, processes)

print("=== Jalankan simulasi Vector Clock ===")
for p in processes.values(): p.start()
for p in processes.values(): p.join(timeout=3)