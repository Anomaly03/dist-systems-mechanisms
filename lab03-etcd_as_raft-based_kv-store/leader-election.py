import etcd3
import time
import uuid

# ID unik untuk membedakan antar node di terminal berbeda
node_id = str(uuid.uuid4())[:8]

def campaign_leader(etcd):
    print(f"[*] Node {node_id} memulai kampanye...")
    
    while True:
        # Membuat lease dengan TTL 5 detik
        lease = etcd.lease(5)
        
        # Mencoba menulis ke key '/election/leader' hanya jika key tersebut kosong (Version == 0)
        status = etcd.transaction(
            compare=[etcd3.transactions.Version('/election/leader') == 0],
            success=[etcd3.transactions.Put('/election/leader', node_id, lease=lease)],
            failure=[etcd3.transactions.Get('/election/leader')]
        )
        
        if status[0] is True:
            print(f"[{time.strftime('%H:%M:%S')}] >>> MANTAP! Node {node_id} adalah LEADER.")
        else:
            # Jika gagal, ambil ID node yang saat ini menjabat sebagai leader
            try:
                current_leader_id = status[1][0][0].decode()
                print(f"[{time.strftime('%H:%M:%S')}] [-] Gagal. Kursi Leader diduduki oleh: {current_leader_id}")
            except:
                print(f"[{time.strftime('%H:%M:%S')}] [-] Sedang terjadi persaingan...")
            
        time.sleep(2)

try:
    etcd_client = etcd3.client(host='localhost', port=2379)
    campaign_leader(etcd_client)
except KeyboardInterrupt:
    print("\n[!] Node mengundurkan diri dari kampanye.")