import { getProducts } from "@/lib/axios";

export default async function HomePage() {
  const data = await getProducts();

  console.log(data);

  return <div>Salom</div>;
}
