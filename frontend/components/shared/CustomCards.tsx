/* eslint-disable react/no-unescaped-entities */
"use client";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { MessageCircleMore, ShoppingCartPlus } from "lucide-react";
import Image from "next/image";
import { Button } from "../ui/button";

export default function CustomCards() {
  return (
    <Card className="group">
      <div className="w-full min-h-80 h-full relative">
        <Image
          fill
          src="https://images.uzum.uz/da7tu99e6phbsqqkv5dg/t_product_540_high.jpg"
          alt="Event cover"
          className="relative z-20 aspect-video w-full object-cover group-hover:scale-103 transition duration-100 ease-in"
        />
      </div>

      <CardHeader>
        {/* PRICE */}
        <p className="font-semibold text- text-blue-500">57 980</p>

        <CardTitle className="line-clamp-2 font-light text-sm w-full">
          Erkaklar krossovkalari, kundalik poyabzallar, issiqlikni
          qisqartiruvchi bog'ichli
        </CardTitle>
        <CardDescription className="flex items-center gap-1">
          <MessageCircleMore strokeWidth={1} size={18} />
          <span>124 ta sharx</span>
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Button className="w-full bg-blue-500 flex items-center gap-3 hover:bg-blue-600">
          <ShoppingCartPlus strokeWidth={1.75} />
          <span>Qo'shish</span>
        </Button>
      </CardContent>
    </Card>
  );
}
