import { axiosInstance } from "@/lib/axios";
import type { Product } from "@orders/types/product";

export const searchProducts = async (query: string) => {
  const res = await axiosInstance.get<Product[]>(`/products`, {
    params: {
      query,
    },
  });

  return res;
};
