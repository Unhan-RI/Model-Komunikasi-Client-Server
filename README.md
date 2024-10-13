<h3><i>Anggota Kelompok</i></h3>
<strong>Muhammad Iqbal Setyawan (320220401017)</strong><br>
<strong>Zerusealtin David Naibaho (320220401025)</strong>
<br>
<h1>Model-Komunikasi-Client-Server</h1>
Proyek ini menunjukkan implementasi sederhana dari load balancer yang mendistribusikan permintaan klien ke beberapa server backend menggunakan algoritma round-robin. Proyek ini terdiri dari beberapa komponen utama:
<ol type="a">
<li>Load Balancer: Menerima koneksi dari klien dan meneruskan permintaan tersebut ke salah satu server backend, mendistribusikan beban secara merata.</li>
<li>Server Backend: Setiap server backend mendengarkan permintaan yang diteruskan oleh load balancer dan merespon klien dengan pesan sederhana.</li>
<li>Klien Multipel: Klien-klien yang disimulasikan mengirim permintaan ke load balancer, yang kemudian meneruskannya ke server backend. Klien kemudian menerima balasan dari server backend tersebut.</li>
</ol>
<h2>Fitur Utama:</h2>
<ul>
<li>Multithreading: Baik load balancer maupun server backend menangani beberapa koneksi secara bersamaan menggunakan multithreading.</li>
<li>Load Balancing Round-Robin: Load balancer meneruskan permintaan klien ke server backend secara bergantian menggunakan algoritma round-robin.</li>
<li>Logging: Log detail dicatat untuk merekam koneksi klien, transfer pesan, dan respons dari server:</li>
<li>Log Load Balancer: Mencatat klien mana yang diteruskan ke server backend mana.</li>
<li>Log Klien: Mencatat waktu koneksi, pesan yang dikirim, respons yang diterima, dan waktu round-trip.</li>
<li>Simulasi Beban Klien: Proyek ini juga menyertakan simulasi klien multipel untuk menguji skalabilitas sistem, dengan jumlah klien yang dapat disesuaikan.</li>
</ul>
<h2>Cara Kerja:</h2>
<ol>
<li>Server Backend: Beberapa server backend dijalankan pada port yang berbeda.
<li>Load Balancer: Load balancer mendengarkan koneksi dari klien dan mendistribusikan permintaan ke server backend yang tersedia.
<li>Klien Multipel: Klien terhubung ke load balancer, mengirim pesan, dan menerima balasan dari salah satu server backend.
</ol>
<br>
Proyek ini merupakan versi sederhana dari arsitektur client-server terdistribusi yang berguna untuk mempelajari tentang load balancing, pemrograman jaringan secara bersamaan, dan pencatatan log.
