"use client";

import { useState } from "react";
import Autoplay from "embla-carousel-autoplay";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
} from "@/components/ui/carousel";

export function CustomCarousel() {
  const [plugin] = useState(() =>
    Autoplay({ delay: 3000, stopOnInteraction: true }),
  );

  return (
    <Carousel
      plugins={[plugin]}
      opts={{ loop: true, duration: 20 }}
      className="w-full rounded-lg overflow-hidden"
      onMouseEnter={plugin.stop}
      onMouseLeave={plugin.reset}
    >
      <CarouselContent>
        <CarouselItem className="bg-emerald-100 h-50">1</CarouselItem>
        <CarouselItem className="bg-emerald-200 h-50">2</CarouselItem>
        <CarouselItem className="bg-emerald-300 h-50">3</CarouselItem>
      </CarouselContent>
    </Carousel>
  );
}
