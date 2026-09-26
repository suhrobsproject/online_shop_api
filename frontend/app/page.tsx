import { CustomCarousel } from "@/components/shared/CustomCarousel";
import { getProducts } from "@/services/products";
import CardsSection from "@/components/sections/CardsSection";

export default async function HomePage() {
  const data = await getProducts();

  console.log(data);

  return (
    <>
      <CustomCarousel />
      <CardsSection />
    </>
  );
}
