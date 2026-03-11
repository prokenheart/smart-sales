import { Button, CircularProgress } from "@mui/material";
import { useContext, useState } from "react";
import type { Dispatch, ReactElement, SetStateAction } from "react";
import { HttpStatusCode } from "axios";
import { useSnackbar } from "notistack";

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
  const [isLoading, setIsLoading] = useState(false);

  const { enqueueSnackbar } = useSnackbar();

  const calcOrderTotal = (items: Item[]): number => {
    return items.reduce((sum, item) => {
      return sum + item.itemQuantity * item.itemPrice;
    }, 0);
  };

  const handleSave = async () => {
    if (!order) return;

    setIsLoading(true);

    const itemPosts: ItemPost[] = items.map((item) => ({
      productId: item.product.productId,
      itemQuantity: item.itemQuantity,
    }));

    try {
      const res = await createItem(order.orderId, itemPosts);

      if (res.status === HttpStatusCode.Ok) {
        const newTotal = calcOrderTotal(items).toString();

        setSelectedCustomer(undefined);
        setSelectedItems([]);

        updateTable?.setUpdatedOrder?.({
          ...order,
          orderTotal: newTotal,
        });
      }
    } catch (error) {
      console.error("UPDATE FAILED", error);
    } finally {
      setIsLoading(false);
      enqueueSnackbar("Order updated successfully", { variant: "success" });
    }
  };

  return (
    <Button variant="contained" onClick={handleSave} disabled={isLoading}>
      {isLoading ? <CircularProgress size={20} /> : "Save"}
    </Button>
  );
};

export default UpdateOrderButton;
