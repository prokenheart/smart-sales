import { axiosInstance } from "@/lib/axios";
import type { Customer } from "@orders/types/order";

export const searchCustomers = async (query: string) => {
  const res = await axiosInstance.get<Customer[]>(`/customers`, {
    params: {
      query,
    },
  });

  return res;
};
