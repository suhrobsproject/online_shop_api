/* eslint-disable react/no-unescaped-entities */
"use client";

import { Heart, SearchIcon, ShoppingCart, User } from "lucide-react";
import { Field } from "@/components/ui/field";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";
import Link from "next/link";
import CatalogDropDown from "./CatalogDropDown";

export default function Navbar() {
  return (
    <nav className="py-10">
      {/* LARGE SCREEN NAVBAR */}
      <div className="flex items-center flex-col-reverse lg:flex-row gap-5 lg:gap-10 relative">
        <Link href="/" className="text-2xl font-bold hidden lg:block">
          <span className="text-orange-300">Tog'os</span>
          <span className="text-violet-500">Market</span>
        </Link>
        <div className="flex items-center gap-2 flex-1 w-full">
          <CatalogDropDown />
          <Field className="w-full">
            <InputGroup className="px-4">
              <InputGroupInput
                className="text-base"
                id="inline-start-input"
                placeholder="Search..."
              />
              <InputGroupAddon align="inline-end">
                <SearchIcon className="text-muted-foreground" />
              </InputGroupAddon>
            </InputGroup>
          </Field>
        </div>
        <div className="w-full lg:w-auto flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold lg:hidden block">
            <span className="text-orange-300"></span>
            <span className="text-violet-500">LOGO</span>
          </Link>
          <div className="flex items-center gap-1 lg:gap-2">
            <Link
              href="/login"
              className="flex items-center gap-1 p-2 rounded-md overflow-hidden hover:bg-muted transition duration-75 ease-in"
            >
              <User />
              <span className="hidden lg:block">Kirish</span>
            </Link>
            <Link
              href="/favourite"
              className="flex items-center gap-1 p-2 rounded-md overflow-hidden hover:bg-muted transition duration-75 ease-in"
            >
              <Heart />
              <span className="hidden lg:block">Saralangan</span>
            </Link>
            <Link
              href="/basket"
              className="flex items-center gap-1 p-2 rounded-md overflow-hidden hover:bg-muted transition duration-75 ease-in"
            >
              <ShoppingCart />
              <span className="hidden lg:block">Savat</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
