# lab4_vector_clock.py

class VectorClock:
    def __init__(self, pid, all_pids):
        self.pid = pid
        self.clock = {p: 0 for p in all_pids}

    def tick(self):
        self.clock[self.pid] += 1
        return dict(self.clock)

    def send(self):
        self.clock[self.pid] += 1
        return dict(self.clock)

    def receive(self, remote_ts):
        for p in self.clock:
            self.clock[p] = max(self.clock[p], remote_ts[p])
        self.clock[self.pid] += 1  # increment setelah merge
        return dict(self.clock)

    def happens_before(self, ts_a, ts_b) -> bool:
        """Return True jika ts_a causally precedes ts_b."""
        leq = all(ts_a[p] <= ts_b[p] for p in ts_a)
        lt = any(ts_a[p] < ts_b[p] for p in ts_a)
        return leq and lt

    def concurrent(self, ts_a, ts_b) -> bool:
        return (not self.happens_before(ts_a, ts_b) and 
                not self.happens_before(ts_b, ts_a))

# --- Demo Sesuai Tugas ---
pids = ["P1", "P2", "P3"]
vc1 = VectorClock("P1", pids)
vc2 = VectorClock("P2", pids)
vc3 = VectorClock("P3", pids)

# SKENARIO 1: Causal Ordering (a -> b)
# ts_a = vc1.send()      # P1 sends
# vc2.receive(ts_a)      # P2 receives ts_a
# ts_b = vc2.send()      # P2 sends after receiving

# print("ts_a:", ts_a)
# print("ts_b:", ts_b)
# print("a -> b?", vc1.happens_before(ts_a, ts_b))   # True
# print("b -> a?", vc1.happens_before(ts_b, ts_a))   # False
# print("concurrent?", vc1.concurrent(ts_a, ts_b))  # False (a->b, bukan concurrent)

# # Skenario 2: Concurrent (a || c)
# # P3 kirim pesan tanpa tahu tentang ts_a
# ts_c = vc3.send()    

# print("\nts_a (dari P1):", ts_a)
# print("ts_c (dari P3):", ts_c)
# print("a -> c?", vc1.happens_before(ts_a, ts_c))   # False
# print("c -> a?", vc1.happens_before(ts_c, ts_a))   # False
# print("a || c (concurrent)?", vc1.concurrent(ts_a, ts_c))  # True!

# SKENARIO 2: Concurrent - P1 dan P3 beraksi sendiri-sendiri
# print("\n--- Skenario Konkuren ---")

# # Reset clock untuk simulasi baru
# vc1 = VectorClock("P1", ["P1", "P2", "P3"])
# vc3 = VectorClock("P3", ["P1", "P2", "P3"])

# # Event a: P1 melakukan sesuatu (misal kirim pesan ke tempat lain atau internal tick)
# ts_a = vc1.tick() 

# # Event c: P3 melakukan sesuatu secara bersamaan (tanpa pesan dari P1)
# ts_c = vc3.tick()

# print(f"Timestamp Event A (P1): {ts_a}") # Output: {'P1': 1, 'P2': 0, 'P3': 0}
# print(f"Timestamp Event C (P3): {ts_c}") # Output: {'P1': 0, 'P2': 0, 'P3': 1}

# # Pembuktian dengan fungsi concurrent()
# is_concurrent = vc1.concurrent(ts_a, ts_c)
# print(f"Apakah A dan C concurrent? {is_concurrent}")

# SKENARIO 3: P2 dan P3 mengirim pesan ke P1 secara independen (concurrent)
print("\n--- Skenario Tambahan: P2 & P3 kirim ke P1 ---")

# Reset clocks
vc1 = VectorClock("P1", pids)
vc2 = VectorClock("P2", pids)
vc3 = VectorClock("P3", pids)

# Event 1: P2 mengirim ke P1
ts_p2_send = vc2.send() 
print(f"P2 Send: {ts_p2_send}") # Expected: {'P1': 0, 'P2': 1, 'P3': 0}

# Event 2: P3 mengirim ke P1 secara bersamaan (tidak tahu aksi P2)
ts_p3_send = vc3.send()
print(f"P3 Send: {ts_p3_send}") # Expected: {'P1': 0, 'P2': 0, 'P3': 1}

# Event 3: P1 menerima dari P2
vc1.receive(ts_p2_send)
print(f"P1 receive dari P2: {vc1.clock}")


# Event 4: P1 menerima dari P3
ts_p1_final = vc1.receive(ts_p3_send)
print(f"P1 Final State (setelah terima semua P2 dan P3): {ts_p1_final}")