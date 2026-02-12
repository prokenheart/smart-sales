import { Button } from "@mui/material";
import type { Item, ItemPost } from "../types/item";
import axios from "axios";
import type { Customer, Order } from "../types/order";
import type { Dispatch, SetStateAction } from "react";

const API_URL = import.meta.env.VITE_API_URL;
const USER_ID = import.meta.env.VITE_USER_ID;

export default function CreateOrder({
  customer,
  items,
  setIsPosted,
}: Readonly<{
  customer: Customer;
  items: Item[];
  setIsPosted: Dispatch<SetStateAction<boolean>>;
}>) {
  const handleSave = async () => {
    let orderId;
    try {
      const res = await axios.post<Order>(`${API_URL}/orders`, {
        customerId: customer.customerId,
        userId: USER_ID,
      });
      orderId = res.data.orderId;
    } catch (error) {
      console.error("UPDATE FAILED", error);
    }

    const itemPosts: ItemPost[] = items.map((item) => ({
      productId: item.product.productId,
      itemQuantity: item.itemQuantity,
    }));

    try {
      const res = await axios.put(`${API_URL}/orders/${orderId}/items`, {
        listItem: itemPosts,
      });
			if(res.status == 200){
				setIsPosted(true)
			};
    } catch (error) {
      console.error("UPDATE FAILED", error);
    }
  };

  return (
    <Button variant="contained" onClick={handleSave}>
      Save
    </Button>
  );
}
