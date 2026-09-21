/* eslint-disable react/no-unescaped-entities */
"use client";

import { Button } from "@/components/ui/button";

import { Heart, SearchIcon, ShoppingCart, User } from "lucide-react";
import { Field } from "@/components/ui/field";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";
import CategoriesDropdown from "./CategoriesDropdown";

export default function Navbar() {
  return (
    <nav className="py-10">
      {/* LARGE SCREEN NAVBAR */}
      <div className="hidden md:flex items-center gap-5 lg:gap-10 relative">
        <h1 className="text-2xl font-bold">
          <span className="text-orange-300">Tog'os</span>
          <span className="text-violet-500">Market</span>
        </h1>
        <div className="flex items-center gap-2 flex-1">
          <CategoriesDropdown />
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
        <div className="flex items-center gap-1 lg:gap-2">
          <Button className="flex items-center gap-1" variant="outline">
            <User />
            <span className="hidden lg:block">Kirish</span>
          </Button>
          <Button className="flex items-center gap-1" variant="outline">
            <Heart />
            <span className="hidden lg:block">Saralangan</span>
          </Button>
          <Button className="flex items-center gap-1" variant="outline">
            <ShoppingCart />
            <span className="hidden lg:block">Savat</span>
          </Button>
        </div>
      </div>

      {/* MOBILE NAVBAR */}
      <div className="md:hidden">
        <h1 className="text-2xl font-bold mb-2">
          <span className="text-orange-300">Tog'os</span>
          <span className="text-violet-500">Market</span>
        </h1>
        <div className="flex items-center gap-2 flex-1">
          <CategoriesDropdown />
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
      </div>
    </nav>
  );
}
