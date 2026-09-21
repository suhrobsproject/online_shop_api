"use client";

import { ChevronRight, GalleryVerticalEnd, X } from "lucide-react";
import { Button } from "../ui/button";
import { useState } from "react";

export default function CategoriesDropdown() {
  const [isOpen, setIsOpen] = useState(false);

  const CatalogHandler = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="text-sm">
      <Button
        onClick={CatalogHandler}
        variant="outline"
        className="bg-violet-500 text-white flex items-center"
      >
        {isOpen ? <X /> : <GalleryVerticalEnd />}
        <span>Katalog</span>
      </Button>
      {/* CATEGORIES MENU */}
      <div
        className={`absolute left-0 mt-5 w-full bg-white origin-top transition-all duration-300 ease-out ${
          isOpen
            ? "visible translate-y-0 scale-y-100 opacity-100"
            : "invisible -translate-y-2 scale-y-95 opacity-0 pointer-events-none"
        }
  `}
      >
        <div className="grid grid-cols-[280px_1fr]">
          {/* LEFT SIDE -- CATEGORIES */}
          <div className="border-r pr-4 font-semibold">
            <div className="rounded-md bg-muted px-3 py-2 flex justify-between items-center cursor-pointer">
              <span>Turizm, baliq ovi va ovchilik</span>
              <ChevronRight
                strokeWidth={1}
                className="text-sm text-muted-foreground"
              />
            </div>

            <div className="px-3 py-2 flex justify-between items-center cursor-pointer">
              <span>Elektronika</span>
              <ChevronRight
                strokeWidth={1}
                className="text-sm text-muted-foreground"
              />
            </div>

            <div className="px-3 py-2 flex justify-between items-center cursor-pointer">
              <span>Kiyim</span>
              <ChevronRight
                strokeWidth={1}
                className="text-sm text-muted-foreground"
              />
            </div>

            <div className="px-3 py-2 flex justify-between items-center cursor-pointer">
              <span>Poyabzallar</span>
              <ChevronRight
                strokeWidth={1}
                className="text-sm text-muted-foreground"
              />
            </div>
          </div>

          {/* RIGHT SIDE -- CATEGORY ITEMS */}
          <div className="pl-6">
            <h2 className="mb-3 text-lg font-semibold">
              Turizm, baliq ovi va ovchilik
            </h2>

            <div className="grid grid-cols-3 gap-8">
              <div>
                <h3 className="font-semibold">Kemping</h3>

                <div className="mt-3 space-y-2 text-muted-foreground">
                  <p>Chodirlar</p>
                  <p>Kompressli bog‘lamlar</p>
                  <p>Tentlar va chodirlar</p>
                </div>
              </div>

              <div>
                <h3 className="font-semibold">Baliq ovi</h3>

                <div className="mt-3 space-y-2 text-muted-foreground">
                  <p>G‘altaklar</p>
                  <p>Baliq ovlash asboblari</p>
                  <p>Qayiqlar va aksessuarlar</p>
                </div>
              </div>

              <div>
                <h3 className="font-semibold">Ov va otish mashg‘ulotlari</h3>

                <div className="mt-3 space-y-2 text-muted-foreground">
                  <p>Cho‘zmalar</p>
                  <p>Optika</p>
                  <p>Sport otish mashqlari</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
