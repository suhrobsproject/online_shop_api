import client from "@/lib/axios";

export async function getProducts() {
  const { data } = await client.get("/products/");
  return data;
}
