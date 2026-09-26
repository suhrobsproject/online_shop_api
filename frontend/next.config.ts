import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      new URL(
        "https://images.uzum.uz/da7tu99e6phbsqqkv5dg/t_product_540_high.jpg",
      ),
    ],
  },
};

export default nextConfig;
