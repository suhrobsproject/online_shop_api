import { Heart, Home, ShoppingCart, User } from "lucide-react";
import { Button } from "../ui/button";
import Link from "next/link";

export default function MobileBottomMenu() {
  return (
    <div className="w-full py-4 px-1 fixed bottom-0 left-0 bg-white border-t md:hidden">
      <div className="flex items-center justify-around">
        <Link href="/" className="flex items-center gap-1 flex-col p-4">
          <Home />
          <span className="">Bosh Sahifa</span>
        </Link>
        <Link href="/" className="flex items-center gap-1 flex-col p-4">
          <Heart />
          <span className="">Saralangan</span>
        </Link>
        <Link href="/" className="flex items-center gap-1 flex-col p-4">
          <ShoppingCart />
          <span className="">Savat</span>
        </Link>
        <Link href="/" className="flex items-center gap-1 flex-col p-4">
          <User />
          <span className="">Kabinet</span>
        </Link>
      </div>
    </div>
  );
}
