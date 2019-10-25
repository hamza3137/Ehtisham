@echo off

md %1

md %1\commons

md %1\mp
md %1\mp\upload
echo null > %1\mp\upload\temp.txt

md %1\bh
md %1\bh\upload
echo null > %1\bh\upload\temp.txt

md %1\nu
md %1\nu\upload
echo null > %1\nu\upload\temp.txt


md %1\nb
md %1\nb\upload
echo null > %1\nb\upload\temp.txt


md %1\nr
md %1\nr\upload
echo null > %1\nr\upload\temp.txt

md %1\sn
md %1\sn\upload
echo null > %1\sn\upload\temp.txt


md %1\mmc
md %1\mmc\upload
echo null > %1\mmc\upload\temp.txt


@echo on