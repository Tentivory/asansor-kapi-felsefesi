#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asansör Kapı Felsefesi — çalışan komisyon yazılımı.

Kapı açılmaz. Kapı değerlendirir.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
import time

KOMISYON = "TentiAŞ Kapı Niyet Komisyonu"
YASAK_KATLAR = {4, 13, 404}

GEREKCELER = [
    "Kapı, açılmanın ontolojik yükünü taşıyamadı.",
    "Düğme basıldı fakat niyet formu eksik.",
    "Kat, kendisini henüz kat olarak tanımlamadı.",
    "Asansör boşluğu bugün iç sesini dinliyor.",
    "Işık yandı, bu bir taahhüt değildir.",
    "Komisyon çoğunluk sağlayamadı: bir üye merdiveni tercih etti.",
    "Kapı aralık kaldı. Aralık, karar değil ara durumdur.",
]


def tutanak_no(kat: int, gerekce: str) -> str:
    ham = f"{kat}|{gerekce}|kapi-niyeti".encode("utf-8")
    return hashlib.sha256(ham).hexdigest()[:10].upper()


def karar_ver(kat: int) -> tuple[str, str]:
    if kat in YASAK_KATLAR:
        return "RED", "Bu kat komisyon takviminde tatil günüdür."
    if kat < 0:
        return "RED", "Bodrum bir kat değil, bir ruh halidir."
    if kat > 40:
        return "ERTELE", "Gökyüzü kat olarak tescil edilmemiştir."
    if random.random() < 0.35:
        return "BEKLET", random.choice(GEREKCELER)
    return "KABUL", "Kapı, gönülsüzce de olsa açılmaya niyet beyan etti."


def yazdir(kat: int, gerekce: str) -> int:
    print(f"=== {KOMISYON} ===")
    print(f"Talep edilen kat: {kat}")
    print(f"Başvuranın gerekçesi: {gerekce or '— gerekçe sunulmadı, bu da bir gerekçedir'}")
    print("Kapı dinleniyor", end="", flush=True)
    for _ in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print()
    sonuc, metin = karar_ver(kat)
    no = tutanak_no(kat, gerekce)
    print(f"Tutanak No : ASNS-{no}")
    print(f"Karar      : {sonuc}")
    print(f"Gerekçe    : {metin}")
    print("Not        : Işık yandıysa bu sizi bağlamaz. Sizi bağlayan merdivendir.")
    return 0 if sonuc == "KABUL" else 2


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Asansör kapısının niyetini soruştur.")
    p.add_argument("kat", nargs="?", type=int, help="gidilmek istenen kat")
    p.add_argument("--kat", dest="kat_bayrak", type=int)
    p.add_argument("--gerekce", default="", help="kapıya sunulacak resmi gerekçe")
    a = p.parse_args(argv)
    kat = a.kat if a.kat is not None else a.kat_bayrak
    if kat is None:
        p.print_help()
        print("\nÖrnek: python asansor.py 7")
        return 1
    return yazdir(kat, a.gerekce)


if __name__ == "__main__":
    sys.exit(main())
