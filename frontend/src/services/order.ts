import { axiosInstance } from "@/lib/axios";
import { s3Instance } from "@/lib/s3";
import type { OrdersResponse, Order } from "@orders/types/order";
import type { ItemPost, Item } from "@orders/types/item";

const USER_ID = import.meta.env.VITE_USER_ID;

export const getOrders = async (
  page: number | null,
  cursorDate: string | null,
  cursorId: string | null,
  direction: string | null,
  search: string | null
) => {
  const res = await axiosInstance.get<OrdersResponse>(`/orders`, {
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
  const res = await axiosInstance.post<Order>(`/orders`, {
    customerId: customerId,
    userId: USER_ID,
  });

  return res;
};

export const createItem = async (orderId: string, itemPosts: ItemPost[]) => {
  const res = await axiosInstance.put(`/orders/${orderId}/items`, {
    listItem: itemPosts,
  });

  return res;
};

export const getItemList = async (orderId: string) => {
  const res = await axiosInstance.get<[Item]>(`/orders/${orderId}/items`);
  return res;
};

export const createViewAttachmentURL = async (orderId: string) => {
  const res = await axiosInstance.post(
    `/orders/${orderId}/attachment/view-url`
  );
  return res;
};

export const createUploadAttachmentURL = async (
  orderId: string,
  contentType: string
) => {
  const res = await axiosInstance.post(
    `/orders/${orderId}/attachment/upload-url`,
    {
      contentType: contentType,
    }
  );
  return res;
};

export const uploadAttachment = async (uploadUrl: string, file: File) => {
  const res = await s3Instance.put(uploadUrl, file, {
    headers: {
      "Content-Type": file.type,
    },
  });

  return res;
};

export const updateAttachmentLink = async (orderId: string, s3Key: string) => {
  const res = await axiosInstance.put(`/orders/${orderId}/attachment`, {
    s3Key: s3Key,
  });
  return res;
};
export const updateOrderStatus = async (
  orderId: string,
  statusCode: string
) => {
  const res = await axiosInstance.patch<Order>(`/orders/${orderId}`, {
    statusCode: statusCode,
  });
  return res;
};
