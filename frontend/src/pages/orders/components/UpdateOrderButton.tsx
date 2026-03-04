import { Button } from "@mui/material";
import { useContext } from "react";
import type { Dispatch, ReactElement, SetStateAction } from "react";
import { HttpStatusCode } from "axios";

import { UpdateTableContext } from "@orders/context/UpdateTableContext";

import type { Item, ItemPost } from "@orders/types/item";
import type { Order, Customer } from "@orders/types/order";

import { createItem } from "@services/order";

const UpdateOrderButton = ({
  order,
  items,
  setSelectedCustomer,
  setSelectedItems,
}: Readonly<{
  order: Order | undefined;
  items: Item[];
  setSelectedCustomer: Dispatch<SetStateAction<Customer | undefined>>;
  setSelectedItems: Dispatch<SetStateAction<Item[]>>;
}>): ReactElement => {
  const updateTable = useContext(UpdateTableContext);

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
      if (!order) return;
      const res = await createItem(order.orderId, itemPosts);
      if (res.status == HttpStatusCode.Ok) {
        const newTotal = calcOrderTotal(items).toString();

        if (!order) return;

        setSelectedCustomer(undefined);
        setSelectedItems([]);

        updateTable?.setUpdatedOrder?.({
          ...order,
          orderTotal: newTotal,
        });
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
};

export default UpdateOrderButton;
