import { Button } from "@mui/material";
import type { Item, ItemPost } from "../types/item";
import type { Order, Customer } from "../types/order";
import type { Dispatch, SetStateAction } from "react";
import { createItem } from "../../../services/order";

export default function UpdateOrder({
  order,
  items,
  setIsPosted,
  setSelectedCustomer,
  setSelectedItems,
  setUpdatedOrder,
}: Readonly<{
  order: Order | undefined;
  items: Item[];
  setIsPosted: Dispatch<SetStateAction<boolean>>;
  setSelectedCustomer: Dispatch<SetStateAction<Customer | undefined>>;
  setSelectedItems: Dispatch<SetStateAction<Item[]>>;
  setUpdatedOrder?: Dispatch<SetStateAction<Order | undefined>>;
}>) {
  const calcOrderTotal = (items: Item[]): number => {
    return items.reduce((sum, item) => {
      return sum + item.itemQuantity * item.itemPrice;
    }, 0);
  };

  const handleSave = async () => {
    const itemPosts: ItemPost[] = items.map((item) => ({
      productId: item.product.productId,
      itemQuantity: item.itemQuantity,
    }));

    try {
      if (order != undefined) {
        const res = await createItem(order.orderId, itemPosts);
        if (res.status == 200) {
          const newTotal = calcOrderTotal(items).toString();

          if (!order) return;

          setUpdatedOrder?.({
            ...order,
            orderTotal: newTotal,
          });

          setSelectedCustomer(undefined);
          setSelectedItems([]);

          setIsPosted(true);
        }
      }
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
