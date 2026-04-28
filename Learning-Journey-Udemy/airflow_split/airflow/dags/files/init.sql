CREATE TABLE IF NOT EXISTS karyawan (
			    id SERIAL PRIMARY KEY,
			    nama TEXT NOT NULL,
			    tanggal_lahir DATE NOT NULL
			);
	
INSERT INTO karyawan (nama, tanggal_lahir) VALUES
('Andi Saputra', '1990-03-15'),
('Budi Santoso', '1988-07-22'),
('Citra Lestari', '1992-11-30'),
('Dewi Anggraini', '1985-01-10'),
('Eko Prasetyo', '1995-05-05'),
('Fajar Nugroho', '1993-12-01'),
('Gita Permata', '1989-08-19'),
('Hendra Wijaya', '1991-02-14'),
('Intan Maharani', '1994-06-25'),
('Joko Susilo', '1987-09-09');