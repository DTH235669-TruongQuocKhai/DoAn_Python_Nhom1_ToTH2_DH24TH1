-- 1. Tạo Database
CREATE DATABASE QLBH_DA_TEST
ON 
(
    NAME = N'QLBH_DA_TEST_d',
    FILENAME = N'D:\DTH235669_Python\Database_Test\QLBH_DA_data.mdf', 
    SIZE = 8MB,
    MAXSIZE = 80MB,
    FILEGROWTH = 2MB
)
LOG ON
(
    NAME = N'QLBH_DA_TEST_lg',
    FILENAME = N'D:\DTH235669_Python\Database_Test\QLBH_DA_log.ldf', 
    SIZE = 8MB,
    FILEGROWTH = 2MB
);

USE QLBH_DA_TEST;

-- 2. Tạo Bảng CASI
CREATE TABLE CASI 
(
    MaCaSi char (5) check(MaCaSi like'[A-Z][A-Z][0-9][0-9][0-9]'),
    TenCaSi NVARCHAR(100) NOT NULL,
    NgaySinh DATE,
    QuocTich NVARCHAR(50),
    GioiTinh NVARCHAR(10),
    MoTa NVARCHAR(MAX),
	Primary key (MaCaSi)
);
GO

-- 3. Tạo Bảng THELOAI
CREATE TABLE THELOAI
(
    MaTheLoai char (6) check(MaTheLoai like'[A-Z][A-Z][A-Z][0-9][0-9][0-9]'),
    TenTheLoai NVARCHAR(100) NOT NULL,
    MoTa NVARCHAR(MAX),
	Primary key (MaTheLoai)
);
GO

-- 4. Tạo Bảng ALBUM
CREATE TABLE ALBUM
(
    MaAlbum char (6) check(MaAlbum like'[A-Z][A-Z][A-Z][0-9][0-9][0-9]'),
    TenAlbum NVARCHAR(100) NOT NULL,
    NgayPhatHanh DATE,
    HangPhatHanh NVARCHAR(100),
	Primary key (MaAlbum)
);
GO

-- 5. Tạo Bảng BAIHAT (Bảng chính bạn quản lý)
CREATE TABLE BAIHAT (
    MaBaiHat char (7) check(MaBaiHat like'[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]'),
    TenBaiHat NVARCHAR(100) NOT NULL,
    ThoiLuong TIME, -- Dùng kiểu TIME
    NgayPhatHanh DATE,
    MaCaSi char (5) check(MaCaSi like'[A-Z][A-Z][0-9][0-9][0-9]'),
	MaTheLoai char (6) check(MaTheLoai like'[A-Z][A-Z][A-Z][0-9][0-9][0-9]'),
	MaAlbum char (6) check(MaAlbum like'[A-Z][A-Z][A-Z][0-9][0-9][0-9]'),
    Primary key (MaBaiHat)
);


-- 6. Thiết lập Khóa Ngoại
--BAIHAT(MaTheLoai) -> THELOAI (MaTheLoai)
--BAIHAT(MaCaSi) -> CASI (MaCaSi)
--BAIHAT(MaAlbum) -> ALBUM (MaAlbum)

ALTER TABLE BAIHAT ADD CONSTRAINT fk_BAIHAT_MaTheLoai
FOREIGN KEY (MaTheLoai) REFERENCES THELOAI (MaTheLoai);

ALTER TABLE BAIHAT ADD CONSTRAINT fk_BAIHAT_MaCaSi
FOREIGN KEY (MaCaSi) REFERENCES CASI (MaCaSi);

ALTER TABLE BAIHAT ADD CONSTRAINT fk_BAIHAT_MaAlbum
FOREIGN KEY (MaAlbum) REFERENCES ALBUM (MaAlbum);


-- 7. Chèn Dữ liệu Mẫu (Để test chức năng load_data)

Insert into CASI values ('CS999',N'Sơn Tùng M-TP', '1994-07-05', N'Việt Nam', N'Nam', N'Ca sĩ, nhạc sĩ, nhà sản xuất âm nhạc')
Insert into CASI values ('CS123',N'Mỹ Tâm', '1981-01-16', N'Việt Nam', N'Nữ', N'Ca sĩ nổi tiếng với nhiều bản hit')
SELECT * FROM CASI


Insert into THELOAI values ('POP123',N'Pop', N'Nhạc phổ biến')
Insert into THELOAI values ('BAL456',N'Ballad', N'Nhạc trữ tình, nhẹ nhàng')
SELECT * FROM THELOAI


Insert into ALBUM values ('ALB111',N'M-TP Collection', '2019-06-01', N'M-TP Entertainment')
Insert into ALBUM values ('ALB222',N'Tâm 9', '2017-12-03', N'Mỹ Tâm Production')
SELECT * FROM ALBUM


Insert into BAIHAT values ('BAH9999',N'Nơi Này Có Anh', '00:04:00', '2017-02-14', 'CS999','POP123', 'ALB111')
Insert into BAIHAT values ('BAH5555',N'Người Hãy Quên Em Đi', '00:04:30', '2017-12-03', 'CS123','BAL456', 'ALB222')
SELECT * FROM BAIHAT


SELECT * FROM CASI
SELECT * FROM THELOAI
SELECT * FROM ALBUM
SELECT * FROM BAIHAT
