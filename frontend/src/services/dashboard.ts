import { axiosInstance } from "@/lib/axios";

type OrdersSummary = {
  key: string;
  total: number;
};

export type DashboardSummaryResponse = {
  totalOrders: OrdersSummary[];
  totalRevenue: OrdersSummary[];
  monthlyRevenue: OrdersSummary[];
  topProducts: OrdersSummary[];
}

export const getDashboardSummary = async (): Promise<DashboardSummaryResponse> => {
  const res = await axiosInstance.get<DashboardSummaryResponse>(`/orders/summary`);
  return res.data;
};
