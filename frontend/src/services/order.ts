import axios from "axios";
import type { OrdersResponse, Order } from "../pages/orders/types/order";
import type { ItemPost, Item } from "../pages/orders/types/item";

const API_URL = import.meta.env.VITE_API_URL;
const USER_ID = import.meta.env.VITE_USER_ID;

export const getOrders = async (
  page: number | undefined,
  cursorDate: string | undefined,
  cursorId: string | undefined,
  direction: string | undefined,
  search: string | undefined
) => {
  const res = await axios.get<OrdersResponse>(`${API_URL}/orders`, {
    params: {
      page,
      cursorDate,
      cursorId,
      direction,
      search,
    },
  });

  return res;
};

export const createOrder = async (customerId: string) => {
  const res = await axios.post<Order>(`${API_URL}/orders`, {
    customerId: customerId,
    userId: USER_ID,
  });

  return res;
};

export const createItem = async (
  orderId: string,
  itemPosts: ItemPost[]
) => {
  const res = await axios.put(`${API_URL}/orders/${orderId}/items`, {
    listItem: itemPosts,
  });

  return res;
};

export const getItemList = async (orderId: string) => {
  const res = await axios.get<[Item]>(`${API_URL}/orders/${orderId}/items`);
  return res;
};
