import { axiosInstance } from "@/lib/axios";
import type { AxiosResponse } from "axios";

type OrdersSummary = {
  key: string;
  total: number;
};

export const getTotalOrdersSummary = async (): Promise<
  AxiosResponse<OrdersSummary[]>
> => {
  try {
    const res = await axiosInstance.get(`/orders/summary/total-orders`);
    return res;
  } catch (error) {
    console.error("Failed to fetch total orders summary:", error);
    throw error;
  }
};

export const getRevenueSummary = async (): Promise<
  AxiosResponse<OrdersSummary[]>
> => {
  try {
    const res = await axiosInstance.get(`/orders/summary/total-revenue`);
    return res;
  } catch (error) {
    console.error("Failed to fetch revenue summary:", error);
    throw error;
  }
};

export const getMonthlyRevenueSummary = async (): Promise<
  AxiosResponse<OrdersSummary[]>
> => {
  try {
    const res = await axiosInstance.get(
      `/orders/summary/total-revenue-12-months`
    );
    return res;
  } catch (error) {
    console.error("Failed to fetch revenue summary in 12 months:", error);
    throw error;
  }
};

export const getTopProductRevenue = async (): Promise<
  AxiosResponse<OrdersSummary[]>
> => {
  try {
    const res = await axiosInstance.get(`/orders/summary/top-product-revenue`);
    return res;
  } catch (error) {
    console.error("Failed to fetch top product revenue summary:", error);
    throw error;
  }
};
