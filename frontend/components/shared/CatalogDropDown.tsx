"use client";
import { useState } from "react";
import { Button } from "../ui/button";
import { GalleryVerticalEnd } from "lucide-react";

export default function CatalogDropDown() {
  const [isOpen, setIsOpen] = useState(false);

  const catalogHandler = () => {
    setIsOpen(!isOpen);
    console.log(isOpen);
  };
  return (
    <>
      <Button onClick={catalogHandler} variant="outline">
        <GalleryVerticalEnd />
        <span className="hidden lg:block">Katalog</span>
      </Button>

      {/* CATALOG MENU */}
      <div
        className={`absolute left-0 w-full py-5 px-4 bg-white shadow transition-all duration-300 ease-in-out z-50 ${
          isOpen
            ? "top-30 lg:top-15 opacity-100 translate-y-0 pointer-events-auto"
            : "top-30 lg:top-15 opacity-0 -translate-y-4 pointer-events-none"
        }
`}
      >
        men ochildim
      </div>
    </>
  );
}
